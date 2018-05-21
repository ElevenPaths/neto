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
import requests

import neto.lib.utils as utils
from neto.lib.thirdparties import ThirdpartyCollector


class Virustotal(ThirdpartyCollector):
    """
    A Virustotal module that wraps external analytical modules.

    The constructor of the parent will be in charge of dealing with the creation
    logic, by setting initial values for the instance and loading the
    corresponding features.

    The method to be overriden are defined as follows:
        - getInfo(self, uri=None): To construct the dict that will be loaded,
            most of the times grabbing the information from a remote
            API and process it.

    The serialization of this type of objects will bring a result such as this:
    {
        "platform": "Virustotal",
        "date_analysis": "…",
        "features": {
            …
        },
    }
    """
    BASE_URL = "https://www.virustotal.com/#/file/<FILE_ID>/details"
    API_KEY = utils.getConfigurationFor("analyser")["virustotal_api_key"]

    def getInfo(self, extension=None):
        """
        Method that will perform the collection of the new features

        It will be in charge of collecting the new resourcs and shipping the
        data to a JSON structure. It will need at least:
        {
            "platform": "my_platform",
            "date_analysis": "…",
            "features": {
                …
            },
        }

        Args:
        -----
            extension: Remote identifier to be used in the URI.
        """
        platformName = self.__class__.__name__.lower()
        results = {platformName: {}}
        results[platformName]["date_analysis"] = str(dt.datetime.utcnow())

        if self.API_KEY:
            params = {
                'apikey': self.API_KEY,
                'resource': extension.digest["sha256"]
            }
            headers = {
              "Accept-Encoding": "gzip, deflate",
              "User-Agent" : "gzip,  Neto | A Browser Extension Analysis Toolkit"
              }
            response = requests.post(
                'https://www.virustotal.com/vtapi/v2/file/report',
                #'https://www.virustotal.com/vtapi/v2/file/rescan',
                params=params
            )
            #results[platformName]["features"] = {}
            if response.json()["response_code"] != 0:
                results[platformName]["features"] = response.json()
                results[platformName]["assesment"] = "{}/{}".format(response.json()["positives"], response.json()["total"])
            else:
                print("[*] Something happened with the Virustotal API: ''.".format(response.json()["verbose_msg"]))

        return results
