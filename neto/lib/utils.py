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

import pkgutil
import importlib
import inspect
import tempfile
import zipfile

import neto

LICENSE_URL = "https://www.gnu.org/licenses/gpl-3.0.txt"


def showLicense():
    """
    Method that prints the license if requested.

    It tries to find the license online and manually download it. This method
    only prints its contents in plain text.
    """
    print("Trying to recover the contents of the license...\n")
    try:
        # Grab the license online and print it.
        text = urllib.urlopen(LICENSE_URL).read()
        print("License retrieved from " + LICENSE_URL + ".")
        raw_input("\n\tPress <ENTER> to print it.\n")
        print(text)
    except:
        print("The license could not be downloaded and printed. You should be able to find it here:\n\t" + LICENSE_URL)


def getAllClassesFromModule(strModule):
    """
    Method that get all the classes from a module

    This is intended to dinamically collect all the plugins available from a
    folder. It dinamically grabs the classes of the module.

    The documentantion on how to use the methodObj can be found here:
        https://docs.python.org/3.4/library/inspect.html

    Args:
    -----
        strModule: The module to be loaded as a string.
    """
    all_modules = []
    packageModule = importlib.import_module(strModule)
    for _, name, _ in pkgutil.iter_modules(packageModule.__path__):
        all_modules.append(strModule + "." + name)

    listAll = []

    # Iterating through all the module names to grab them
    for moduleName in all_modules:
        # Importing the module
        my_module = importlib.import_module(moduleName)

        # Getting all the classNames.
        classNames = [m[0] for m in inspect.getmembers(my_module, inspect.isclass) if m[1].__module__ == moduleName]

        # Dinamically grabbing the first class of the module.
        for c in classNames:
            MyClass = getattr(my_module, c)

            # Instantiating the object
            try:
                newInstance = MyClass()
                # Adding to the list!
                listAll.append(newInstance)
            except Exception as e:
                print("Error. Class '" + c + "' could not be loaded properly. Does it need additional parameters in the constructor?")
                print(e)

    return listAll


def getRunnableAnalysisFromModule(strModule):
    """
    Method that get all the runable analysis from a module

    This is intended to dinamically collect all the plugins available from a
    folder. It dinamically grabs the methods found in the module.

    The documentantion on how to use the methodObj can be found here:
        https://docs.python.org/3.4/library/inspect.html

    Args:
    -----
        strModule: The module to be loaded as a string.
    """
    all_modules = []
    packageModule = importlib.import_module(strModule)
    for _, name, _ in pkgutil.iter_modules(packageModule.__path__):
        all_modules.append(strModule + "." + name)

    listAll = []

    # Iterating through all the module names to grab them
    for moduleName in all_modules:
        # Importing the module
        my_module = importlib.import_module(moduleName)
        # Getting all the classNames.
        methodNames = [m[0] for m in inspect.getmembers(my_module, inspect.isfunction) if m[1].__module__ == moduleName]

        # Dinamically grabbing the first class of the module.
        for m in methodNames:
            methodObj = getattr(my_module, m)
            listAll.append(methodObj)

    return listAll


def unzipFile(lPath, tFolder):
    """
    Method that unzips a file

    Args:
    -----
        lPath: the local path of the zipped file.
        tFolder: the path where the unzipped files will be stored.

    Returns:
    --------
        A list of the tmpFiles found inside the package or None if there was
            a problem when unzipping the extension.

    Raises:
    -------
        zipfile.BadZipFile: if the function is unable of unzipping the
            extension.
    """
    # Unzip the extension file
    zip_ref = zipfile.ZipFile(lPath)
    zip_ref.extractall(tFolder)
    zip_ref.close()

    # Return the list of files
    return zip_ref.namelist()
