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

import neto.lib.validations as validations

class Resource:
    """
    A class that represents online resources to be grabbed

    Note that its attribute URI can represent any valid URI not only HTTP or
    HTTPS URIs. This way, the collector will be able to address any resource.
    """

    def __init__(self, u):
        """
        Constructor

        Args:
        -----
            u: A string containing the URI of the resource.
        """
        self.uri = u

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        """
        Sets the URI value

        It also calls the appropiate setter to get the appropriate protocol.

        Args:
        -----
            value: A string representing a URI.

        Raises:
        -------
            TypeError: Whenever the value provided is not a string.
            ValueError: If the value is not  a well formed URI.
        """
        if validations.isURI(value):
            self._uri = value
            # We call the protocol setter
            self.protocol = value

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        """
        Sets the protocol

        Args:
        -----
            value: A string representing a URI.

        Raises:
        -------
            ValueError: If the value is not a well formed URI.
        """
        if validations.isURI(value):
            self._protocol = value.split("://")[0]

    def download(self):
        """
        Method to download a resource

        This method is a wrapper that will perform the download of a resource.
        It will be in charge of addressing the download method depending on the
        type of URI provided.

        Returns:
        --------
            The downloaded contents of the resource.
        """
        return None
