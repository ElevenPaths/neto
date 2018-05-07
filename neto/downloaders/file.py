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

import requests

import neto.lib.validations as validations
from neto.libn.resources import Resource

class FileResource(Resource):
    """
    A class that represents a resource stored locally

    This class will perform the download of a file stored locally and will deal
    with the issues linked to it.
    """
    def __init__(self, u):
        """
        Constructor

        Args:
        -----
            u: a string containing the URI of the resource.
        """
        super().__init__(self, u)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        if validations.isTypeCorrect(value, "dict"):
            self._headers = value

    @protocol.setter
    def protocol(self, value):
        if validations.isURI(value):
            p = value.split("://")[0]
            if p in ["file"]:
                self._protocol = p
            else:
                raise ValueError("The provided URI does not represent a path to a file. The path should start with 'file://'.")

    def download(self):
        """
        Method to download a resource

        This method is a wrapper that will perform the download of a resource.

        Returns:
        --------
            The downloaded contents of the local resource.
        """
        with open(self.uri.split("://")[1]) as iF:
            data = iF.read()
            return data
