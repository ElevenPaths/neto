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


import os
import json
import timeout_decorator

#@timeout_decorator.timeout(30, timeout_exception=StopIteration)
def runAnalysis(**kwargs):
    """
    Method that runs an analysis

    This method is dinamically loaded by neto.lib.extensions.Extension objects
    to conduct an analysis. The analyst can choose to perform the analysis on
    kwargs["extensionFile"] or on kwargs["unzippedFiles"]. It SHOULD return a
    dictionary with the results of the analysis that will be updated to the
    features property of the Extension.

    Args:
    -----
        kwargs: It currently contain:
            - extensionFile: A string to the local path of the extension.
            - unzippedFiles: A dictionary where the key is the relative path to
                the file and the the value the absolute path to the extension.
                {
                    "manifest.json": "/tmp/extension/manifest.json"
                    …
                }
    Returns:
    --------
        A dictionary where the key is the name given to the analysis and the
            value is the result of the analysis. This result can be of any
            format.
    """
    results = {}

    # Iterate through all the files in the folder
    for f, realPath in kwargs["unzippedFiles"].items():
        if os.path.isfile(realPath):
            # Extract localization
            if f.split(os.sep)[0] == "_locales":
                with open(realPath) as iF:
                    lang = f.split(os.sep)[1].lower()
                    aux = {
                        lang: {}
                    }
                    try:
                        text = iF.read()
                        jText = json.loads(text)
                        # Minor refactor of the strings to put the message in each language as the key
                        for k, translated in jText.items():
                            aux[lang][translated["message"]] = {
                                "description": translated["description"],
                                "placemark": k
                            }
                    except:
                        # If other format was found or the JSON crashes, just keep the lang
                        pass
                    results.update(aux)

    return {"locales": results}
