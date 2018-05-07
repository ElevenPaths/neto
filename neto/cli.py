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

import argparse
import os
import sys
import tempfile
import textwrap

import neto
import neto.analyser
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
be used directly from other Python packages or by means of its WebUI.

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
        description=textwrap.dedent('''  The actions that can be launched are listed as subcommands in this CLI:

    analyser          Performs the analysis of one or several extensions.
    daemon            Starts the JSON RPC daemon.

          ''') + textwrap.fill("Available subcommands are invoked by typing 'neto <SUBCOMMAND>' where '<SUBCOMMAND>' is one of the words listed below. Appending '--help' to the full command will print the help for each one of them."),
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
        '-t', '--temporal',
        metavar='<PATH>',
        default=os.path.join(tempfile.gettempdir(), "neto", "analyser"),
        action='store',
        help='the path where the extensions will be extracted.'
    )
    analyserGroupOther.add_argument(
        '-o', '--output',
        metavar='<PATH>',
        default="output",
        action='store',
        help='the path where the results will be stored.'
    )
    # TODO: Add a flag that would let the analyst to hardcode extra parameters
    analyserGroupOther.add_argument(
        '-j' , '--json',
        action='store',
        default="{}",
        help='a Json that would be added to each analysis in this iteration.'
    )
    analyserGroupOther.add_argument(
        '--clean',
        action='store_true',
        default=False,
        help='removes all temporary files.'
    )
    analyserGroupOther.add_argument(
        '--contains_name',
        action='store',
        default=None,
        help='set a string that SHOULD appear in the name of the file.'
    )
    analyserGroupOther.add_argument(
        '--show',
        action='store_true',
        default=False,
        help='print the results in the terminal.'
    )
    analyserGroupOther.add_argument(
        '--start',
        action='store',
        default=0,
        type=int,
        help='set the start index for the analysis.'
    )
    analyserParser.set_defaults(func=neto.analyser.main)

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
        default=14041,
        required=False
    )
    daemonGroupOptions.add_argument(
        "--host",
        type=str,
        help="Host to be listen on",
        default='localhost',
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
        default=os.path.join(tempfile.gettempdir(), "neto", "downloads"),
        help='the path where the extensions will be downloaded.'
    )
    daemonGroupOptions.add_argument(
        '--analysis',
        action='store',
        default=os.path.join(tempfile.gettempdir(), "neto", "analysis"),
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
