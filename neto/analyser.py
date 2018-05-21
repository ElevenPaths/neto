# -*- coding: utf-8 -*-
#
################################################################################
#
#   Copyright 2017-2018 ElevenPaths
#
#   Neto is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

import argparse
import datetime as dt
import json
import os
import tempfile
import traceback
import shutil
import sys

import neto
import neto.lib.crypto.md5 as md5
import neto.lib.utils as utils
import neto.lib.validations as validations
from neto.lib.extensions import Extension
from neto.downloaders.http import HTTPResource


def analyseExtensionFromFile(filePath, quiet=False, analysisPath=utils.getConfigPath()["appPathDataAnalysis"], tmpPath=tempfile.gettempdir()):
    """
    Main function for Neto Analyser.

    Performs an analysis of a locally stored file.

    Params:
    -------
        filePath: The local path to an extension.
        quiet: A boolean that defines whether to print an output.
        analysisPath: The folder where the extension will be stored.
        tmpPath: The folder where unzipped files will be created.

    Returns:
    --------
        An Extension object.

    Raises:
    """
    # Process the filePath
    if os.path.isfile(filePath):
        ext = Extension(filePath, tFolder=tmpPath)

        print("[*]\tData collected:\n" + str(ext))

        # Store the features extracted
        outputFile = os.path.join(analysisPath, ext.digest["md5"] + ".json")
        if not quiet:
            print("[*]\tAdditional information about the extension can be found as a JSON at {}…".format(outputFile))
        with open(outputFile, "w") as oF:
            oF.write(json.dumps(ext.__dict__, indent=2))
        return ext
    else:
        raise FileNotFoundError("The filepath provided ({}) does not match with a file.".format(filePath))

def analyseExtensionFromURI(uri, quiet=False, analysisPath=utils.getConfigPath()["appPathDataAnalysis"], downloadPath=utils.getConfigPath()["appPathDataFiles"], tmpPath=tempfile.gettempdir()):
    """
    Main function for Neto Analyser.

    Performs an analysis of a URI extension provided using the command line.

    Params:
    -------
        uri: The parameter options received from the command line.
        quiet: A boolean that defines whether to print an output.
        analysisPath: The folder where the anbalysis will be stored.
        downloadPath: The folder where the downloaded extension will be stored.
        tmpPath: The folder where unzipped files will be created.

    Returns:
    --------
        An Extension object.
    """
    if validations.isURI(uri):
        try:
            u =  HTTPResource(uri)
            data = u.download()
            if data:
                # The name of the extension is formed by:
                #   <source>_<hashed_uri>_<extension_name>
                # Not that the hash is not the hash of the whole extension
                if uri.split("/")[-1] != "":
                    fileName = uri.split("/")[-1]
                else:
                    fileName = "Manual_" + md5.calculateHash(u.uri)
                filePath = os.path.join(downloadPath, fileName)
                if not quiet:
                    print("[*]\tRemote file is being stored as {}…".format(filePath))
                with open(filePath, "wb") as oF:
                    oF.write(data)
        except ConnectionError as e:
            print("[X]\tSomething happened when trying to download the resource. Have we been banned?\n" + str(e))
            return
    else:
        # If it is not a URI, assume that is a local path
        filePath = uri

    return analyseExtensionFromFile(
        filePath,
        tmpPath=tmpPath,
        analysisPath=outputPath,
        quiet=quiet
    )


def main(parsed_args):
    """
    Main function for Neto Analyser.

    Performs an analysis of an extension provided using the command line. The
    details of the parser can be found in the `cli.py` file.

    Params:
    -------
        parsed_args: The parameter options received from the command line parsed
            by the neto CLI parser.

    Returns:
    --------
        An exit value. If 0, successful termination. Whatever else, an error.
    """
    # Create folders
    if not os.path.isdir(parsed_args.analysis_path):
        os.makedirs(parsed_args.analysis_path)

    if not os.path.isdir(parsed_args.download_path):
        os.makedirs(parsed_args.download_path)

    if not os.path.isdir(parsed_args.temporal_path):
        os.makedirs(parsed_args.temporal_path)

    # Perform the process depending on the options provided
    if parsed_args.downloads and os.path.isdir(parsed_args.downloads):
        files = os.listdir(parsed_args.downloads)
        # Order by creation date
        files.sort(key=lambda x: os.path.getmtime(x))

        for i, f in enumerate(files[parsed_args.start:]):
            filePath = os.path.abspath(os.path.join(parsed_args.downloads, f))
            if os.path.isfile(filePath):
                # Extra verification to check if the file name contains a given string
                if not parsed_args.contains_name or parsed_args.contains_name in filePath:
                    print("[*] " + str(i+1+parsed_args.start) + "/"+ str(len(files)) +  "\t(" + str(dt.datetime.now()) + ") Processing: " + filePath)
                    try:
                        ext = analyseExtensionFromFile(
                            filePath,
                            tmpPath=parsed_args.temporal_path,
                            analysisPath=parsed_args.analysis_path,
                            quiet=parsed_args.quiet,
                        )
                    except Exception as e:
                        print("[X]\tSomething happened when processing {s}...".format(s=filePath))
                        print(e)
                        traceback.print_exc()
                        print("[*]\tGoing on with the execution")
    elif parsed_args.uris:
        for i, uri in enumerate(parsed_args.uris):
            print("[*] " + str(i+1+parsed_args.start) + "/"+ str(len(parsed_args.uris)) +  "\t(" + str(dt.datetime.now()) + ") Processing: " + uri)
            ext = analyseExtensionFromURI(
                uri,
                tmpPath=parsed_args.temporal_path,
                analysisPath=parsed_args.analysis_path,
                downloadPath=parsed_args.download_path,
                quiet=parsed_args.quiet
            )
    elif parsed_args.extensions:
        for i, filePath in enumerate(parsed_args.extensions):
            print("[*] " + str(i+1+parsed_args.start) + "/"+ str(len(parsed_args.extensions)) +  "\t(" + str(dt.datetime.now()) + ") Processing: " + filePath)
            ext = analyseExtensionFromFile(
                filePath,
                tmpPath=parsed_args.temporal_path,
                analysisPath=parsed_args.analysis_path,
                quiet=parsed_args.quiet
            )

    if parsed_args.clean:
        print("[*] Cleaning temporal files from '{}'…".format(parsed_args.temporal_path))
        shutil.rmtree(parsed_args.temporal_path)
