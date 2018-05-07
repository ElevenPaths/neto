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
from neto.lib.resources import Resource

class HTTPResource(Resource):
    """
    A class that represents an HTTP resource

    This class will perform the download of an HTTP Resoure
    """
    def __init__(self, u, h=None):
        """
        Constructor

        Args:
        -----
            u: a string containing the URI of the resource.
            h: a dict containing the headers.
        """
        super().__init__(u)
        if not h:
            h = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
                "Accept-Encoding": "gzip, deflate, br",
                "Moz-XPI-Update": "1",
                "Connection": "close"
            }
        self.headers = h

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        """
        Sets the value for the headers.

        Args:
        -----
            value: a dictionary representing the headers to be loaded.

        Raises:
        -------
            ValueError: if the value is a dictionary.
        """
        if validations.isTypeCorrect(value, "dict"):
            self._headers = value

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        """
        Sets the value for the protocol.

        Args:
        -----
            value: a string representing the URI.

        Raises:
        -------
            ValueError: if the value is not a valid URI and if it is not a HTTP or HTTPS one.
        """
        if validations.isURI(value):
            p = value.split("://")[0]
            if p in ["http", "https"]:
                self._protocol = p
            else:
                raise ValueError("The provided URI (" + value + ") does not represent a HTTP or HTTPS protocol.")

    def download(self, type="bytes"):
        """
        Method to download a resource

        This method is a wrapper that will perform the download of a resource.

        Returns:
        --------
            The downloaded contents of the remote resource.
        """
        response = requests.get(
            url=self.uri,
            headers=self.headers
        )
        if response.status_code != 200:
            print(str(response.status_code) + " for " + self.uri)
        return response.content
