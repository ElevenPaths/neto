#!/usr/bin/env python
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

# Example based on json-rpc documentation:
#   <https://json-rpc.readthedocs.io/en/latest/quickstart.html>

import os
import sys

from jsonrpc import JSONRPCResponseManager, dispatcher
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

import neto
import neto.lib.crypto.md5 as md5
from neto.lib.extensions import Extension
from neto.downloaders.http import HTTPResource


DOWNLOADS_PATH = "./downloads"

@dispatcher.add_method
def remote(*args):
    """
    Downloads and analyses a remote URI

    To prevent misuse, just the first parameter is processed.

    Args:
    -----
        args: list of remote uris to download
    """
    results = {}
    for i, uri in enumerate(args):
        print(" * {0}/{1} Processing <{2}>...".format(i+1, len(args), uri))
        try:
            data = HTTPResource(uri).download()
        except ConnectionError as e:
            print(" X Something happened when trying to download the resource. Have we been banned?\n<" + str(e) + ">\nRetrying...")

        if data:
            # The name of the extension is formed by:
            #   <source>_<hashed_uri>_<extension_file_name>
            # Note: that the hash is not the hash of the whole extension
            file_name = "jsonrpc_" + md5.calculateHash(uri)
            if len(uri.split("/")[-1]) > 1:
                file_name += "_" + uri.split("/")[-1]
            target_file = os.path.join(
                DOWNLOADS_PATH,
                file_name
            )

            with open(target_file, "wb") as oF:
                oF.write(data)
            print(" * Extension stored as '{0}'...".format(target_file))

            print(" * Analysing the extension at '{0}'...".format(target_file))
            ext = Extension(target_file)
            results[uri] = ext.__dict__
        else:
            print("SAMPASA")
    return results


@dispatcher.add_method
def local(*args):
    """
    Analyses a locally downloaded extension

    Args:
    -----
        args: list of locally downloaded extension files.

    Returns:
    --------
        A dict where the key is the local path and the value is the JSON representation of the analysis.
    """
    results = {}

    for i, localPath in enumerate(args):
        try:
            results[localPath] = Extension(localPath).__dict__
        except Exception as e:
            print(e)

    return results


@dispatcher.add_method
def commands():
    """
    Returns list of possible commands

    Returns:
    --------
        Returns a list of the available commands.
    """
    result = []
    for c in dispatcher.keys():
        result.append(c)
    return result


@dispatcher.add_method
def info():
    """
    Prints Neto's JSONRPC information

    Returns:
    --------
        Returns a list of the available commands.
    """
    return (
        {
            "version": neto.__version__,
            "package": "neto"
        }
    )


@Request.application
def application(request):
    """
    Creates the Wekzeug application.
    """
    # dispatcher is a dictionary {<method_name>: callable}
    # It can also be isntantiated using:
    #   dispatcher["new_method"] = functionName
    response = JSONRPCResponseManager.handle(
        request.data,
        dispatcher
    )
    return Response(
        response.json,
        mimetype='application/json'
    )


def main(parsed_args):
    """
    Main function for Neto server

    Provides an easy WebUI to analyse a given extension

    Params:
    -------
        parsed_args: The parameter options received from the command line parsed
            by the neto CLI parser.

    Returns:
    --------
        An exit value. If 0, successful termination. Whatever else, an error.
    """
    # Check the creation of the intermediate download folder
    if not os.path.isdir(parsed_args.downloads):
        # Create folder
        os.makedirs(parsed_args.downloads)

    # Set global JSON RPC vars
    global DOWNLOADS_PATH
    DOWNLOADS_PATH = parsed_args.downloads

    try:
        run_simple(parsed_args.host, parsed_args.port, application)
    except OSError:
        print(" * It seems that the address '{0}:{1}' is already in use. Try another address or close the other instance.".format(parsed_args.host, parsed_args.port))
        sys.exit(1)
