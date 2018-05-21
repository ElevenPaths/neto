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

import configparser as ConfigParser
import importlib
import inspect
import os
import pkgutil
import sys
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


def getAllClassesFromModule(strModule, classesToAvoid=[]):
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
    listAll = []
    packageModule = importlib.import_module(strModule)

    # Iterating through all the module names to grab them
    for _, name, _ in pkgutil.iter_modules(packageModule.__path__):
        moduleName = strModule + "." + name
        # Importing the module
        my_module = importlib.import_module(moduleName)

        # Getting all the classNames.
        classNames = [m[0] for m in inspect.getmembers(my_module, inspect.isclass)]

        # Dinamically grabbing the first class of the module.
        for c in classNames:
            if c not in classesToAvoid:
                MyClass = getattr(my_module, c)
                emptyInstance = MyClass()
                # Adding to the list!
                listAll.append(emptyInstance)
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
    listAll = []

    packageModule = importlib.import_module(strModule)

    for _, name, _ in pkgutil.iter_modules(packageModule.__path__):
        moduleName =  strModule + "." + name
        # Importing the module
        my_module = importlib.import_module(moduleName)
        # Getting all the method names
        methodNames = [m[0] for m in inspect.getmembers(my_module, inspect.isfunction)]

        # Dinamically grabbing only the runnable of the module.
        for m in methodNames:
            if m == "runAnalysis":
                methodObj = getattr(my_module, m)
                listAll.append(methodObj)
                break

    return listAll


def getUserAnalysisMethods():
    """
    Method that recovers ALL the list of functions that will perform the
    analysis…

    Return:
    -------
        Returns a list [] of <callables>.
    """
    userMethods = []

    # Creating the application paths
    paths = utils.getConfigPath()

    newPath = os.path.abspath(paths["appPathPlugins"])

    # Inserting in the System Path
    if not newPath in sys.path:
        sys.path.append(newPath)

    for module in os.listdir(newPath):
        if module[-3:] == '.py':
            current = module.replace('.py', '')
            my_module = __import__(current)

            # Getting all the method names
            methodNames = [m[0] for m in inspect.getmembers(my_module, inspect.isfunction)]

            # Dinamically grabbing only the runnable of the module.
            for m in methodNames:
                if m == "runAnalysis":
                    methodObj = getattr(my_module, m)
                    userMethods.append(methodObj)
                    break

    del newPath

    return userMethods


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


def getConfigPath():
    """
    Auxiliar function to get the configuration paths depending on the system

    Returns:
    --------
        A dictionary with the following keys: appPath, appPathDefaults,
            appPathPlugins.
    """
    paths = {}

    # Returning the path of the configuration folder
    if sys.platform == 'win32':
        applicationPath = os.path.expanduser(os.path.join('~\\', 'ElevenPaths', 'Neto'))
    else:
        applicationPath = os.path.expanduser(os.path.join('~/', '.config', 'ElevenPaths', 'Neto'))

    # Defining additional folders
    paths = {
        "appPath": applicationPath,
        "appPathData": os.path.join(applicationPath, "data"),
        "appPathDataFiles": os.path.join(applicationPath, "data", "files"),
        "appPathDataAnalysis": os.path.join(applicationPath, "data", "analysis"),
        "appPathDefaults": os.path.join(applicationPath, "default"),
        "appPathPlugins": os.path.join(applicationPath, "plugins"),
    }

    # Creating them if they don't exist
    for path in paths.keys():
        if not os.path.exists(paths[path]):
            os.makedirs(paths[path])

    return paths



def getConfigurationFor(util):
    """
    Method that recovers the configuration information about each Neto util

    This method analyses the configuration values stored in Neto's folder and
    recovers the configuration values for a given utility. The result is always
    a dictionary where the key is the name of the property and the value the
    stored value in the configuration file.

    Args:
    -----
        util: Any of the utils that are contained in the framework: analyser,
            console, daemon.
    Returns:
    --------
        A dictionary containing the default configuration.
    """

    VALUES = {}

    # If a api_keys.cfg has not been found, creating it by copying from default
    configPath = os.path.join(getConfigPath()["appPath"], "general.cfg")

    # Checking if the configuration file exists
    if not os.path.exists(configPath):
        # Copy the data from the default folder
        defaultConfigPath = os.path.join(getConfigPath()["appPathDefaults"], "general.cfg")

        try:
            # Recovering default file
            with open(defaultConfigPath) as iF:
                cont = iF.read()
                # Moving its contents as the default values
                with open(configPath, "w") as oF:
                    oF.write(cont)
        except Exception as e:
            print("Error. No configuration file could be found. Please, reinstall Neto to get a new backup copy of this file.");

    # Reading the configuration file
    config = ConfigParser.ConfigParser()
    config.read(configPath)

    # Iterating through all the sections, which contain the platforms
    for section in config.sections():
        incomplete = False
        if section.lower() == util.lower():
            # Iterating through parameters
            for (param, value) in config.items(section):
                VALUES[param] = value
            break

    return VALUES
