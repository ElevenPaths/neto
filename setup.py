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

import neto
from distutils.core import setup

setup(
    name='Neto',
    version=neto.__version__,
    author='ElevenPaths',
    description='A package to perform extension analysis',
    url='https://github.com/febrezo/neto',
    license='GNU GPLv3+',
    packages=[
        'neto',
        'neto.downloaders',
        'neto.lib',
        'neto.lib.crypto',
        'neto.plugins',
        'neto.plugins.analysis',
        'neto.plugins.thirdparties',
    ],
    entry_points={
        'console_scripts': [
            'neto = neto.cli:main',
        ],
    },
    install_requires=[
        "pyasn1",
        "timeout_decorator",
        "requests",
        "json-rpc",
        "werkzeug"
    ]
)
