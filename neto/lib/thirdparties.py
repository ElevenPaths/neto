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
import datetime as dt
import json
import os

import neto.lib.validations as validations


class Thirdparty():
    __metaclass__  = abc.ABCMeta

    """
    Thirdparty is an abstract class that wraps external analytical modules

    This class is thought to wrap thirdparty analysis and ship them onto a JSON
    structure. The thirdparties will be neto.lib.thirdparties.Thirdparty
    instances that return a dictionary with the following format when being
    printed.

    The constructor of this abstrac class will be in charge of dealing with the
    creation logic, by setting initial values for the instance and loading the
    corresponding features.

    The methods to be overriden are defined as follows:
        - buildURI(self, fileID): To construct the uri property based on a
            fileId. To do so automatically without rebuilding this method, the
            string should contain the placemark <FILE_ID>.
        - getFeatures(self, uri=None): To construct the dict that will be
            loaded, most of the times grabbing the information from a remote
            API and process it.

    The information is loaded into different properties:
        @platform: the Neto version used to conduct the analysis.
        @date_analysis: the date in which the analysis was performed.
        @features: a dict with other relevant features extracted from the
            extension.
        @item: The id to the item in the thirdparty platform.
        @uri: The remote URI from which the data has been obtained.

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
    platform = None
    date_analysis = None
    features = None
    uri = None
    BASE_URL = "https://example.com/<FILE_ID>"

    def __init__(self, extension=None, date_analysis=None):
        """
        Constructor

        It creates the instance initializing the attributes.

        Args:
        -----
            extension: An extension object to the remote resource.
            date_analysis: The date of the analysis as a string.
        """
        if extension:
            self.uri = self.buildUri(extension)
        else:
            self.uri = None
        self.features = self.getFeatures()
        self.date_analysis = date_analysis
        self.platform = self.__class__.__name__.lower()

    @property
    def date_analysis(self):
        return self._date_analysis

    @date_analysis.setter
    def date_analysis(self, value=None):
        """
        Sets the details of the connection to a queue

        Args:
        -----
            value: A representation of the connection details
        """
        if not value:
            self._date_analysis = str(dt.datetime.now())
        elif validations.isTypeCorrect(value, 'str'):
            self._date_analysis = value

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, value):
        """
        Sets the features

        Args:
        -----
            value: A dictionary representing the extracted features.

        Raises:
        -------
            ValueError: If the value is not a well formed URI.
        """
        if validations.isTypeCorrect(value, 'dict'):
            self._features = value

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, value=None):
        """
        Sets the platform name

        Args:
        -----
            value: A representation of the connection details
        """
        if validations.isTypeCorrect(value, 'str'):
            self._platform = value

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        """
        Sets the URI value

        Args:
        -----
            value: A string representing a URI.
        """
        self._uri = value

    def buildUri(self, extension):
        """
        Abstract method that builds the remote URI for the object

        This method will need to be overriden in each and every inherited class.

        Args:
        -----
            extension: An extension object to the remote resource.
        """
        return None

    @classmethod
    @abc.abstractmethod
    def getFeatures(self):
        """
        Abstract method that will perform the collection of the new features

        It will be in charge of collecting the new resourcs and shipping the
        data to the self.features local JSON structure.
        """
        return {}

    def __str__(self):
        """
        Returns the information of the current object as an idented JSON
        """
        return json.dumps(self.__dict__, indent=2)
