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

from distutils.core import setup
import os
import sys

import neto
import neto.lib.utils as utils

setup(
    name='Neto',
    version=neto.__version__,
    author='ElevenPaths',
    description='A package to perform extension analysis',
    url='https://github.com/elevenpaths/neto',
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
        "werkzeug",
        "configparser"
    ]
)


############################
### Creating other files ###
############################

HERE = os.path.abspath(os.path.dirname(__file__))


paths = utils.getConfigPath()


print("[*] Copying relevant files…")
files_to_copy= {
    paths["appPath"] : [
        os.path.join("config", "general.cfg"),
    ],
    paths["appPathDefaults"] : [
        os.path.join("config", "general.cfg"),
    ],
    paths["appPathPlugins"] : [
        os.path.join("config", "template.py.sample"),
    ],
}

# Iterating through all destinations to write the info
for destiny in files_to_copy.keys():
    # Grabbing each source file to be moved
    for sourceFile in files_to_copy[destiny]:
        fileToMove = os.path.join(HERE,sourceFile)

        cmd = ""
        # Choosing the command depending on the SO
        if sys.platform == 'win32':
            if os.path.isdir(fileToMove):
                cmd = "echo d | xcopy \"" + fileToMove + "\" \"" + destiny + "\" /s /e"
            else:
                cmd = "copy \"" + fileToMove + "\" \"" + destiny + "\""
        elif sys.platform == 'linux2' or sys.platform == 'linux' or sys.platform == 'darwin':
            if not os.geteuid() == 0:
                cmd = "cp -r -- \"" + fileToMove + "\" \"" + destiny + "\""
            else:
                cmd = "sudo cp -r -- \"" + fileToMove + "\" \"" + destiny + "\""
        output = os.popen(cmd).read()
