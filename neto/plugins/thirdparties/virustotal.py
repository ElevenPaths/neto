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

from neto.lib.thirdparties import Thirdparty

class Virustotal(Thirdparty):
    """
    A Virustotal module that wraps external analytical modules.

    The constructor of the parent will be in charge of dealing with the creation
    logic, by setting initial values for the instance and loading the
    corresponding features.

    The methods to be overrrided are defined as follows:
        - buildURI(self, fileID): To construct the uri property based on a
            fileId. To do so automatically without rebuilding this method, the
            string should contain the placemark <FILE_ID>.
        - getFeatures(self, uri=None): To construct the dict that will be
            loaded, most of the times grabbing the information from a remote
            API and process it.

    The serialization of this type of objects will bring a results such as this:

    {
      "_platform": "Virustotal",
      "_date_analysis": "…",
      "_features": {
        …
      },
      "_uri": "https://…",
      "_item": "0123456789abcdef"
    }
    """
    BASE_URL = "https://www.virustotal.com/#/file/<FILE_ID>/details"

    def buildUri(self, extension):
        """
        Abstract method that builds the remote URI for the object

        Args:
        -----
            extension: Remote identifier to be used in the URI.
        """
        return self.BASE_URL.replace("<FILE_ID>", extension.digest["sha256"])

    def getFeatures(self):
        """
        Method that will perform the collection of the new features

        It will be in charge of collecting the new resourcs and shipping the
        data to the self.features local JSON structure.
        """
        return {}
