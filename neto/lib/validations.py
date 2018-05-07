#!/usr/bin/python3
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

def isTypeCorrect(value, expectedType):
    """
    Function that verifies if a value has the correct type.

    Args:
    -----
        value:  the value to be verified.
        expectedType: the expected type of the previous value.

    Returns:
    --------
        True: depending on whether the function has passed the tests-

    Raises:
    -------
        TypeError: whenever the type has not been set as correct.
    """
    if value.__class__.__name__ == expectedType:
        return True
    else:
        raise TypeError("The value provided for this parameter, '" + str(value) + "', is not of the expected type: '" + str(expectedType) + "'.")


def isURI(value):
    """
    Function that verifies if a given URL is a URI

    Args:
    -----
        value:  the value to be verified.

    Returns:
    --------
        bool: depending on whether the function has passed the tests-

    Raises:
    -------
        ValueError: whenever the string is not a URI.
    """
    if isTypeCorrect(value, 'str'):
        if len(value.split("://")) > 0:
            return True
        else:
            raise ValueError("The value provided for this parameter '" + str(value) + "' is not a valid URI.")
