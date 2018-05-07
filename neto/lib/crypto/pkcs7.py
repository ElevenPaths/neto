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
from pyasn1.codec.der.decoder import decode

def getCertificateData(pkcs7_file):
    """
    Gets the data from a PKCS7 File.

    Args:
    -----
        pkcs7_file: It can be either a path or the byte data itself.

    Returns:
    --------
        A string containing the data inside the certificate.
    """
    if type(pkcs7_file).__name__ != "bytes":
        cData = open(pkcs7_file, "rb").read()
    else:
        cData = pkcs7_file
    try:
        cert, rest = decode(cData)
        return str(cert)
    except:
        print("pyasn1.error.PyAsn1Error: Indefinite length encoding not supported by this codec")
        return ""

if __name__ == "__main__":
    print(getCertificateData(sys.argv[1]))
