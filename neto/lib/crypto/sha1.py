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
    h = hashlib.sha1()
    if data.__class__.__name__ == "bytes":
        h.update(data)
    else:
        h.update(data.encode())
    return h.hexdigest()


if __name__ == "__main__":
    print(calculateHash(sys.argv[1]))
