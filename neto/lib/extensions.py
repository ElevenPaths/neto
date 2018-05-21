# -*- coding: utf-8 -*-
#
################################################################################
#
#   Copyright 2017 ElevenPaths
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

import datetime as dt
import json
import os
import tempfile
import textwrap

from binascii import unhexlify

import neto
import neto.lib.utils as utils
import neto.lib.crypto.multiple_hashes as hasher
import neto.lib.crypto.pkcs7 as pkcs7
import neto.lib.validations as validations


class Extension:
    """
    A class that represents the features of a given extension.

    The information is loaded into different properties:
        @analyser_version: the Neto version used to conduct the analysis.
        @date_analysis: the date in which the analysis was performed.
        @digest: the hash of the extension.
        @features: a dict with other relevant features extracted from the
            extension.
        @filename: the filename of the extension.
        @files: a dict of the files found inside, where the key is the relative
            path and the value is a dictionary containing the hexdigest of the
            files as MD5, SHA1, and SHA256.
        @manifest: a dict with the manifest values of the extension.
        @manifest_file: a string containing the name of the manifes file.
        @size: the size of the file.
    """

    def __init__(self, lPath=None, tFolder=tempfile.gettempdir(), jText=None):
        """
        Constructor

        Args:
        -----
            lPath: a string containing the local path for the file.
            tFolder: a string representing the folder for the temporal file.
            jText: a string representing the details of the extension as a JSON.

        Raises:
        -------
            ValueError: if neither a lPath or a JSON has been provided ow when
                the JSON string could not be read.
        """
        if lPath:
            self.analyser_version = neto.__version__
            self.date_analysis = dt.datetime.utcnow()
            self.filename = os.path.basename(lPath)
            self.files = None
            self.type = self.__class__.__name__
            self.manifest = None
            self.manifest_file = None
            self.size = None

            # Hashing the file
            with open(lPath, "rb") as iF:
                data = iF.read()
                self.digest = hasher.calculateHash(data)
            # Trying to unzip the folder
            tmpFolder = os.path.join(tFolder, self.digest["md5"])

            tmpFiles = utils.unzipFile(lPath, tmpFolder)
            if tmpFiles:
                # Create auxiliar structure for the found files
                workingPaths = Extension.getWorkingPaths(tmpFolder, tmpFiles)

                # Set the manifest_file
                for m in ["manifest.json", "package.json"]:
                    if m in workingPaths:
                        self.manifest_file = m
                        self.manifest = Extension.readManifest(os.path.join(tmpFolder, self.manifest_file))
                        break
                    else:
                        self.manifest = None
                        self.manifest_file = None

                # Set the hashes for the files
                self.files = Extension.hashFiles(workingPaths)

                # Set the features for the file
                self.features = Extension.analyse(unzippedFiles=workingPaths, extensionFile=lPath)

                # Get third parties links
                self.getThirdparties()
        elif jText:
            try:
                aux = json.loads(jText)
                for key, value in aux.items():
                    setattr(self, key[1:], value)
            except json.decoder.JSONDecodeError:
                raise ValueError("Something happened when loading the data from a JSON in Extension.__init__. " + str(e))
        else:
            raise ValueError("Extension.__init__ requires either lPath and tFolder or jText to create an Extension class.")

    @property
    def analyser_version(self):
        return self._analyser_version

    @analyser_version.setter
    def analyser_version(self, value):
        """
        Sets the value of the analyser version

        Args:
        -----
            value: a string representing the current version of the analyser.

        Raises:
        -------
            TypeError: whenever the value provided is not a string.
        """
        if validations.isTypeCorrect(value, 'str'):
            self._analyser_version = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        """
        Sets the value of the analyser version

        Args:
        -----
            value: a string representing the current object.
        """
        self._type = value

    @property
    def date_analysis(self):
        return self._date_analysis

    @date_analysis.setter
    def date_analysis(self, value):
        """
        Sets the value of the analysis date

        It receives a Datetime object and converts it to a string. If the object
        provided is not a date, it gets the current date with `utcnow()`.

        Args:
        -----
            value: a datetime object with the date.
        """
        try:
            if validations.isTypeCorrect(value, 'datetime'):
                self._date_analysis = str(value) + " UTC"
        except TypeError as e:
            self._date_analysis = str(dt.datetime.utcnow()) + "UTC"

    @property
    def digest(self):
        return self._digest

    @digest.setter
    def digest(self, value):
        """
        Sets the value of the hash

        Args:
        -----
            value: a dictionary representing the digests as MD5, SHA1 & SHA256.
                {
                    "md5": "…",
                    "sha1": "…",
                    "sha256": "…",
                }

        Raises:
        -------
            TypeError: whenever the value provided is not a dict.
        """
        if value is None or validations.isTypeCorrect(value, 'dict'):
            self._digest = value

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, value):
        """
        Sets the value of the features dict

        Args:
        -----
            value: a dict representing the features extracted.

        Raises:
        -------
            TypeError: whenever the value provided is not a dictionary.
        """
        if value is None or validations.isTypeCorrect(value, 'dict'):
            self._features = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        """
        Sets the filename value

        Args:
        -----
            value: a string representing the filename.

        Raises:
        -------
            TypeError: whenever the value provided is not a string.
        """
        if value is None or validations.isTypeCorrect(value, 'str'):
            self._filename = value

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        """
        Sets the value of the dictionary of files found inside

        Args:
        -----
            value: a dictionary representing the files found inside the
                extension, where the key is the relative path and the value is
                the hash of that given file.

        Raises:
        -------
            TypeError: whenever the value provided is not a dictionary.
        """
        if value is None or validations.isTypeCorrect(value, 'dict'):
            self._files = value

    @property
    def manifest(self):
        return self._manifest

    @manifest.setter
    def manifest(self, value):
        """
        Sets the value of the manifest dict

        Args:
        -----
            value: a dict representing the data extracted from the manifest.

        Raises:
        -------
            TypeError: whenever the value provided is not a dictionary.
        """
        if value is None or validations.isTypeCorrect(value, 'dict'):
            self._manifest = value

    @property
    def manifest_file(self):
        return self._manifest_file

    @manifest_file.setter
    def manifest_file(self, value):
        """
        Sets the value of the hash

        Args:
        -----
            value: a string representing the name of the manifest_file.

        Raises:
        -------
            TypeError: whenever the value provided is not a string.
        """
        if value is None or validations.isTypeCorrect(value, 'str'):
            self._manifest_file = value

    @property
    def manifest_file(self):
        return self._manifest_file

    @manifest_file.setter
    def manifest_file(self, value):
        """
        Sets the value of the hash

        Args:
        -----
            value: a string representing the name of the manifest_file.

        Raises:
        -------
            TypeError: whenever the value provided is not a string.
        """
        if value is None or validations.isTypeCorrect(value, 'str'):
            self._manifest_file = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        """
        Sets the size of the extension

        Args:
        -----
            value: an integer representing the number of bytes of the extension.

        Raises:
        -------
            TypeError: whenever the value provided is not an integer.
        """
        if value is None or validations.isTypeCorrect(value, 'int'):
            self._size = value

    def _loadJSON(self, data):
        """
        Private method that converts a JSON string into an Extension object

        Raises:
        -------
            TypeError: if the parameter read from a variabledoes not match the
                appropiate type expected for such property.
            ValueError: if neither a lPath or a JSON has been provided ow when
                the JSON string could not be read.
        """
        try:
            tmp = json.loads(jText)
        except json.decoder.JSONDecodeError:
            raise ValueError("Something happened when loading the data from a JSON in Extension.__init__. " + str(e))

        for key, value in tmp:
            # Setting the properties read from the JSON file
            if key == "_analyser_version":
                self.analyser_version = value
            elif key == "_date_analysis":
                self.date_analysis = value
            elif key == "_digest":
                self.digest = value
            elif key == "_features":
                self.features = value
            elif key == "_filename":
                self.features = value
            elif key == "_files":
                self.files = value
            elif key == "_manifest":
                self.manifest = value
            elif key == "_manifest_file":
                self.manifest_file = value
            elif key == "_size":
                self.size = value
            elif key == "_type":
                self.type = value
            else:
                pass

    @classmethod
    def readManifest(self, tmpFile):
        """
        Method that loads a manifest

        This method is a class method that can be invoked without instantiating
        an object of the class.

        Args:
        ----
            tmpFile: a string that represents the local path to the manifest
            file.

        Returns:
        --------
            A dictionary with the values of the manifest.
        """
        # Set the manifest
        with open(tmpFile) as iF:
            # Analysed line by line to remove comments in JSON files
            lines = iF.readlines()
            text = ""
            for l in lines:
                if not l.lstrip().startswith('//'):
                    text += l
            # TODO: Grab this exception
            # json.decoder.JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
            try:
                return json.loads(text)
            except Exception as e:
                print(str(e) + ": Something happenned when loading the manifest file.")
                return None

    @classmethod
    def getWorkingPaths(self, tmpFolder,  tmpFiles):
        """
        Method that builds a dictionary with the working path for the files

        Args:
        -----
            tmpFolder: the list of files of an extension to be analysed.
            tmpFiles: the list of files of an extension to be analysed.

        Returns:
        ---------
            A dictionary of valid paths towards the files to analyse. The key
            is the relative path inside the extension while the value is the
            real path where the information is stored.
                {
                     "manifest.json": "/tmp/extension/manifest.json"
                     …
                }
        """
        # Set the @files property, including the hashes
        workingPaths = {}

        # The key is the temporal path, while the value is the name of the file
        for f in tmpFiles:
            tmpPath = os.path.join(tmpFolder, f)

            if os.path.isfile(tmpPath):
                # Prepare the data to extract entities
                workingPaths[f] = tmpPath

        return workingPaths

    @classmethod
    def hashFiles(self, tmpFiles):
        """
        Method that hashes the files found in a folder

        Args:
        -----
            tmpFolder: the list of files of an extension to be analysed.
            tmpFiles: the list of files of an extension to be analysed.

        Returns:
        ---------
            A dictionary of valid paths towards the files to analyse. The key
            is the relative path inside the extension while the value is the
            real path where the information is stored.
                {
                     "manifest.json": {
                         "md5": "…",
                         "sha1": "…",
                         "sha256": "…",
                     }
                     …
                }
        """
        files = {}
        # The key is the temporal path, while the value is the name of the file
        for relativePath, realPath in tmpFiles.items():
            # Calculate the hash
            if os.path.isfile(realPath):
                files[relativePath] = hasher.calculateHash(realPath)

        return files

    @classmethod
    def analyse(self, extensionFile=None, unzippedFiles=None):
        """
        Method that extracts entities from the files found in a folder

        This method is a class method that can be invoked without instantiating
        an object of the class. This object calls to a util function that
        dinamically collects the functions found in the modules available at
        neto.plugins.analysis.

        Args:
        -----
            extensionFile: The path to the extension file without being
                unzipped.
            unzippedFiles: A dictionary of valid paths towards the files to
                analyse. The key is the relative path inside the extension while
                the value is the real path where the information is stored.
                {
                     "manifest.json": "/tmp/extension/manifest.json"
                     …
                }

        Returns:
        --------
            A dictionary containing the extracted entities that will potentially
            be returned to the @features property.
                {
                    "url": [
                        {"value": "http://example.com", "path": "./sample.txt"},
                        {"value": "http://example.com/index.html", "path": "./sample.txt"},
                    ],
                    "email": [
                        {"value": "johndoe@example.com", "path": "./sample.txt"},
                    ],
                    …
                    "certificate_info": {
                        "raw_data": [],
                        "entities": []
                    },
                    "exif_data": {},
                    "locales": {
                        "es": {
                            "Título": {
                                "description": "The title for the extension",
                                "placemark": "appTitle"
                            },
                            …
                        },
                        "en": {
                            "Title": {
                                "description": "The title for the extension",
                                "placemark": "appTitle"
                            },
                            …
                        }
                        …
                    }
                }
        """
        results = {}

        analysisList = utils.getRunnableAnalysisFromModule("neto.plugins.analysis")
        for methodObj in analysisList:
            results.update(methodObj(unzippedFiles=unzippedFiles, extensionFile=extensionFile))

        return results


    def getThirdparties(self):
        """
        Method that gets thirdparties analysis

        It automatically updates the instance's features with a thirdparties
        attribute in the Json. To do so, we will use the ThirdPartyCollector
        classes that will return always a JSON structure.
        """
        results = {}
        results["thirdparties"] = {}

        thirdpartiesList = utils.getAllClassesFromModule("neto.plugins.thirdparties", classesToAvoid=["ThirdpartyCollector"])
        for classObj in thirdpartiesList:
            results["thirdparties"].update(classObj.getInfo(self))

        self.features.update(results)


    def __str__(self):
        return textwrap.dedent("""
Name:               {name}
-----

Version:            {version}
--------

SHA256:             {sha256}
-------

Author:             {author}
-------

Permissions:
------------
{permissions}

Content scripts:
----------------
{content_scripts}

Background:
-----------
{background}

Entities:
---------
{entities}

Assesments:
-----------
    {assesments}
""".format(
                name=getattr(self, "manifest", {}).get("name", "N/A"),
                version=getattr(self, "manifest", {}).get("version", "N/A"),
                sha256=getattr(self, "digest", {}).get("sha256", "N/A"),
                author=getattr(self, "manifest", {}).get("author", "N/A"),
                permissions="\n".join('\t- {}'.format(p) for p in getattr(self, "manifest", {}).get("permissions", [])) if getattr(self, "manifest", {}).get("permissions", []) else "N/A",
                content_scripts=json.dumps(getattr(self, "manifest", {}).get("content_scripts", []), indent=2),
                background=json.dumps(getattr(self, "manifest", {}).get("background", []), indent=2),
                entities=json.dumps(getattr(self, "features", {}).get("entities", {}), indent=2),
                assesments="\n".join('\t- {}: {}'.format(platform, self.features["thirdparties"][platform]["assesment"]) for platform in getattr(self, "features").get("thirdparties", [])) if getattr(self, "features", {}).get("thirdparties", []) else "N/A",
            )
        )
