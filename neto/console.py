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


import cmd as cmd
import os
import os.path
import sys
import tempfile

import neto
import neto.analyser as analyser
import neto.lib.extra as extra
import neto.lib.storage as storage
import neto.lib.utils as utils
import neto.lib.validations as validations
from neto.lib.extensions import Extension
from neto.downloaders.http import HTTPResource

class NetoConsoleMain(cmd.Cmd):
    """
    Neto console application to control the different framework utils

    The user can type 'help' at any time to find the available commands included
    in the framework.
    """

    intro = extra.DISCLAIMER

    info  = """
    General information
    ===================

    The Neto Console is a terminal User Interface to interact with the different
    Neto utilities. It includes a set of tools that help the analyst in the task
    of browser extensions analysis.

    To get additional information about the available commands type 'help'."""

    # Appending the self.info data to the headers...
    intro += info

    # Defining the prompt
    prompt = '\nneto > '

    ruler = '='

    knownExtensions = storage.getExtensionList()
    config = {
        "working_directory": "./"
    }
    selectedExtensions = []


    def do_analyse(self, line):
        """
    This command will start an analysis.

    The different inputs are:
        - local. For locally stored paths.
        - remote. For remotely stored extensions.

    Examples:
        analyse local ./example.xpi
        analyse remote https://example.com/example.xpi
        """
        try:
            location, target = line.split(" ", 1)
        except ValueError:
            print("[!] You have to specify the type of target ('local' or 'remote') and the target. Try 'help analyse' to check the available options.\n")
            return

        if location not in ["local", "remote"]:
            print("[!] Not implemented yet. Try 'help analyse' to check the available options.\n")
            return
        else:
            if location == "remote":
                ext = analyser.analyseExtensionFromURI(
                    target,
                    quiet=False
                )
            elif location == "local":
                ext = analyser.analyseExtensionFromFile(
                    os.path.join(self.config["working_directory"], target),
                    quiet=False
                )

            # Update the list of known extensions
            self.knownExtensions = storage.getExtensionList()

    def complete_analyse(self, text, line, begidx, endidx):
        if "analyse local " in line:
            # Auto complete with files in the path
            completions = []
            for f in os.listdir(self.config["working_directory"]):
                fullPath = os.path.join(self.config["working_directory"], f)
                if os.path.isfile(fullPath) and f.startswith(text):
                        completions.append(f)
        else:
            completions = [ f
                for f in [ "local","remote" ] if f.startswith(text.lower())
            ]

        return completions


    def do_delete(self, line):
        """
    This command will list previously performed analysis enumerating them.

    The analyst can choose to select any of the previously analysed
    extensions to work with them in the future.

    Examples:
        delete ALL
        delete SELECTED
        delete sa*
        delete another.xpi
        """
        counter = 0
        # Recover analysed extensions
        if line.upper() == 'ALL':
            print("\nDeleting all analysis…\n")
            for ext in self.knownExtensions:
                if os.path.isfile(ext["analysis_path"]):
                    os.remove(ext["analysis_path"])
                    self.knownExtensions.remove(ext)
                    counter += 1
        elif line.upper() == 'SELECTED':
            print("\nDeleting selected analysis…\n")
            for sel in self.selectedExtensions:
                for ext in self.knownExtensions:
                    if sel == ext["name"] and os.path.isfile(ext["analysis_path"]):
                        os.remove(ext["analysis_path"])
                        self.knownExtensions.remove(ext)
                        self.selectedExtensions.remove(sel)
                        counter += 1
        elif line[-1] == "*":
            extensionNames = []
            for ext in self.knownExtensions:
                if ext["name"].startswith(line[:-1].lower()) and os.path.isfile(ext["analysis_path"]):
                    os.remove(ext["analysis_path"])
                    self.knownExtensions.remove(ext)
                    if ext["name"] in self.selectedExtensions:
                        self.selectedExtensions.remove(ext["name"])
                    counter += 1
        else:
            extensionNames = []
            for ext in self.knownExtensions:
                if ext["name"] == line and os.path.isfile(ext["analysis_path"]):
                    os.remove(ext["analysis_path"])
                    self.knownExtensions.remove(ext)
                    if ext["name"] in self.selectedExtensions:
                        self.selectedExtensions.remove(ext["name"])
                    counter += 1
        print("\nExtensions removed: {}.\n".format(counter))


    def complete_delete(self, text, line, begidx, endidx):
        completions = [ "ALL", "SELECTED" ] + [ e["name"] for e in self.knownExtensions]
        if text:
            completions = [ f
                for f in completions if f.startswith(text)
            ]
        return completions


    def do_deselect(self, line):
        """
    This command deselects an extension. The analyst needs to provide the
    extension name.

    Example:
        deselect sample.xpi"""
        if line == "ALL":
            self.selectedExtensions = []
            print("\nAll the extensions have been unmarked as selected.\n")
        else:
            for ext in self.selectedExtensions:
                if line == ext:
                    self.selectedExtensions.remove(line)
                    print("\nExtension unmarked as selected.\n")
                    return
            print("\nExtension name ('{}') not found.\n".format(line))

    def complete_deselect(self, text, line, begidx, endidx):
        completions = ["ALL"] + self.selectedExtensions
        if text:
            completions = [ f
                for f in self.selectedExtensions if f.startswith(text.lower())
            ]
        return completions


    def do_details(self, line):
        """
    This command will show the details of a given extension.

    The analyst will be able to choose what extension he/she wants to get
    details from. The console will print the basic representation of the object
    as a string.

    Examples:
        details sample.xpi
        """
        for e in self.knownExtensions:
            if line == e["name"]:
                print("\nShowing details of this extension…\n")
                with open(e["analysis_path"], "r") as iF:
                    ext = Extension(jText=iF.read())
                    print(ext)
                    return
        print("\nNo analysis found for '{}'.".format(line))

    def complete_details(self, text, line, begidx, endidx):
        completions = [ e["name"] for e in self.knownExtensions]
        if text:
            return [ name
                for name in completions if name.startswith(text.lower())
            ]
        return completions


    def do_exit(self, line):
        """
    This command will exit the console normally.
        """
        print("\nExiting…\n")
        sys.exit()


    def complete_full_details(self, text, line, begidx, endidx):
        completions = [ e["name"] for e in self.knownExtensions]
        if text:
            return [ name
                for name in completions if name.startswith(text.lower())
            ]
        return completions


    def do_full_details(self, line):
        """
    This command will show the json representation of a given extension.

    The analyst will be able to choose what extension he/she wants to get
    details from and see the whole Json structure of the analysis.

    Examples:
        full_details sample.xpi
        """
        for e in self.knownExtensions:
            if line == e["name"]:
                print("\nShowing the whole JSON for this extension…\n")
                with open(e["analysis_path"], "r") as iF:
                    print(iF.read())
                    print()
                    return
        print("\nNo analysis found for '{}'.".format(line))

    def complete_full_details(self, text, line, begidx, endidx):
        completions = [ e["name"] for e in self.knownExtensions]
        if text:
            return [ name
                for name in completions if name.startswith(text.lower())
            ]
        return completions


    def do_grep(self, line):
        """
    This command will list any extension containing a given text.

    The analyst will be able to make a literal search of any text found inside
    the results thrown by the Neto analyser.

    Examples:
        grep tabs
        """
        matchedExtensions = []
        if self.selectedExtensions:
            for name in self.selectedExtensions:
                for ext in self.knownExtensions:
                    if name == ext["name"]:
                        with open(ext["analysis_path"], "r") as iF:
                            text = iF.read()
                            if line in text:
                                matchedExtensions.append(name)
        else:
            for ext in self.knownExtensions:
                with open(ext["analysis_path"], "r") as iF:
                    text = iF.read()
                    if line in text:
                        matchedExtensions.append(ext["name"])
        print("\nExtensions that contain the text '{}': {}".format(line, len(matchedExtensions)))

        # Print matched extensions name
        for i, name in enumerate(matchedExtensions):
            print("\t- {}".format(name))


    def do_list(self, line):
        """
    This command will list previously performed analysis enumerating them.

    The analyst can choose to select any of the previously analysed
    extensions to work with them in the future.

    Examples:
        list ALL
        list SELECTED
        list sa*
        list another.xpi
        """
        # Recover analysed extensions
        if line == '' or line.upper() == 'ALL':
            extensionNames = [ ext["name"] for ext in self.knownExtensions]
        elif line.upper() == 'SELECTED':
            extensionNames = self.selectedExtensions
        elif line[-1] == "*":
            extensionNames = []
            for ext in self.knownExtensions:
                if ext["name"].startswith(line[:-1].lower()):
                    extensionNames.append(ext["name"])
        else:
            extensionNames = []
            for ext in self.knownExtensions:
                if ext["name"] == line:
                    extensionNames.append(ext["name"])

        print("\nExtensions found matching the query: {}.\n".format(len(extensionNames)))

        # Print analysed extensions
        for i, name in enumerate(extensionNames):
            print("\t[{}] {}".format("x" if name in self.selectedExtensions else " ", name))
        print()

    def complete_list(self, text, line, begidx, endidx):
        completions = [ "ALL", "SELECTED" ] +  [ ext["name"] for ext in self.knownExtensions ]
        if text:
            return [ f
                for f in completions if f.startswith(text)
            ]
        return completions

    '''
    def do_load(self, line):
        """
    This command will load the details of an extension to explore them

    The analyst can choose to select any of the previously analysed
    extensions to work with them in the future.

    Examples:
        load another.xpi
        """
        # Recover analysed extensions
        for ext in self.knownExtensions:
            if ext["name"] == line:
                with open(ext["analysis_path"], "r") as iF:
                    text = iF.read()
                    e = Extension(jText=text)
                    print("\nExtension '{}' loaded.".format(ext["name"]))
                    #TODO. Open a new CMD.loop


    def complete_load(self, text, line, begidx, endidx):
        completions = [ ext["name"] for ext in self.knownExtensions ]
        if text:
            return [ f
                for f in completions if f.startswith(text)
            ]
        return completions
    '''

    def do_select(self, line):
        """
    This command will select an analysis and will let the user interact with the
    Python objects of each extension. The analyst needs to provide the extension
    name.

    Example:
        select sample.xpi"""
        # Iterating through all the extensions
        for ext in self.knownExtensions:
            if line == ext["name"]:
                self.selectedExtensions.append(line)
                print("\nExtension marked as selected.\n")
                return

        if line.endswith("*"):
            added = 0
            for e in self.knownExtensions:
                if e["name"].startswith(line[:-1]):
                    self.selectedExtensions.add(e)
                    added += 1
            print("\nExtensions marked as selected: {}.\n".format(added))
        else:
            print("\nExtension name not found.\n")

    def complete_select(self, text, line, begidx, endidx):
        # Get all the extensions by name
        if text:
            completions = []
            for f in self.knownExtensions:
                if f["name"].startswith(text.lower()):
                    completions.append(f["name"])
        else:
            completions = [ ext["name"] for ext in self.knownExtensions ]
        return completions


    def do_set(self, line):
        """
    This command sets a configuration variable. You can check at any moment of
    the different variables using 'show options'.

    Example:
        set working_directory ./"""
        try:
            option, value = line.split(" ", 2)
            self.config[option] = value
        except ValueError:
            print("[*] Wrong command. To set a configuration option you should use the following syntax: 'set <option> <value>'.\n")
        except KeyError:
            print("[*] Wrong command. '{}' is not a valid configuration option.\n".format(command))

    def complete_set(self, text, line, begidx, endidx):
        completions = self.config.keys()
        if text:
            completions = [ f
                for f in self.config.keys() if f.startswith(text.lower())
            ]
        return completions


    def do_show(self, line):
        """
    Command that shows the general information about Neto like the welcome
    message or the configuration options.

    Examples:
        show info
        show options
        """
        if line == "info":
            print(self.info)
        elif line == "options":
            print("""
    Options
    =======
        working_directory -> it shows the value of the directory where the
            extensions will be searched.

    Values
    ====== """)
            for key, value in self.config.items():
                print("\t{}{}".format(key.ljust(20, " "), value))
        print()

    def complete_show(self, text, line, begidx, endidx):
        completions = [ "info", "options" ]
        if text:
            completions = [ f
                for f in completions if f.startswith(text.lower())
            ]
        return completions


    def do_update(self, line):
        """
    This command performs a manual update of the known extensions.

    This may be needed to be performed manually in somes cases where another
    app or script has performed more analysis.
        """
        previous = len(self.knownExtensions)
        print("\nUpdating the list of known extensions…")
        self.knownExtensions = storage.getExtensionList()
        print("Total number of extensions loaded: {} ({})\n".format(len(self.knownExtensions), len(self.knownExtensions)-previous))


def main(parsed_args):
    """
    Main function that starts the loop

    Params:
    -------
        parsed_args: The parameter options received from the command line parsed
            by the neto CLI parser.
    """
    NetoConsoleMain().cmdloop()


if __name__ == '__main__':
    main()
