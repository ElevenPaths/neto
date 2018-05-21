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

import argparse
import os
import sys
import tempfile
import textwrap

import neto
import neto.analyser
import neto.console
import neto.daemon
import neto.lib.extra as extra
import neto.lib.utils as utils


def main():
    """
    Main function for Neto

    It can deal with several tasks as specified in the application's help.

    Returns:
    --------
        An exit value. If 0, successful termination. Whatever else, an error.
    """
    # ===============
    # Add main parser
    # ===============

    parser = argparse.ArgumentParser(add_help=False)
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.description = textwrap.dedent('''\
Neto | A tool to analyse browser extensions
-------------------------------------------

This package is intended to help security analysts when analysing different
types of browser extensions. Apart from this CLI, the utils in this package can
be used directly from other Python packages or by means of its JSON RPC
interface.

''')
    parser.epilog = textwrap.dedent('''\
  Exit status:
    The CLI will exit with one of the following values:

    0   Successful execution.
    1   Failed executions.
''')

    # ==============
    # Add subparsers
    # ==============

    subparsers = parser.add_subparsers(
        title="Subcommands",
        description=textwrap.dedent('''  Available subcommands are invoked by typing 'neto <SUBCOMMAND>' where '<SUBCOMMAND>' is one of the actions listed below:

    analyser          Performs the analysis of one or several extensions.
    console           Starts an interactive application to conduct the analysis.
    daemon            Starts the JSON RPC daemon.

          ''') + textwrap.fill("Appending '--help' to the full command will print the help for each one of them."),
        dest="subcommand"
    )

    # Analyser parser
    # ---------------
    analyserParser = subparsers.add_parser('analyser')
    analyserParser._optionals.title = "Input options (one required)"

    # Defining the mutually exclusive group for the main options
    analyserGroupMainOptions = analyserParser.add_mutually_exclusive_group(required=True)

    # Adding the main options
    analyserGroupMainOptions.add_argument(
        '-d', '--downloads',
        metavar='<PATH>',
        action='store',
        help='sets the folder that contains the downloaded extensions.'
    )
    analyserGroupMainOptions.add_argument(
        '-e', '--extensions',
        metavar='<PATH>',
        nargs='+',
        action='store',
        help='receives one or several local files and performs the analysis.'
    )
    analyserGroupMainOptions.add_argument(
        '-u', '--uris',
        metavar='<URI>',
        nargs='+',
        action='store',
        help='receives one or several URIs, downloads them and performs the analysis of the extension found there.'
    )

    # Other options
    analyserGroupOther = analyserParser.add_argument_group(
        'Other arguments',
        textwrap.fill('Advanced configuration of the behaviour of the analyser.')
    )
    # Adding optional parameters
    analyserGroupOther.add_argument(
        '--analysis_path',
        metavar='<PATH>',
        default=utils.getConfigPath()["appPathDataAnalysis"],
        action='store',
        help='sets a different path to store the analysis as a Json. Default: {}'.format(utils.getConfigPath()["appPathDataAnalysis"])
    )
    analyserGroupOther.add_argument(
        '--download_path',
        metavar='<PATH>',
        default=utils.getConfigPath()["appPathDataFiles"],
        action='store',
        help='sets a different path to store the downloaded extensions. Default: {}'.format(utils.getConfigPath()["appPathDataFiles"])
    )
    analyserGroupOther.add_argument(
        '--temporal_path',
        metavar='<PATH>',
        default=os.path.join(tempfile.gettempdir(), "neto", "temporal"),
        action='store',
        help='sets the path where the extensions will be extracted. It is recommended to use a temporal path. Default: {}'.format(os.path.join(tempfile.gettempdir(), "neto", "temporal"))
    )
    analyserGroupOther.add_argument(
        '--clean',
        action='store_true',
        default=False,
        help='removes all temporary generated files created in the unzipping process so as to free space.'
    )
    analyserGroupOther.add_argument(
        '--quiet',
        action='store_true',
        default=False,
        help='avoids printing the results in the terminal.'
    )
    analyserGroupOther.add_argument(
        '--start',
        action='store',
        default=0,
        type=int,
        help='sets the start index in case you analyse several files in a folder. This option can be used to relaunch experiments with a big series of files..'
    )
    analyserParser.set_defaults(func=neto.analyser.main)

    # Console parser
    # -------------
    consoleParser = subparsers.add_parser('console')

    # Other options
    consoleGroupOther = consoleParser.add_argument_group(
        'Other arguments',
        textwrap.fill('Advanced configuration of the behaviour of the console UI, including temporal folders and output folders.')
    )
    consoleGroupOther.add_argument(
        '--downloads',
        metavar='<PATH>',
        action='store',
        default=utils.getConfigPath()["appPathDataFiles"],
        help='the path where the extensions will be downloaded.'
    )
    consoleGroupOther.add_argument(
        '--analysis',
        action='store',
        default=utils.getConfigPath()["appPathDataAnalysis"],
        help='sets the analysis folder where the JSON files will be stored.'
    )
    consoleGroupOther.add_argument(
        '--working_directory',
        action='store',
        default=utils.getConfigurationFor("console")["working_directory"] or utils.getConfigPath()["appPathDataAnalysis"],
        help='sets the path where previous analysis are supposed to be. The loaded analysis will be brought from here.'
    )
    consoleParser.set_defaults(func=neto.console.main)

    # Daemon parser
    # -------------
    daemonParser = subparsers.add_parser('daemon')

    # Add the main configuration options for the JSON RPC server
    daemonGroupOptions = daemonParser.add_argument_group(
        'Daemon Options',
        textwrap.fill('Configuring the behaviour of daemon.')
    )

    daemonGroupOptions.add_argument(
        "--port",
        type=int,
        help="Port to listen on",
        default=int(utils.getConfigurationFor("daemon")["port"]) or 14041,
        required=False
    )
    daemonGroupOptions.add_argument(
        "--host",
        type=str,
        help="Host to be listen on",
        default=utils.getConfigurationFor("daemon")["host"] or 'localhost',
    )
    daemonGroupOptions.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='shows debug information.'
    )

    # Other options
    daemonGroupOther = daemonParser.add_argument_group(
        'Other arguments',
        textwrap.fill('Advanced configuration of the behaviour of the downloader, including temporal folders and output folders.')
    )
    daemonGroupOther.add_argument(
        '--downloads',
        metavar='<PATH>',
        action='store',
        default=utils.getConfigPath()["appPathDataFiles"],
        help='the path where the extensions will be downloaded.'
    )
    daemonGroupOptions.add_argument(
        '--analysis',
        action='store',
        default=utils.getConfigPath()["appPathDataAnalysis"],
        help='sets the analysis folder where the JSON files will be stored.'
    )
    daemonParser.set_defaults(func=neto.daemon.main)

    # About options
    # -------------
    groupAbout = parser.add_argument_group(
        'About this package',
        'Get additional information about this package.'
    )
    groupAbout.add_argument(
        '-h', '--help',
        action='help',
        help='shows this help and exits.'
    )
    groupAbout.add_argument(
        '--license',
        action='store_true',
        default=False,
        help='shows the GPLv3+ license and exits.'
    )
    groupAbout.add_argument(
        '--no-banner',
        action='store_true',
        help='avoids printing the initial banner.'
    )
    groupAbout.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + neto.__version__,
        help='shows the version of this package and exits.'
    )


    # =================
    # Process arguments
    # =================
    args = parser.parse_args()

    if not args.no_banner:
        print(extra.banner)

    if args.license:
        utils.showLicense()
    elif args.subcommand:
        args.func(args)
    else:
        parser.print_help()

    sys.exit(0)


if __name__ == "__main__":
    main()
