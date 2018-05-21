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

import abc
import json
import os

import neto.lib.validations as validations


class ThirdpartyCollector():
    __metaclass__  = abc.ABCMeta

    """
    Thirdparty is an abstract class that wraps external analytical modules

    This class is thought to wrap thirdparty analysis and ship them onto a JSON
    structure. The thirdparties will be neto.lib.thirdparties.Thirdparty
    instances that return a dictionary with the following format when being
    printed.

    The constructor of this abstract class will be in charge of dealing with the
    creation logic, by setting initial values for the instance and loading the
    corresponding features.

    The method to be overriden are defined as follows:
        - getInfo(self, uri=None): To construct the dict that will be loaded,
            most of the times grabbing the information from a remote
            API and process it.

    The information is loaded into different properties:
        @platform: the Neto version used to conduct the analysis.
        @date_analysis: the date in which the analysis was performed (UTC).
        @features: a dict with other relevant features extracted from the
            extension.

    The serialization of this type of objects will bring a result such as this:
    {
        "platform": "Virustotal",
        "date_analysis": "…",
        "features": {
            …
        },
    }
    """
    @classmethod
    @abc.abstractmethod
    def getInfo(self, extension=None):
        """
        Abstract method that will perform the collection of the new features

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
            extension: An extension object to the remote resource.
        """
        results = {self.__class__.__name__.lower(): {}}
        return results

    def __str__(self):
        """
        Returns the information of the current object as an idented JSON
        """
        return json.dumps(self.__dict__, indent=2)
