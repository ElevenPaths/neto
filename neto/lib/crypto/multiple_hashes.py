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

import sys
import hashlib

import neto.lib.crypto.md5 as md5
import neto.lib.crypto.sha1 as sha1
import neto.lib.crypto.sha256 as sha256


def calculateHash(data):
    """
    A function to calculate several hash

    Args:
    -----
        data: a string or set of bytes containing the data to hash.

    Returns:
    --------
        A dictionary containing several hashes where the key is the type of hash
            and the value is the hexdigest.
    """
    return {
        "md5": md5.calculateHash(data),
        "sha1": sha1.calculateHash(data),
        "sha256": sha256.calculateHash(data),
    }

if __name__ == "__main__":
    print(calculateHash(sys.argv[1]))
