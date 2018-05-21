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


import os
import re
import timeout_decorator


REGEXPS = {
    "known_mining_domains": [
        b"coin-?hive.com",
        b"jsecoin.com",
        b"reasedoper.pw",
        b"mataharirama.xyz",
        b"listat.biz",
        b"lmodr.biz",
        b"minecrunch.co",
        b"minetraffic.com",
        b"crypto-loot.com",
        b"2giga.link",
        b"ppoi.org",
        b"coinerra.com",
        b"coin-have.com",
        b"kisshentai.net",
        b"miner.pr0gramm.com",
        b"kiwifarms.net",
        b"anime.reactor.cc",
        b"joyreactor.cc",
        b"kissdoujin.com",
        b"ppoi.org",
        b"minero.pw",
        b"coinnebula.com",
        b"afminer.com",
        b"coinblind.com",
        b"webmine.cz",
        b"monerominer.rocks",
        b"cdn.cloudcoins.co",
        b"coinlab.biz",
        b"papoto.comments",
        b"cookiescript.info",
        b"cookiescriptcdn.pro",
        b"rocks.io",
        b"ad-miner.com",
        b"party-nngvitbizn.now.sh",
        b"cryptoloot.pro",
        b"host.d-ns.ga",
        b"baiduccdn1.com",
        b"jsccnn.com",
        b"jscdndel.com",
        b"nahnoji.cz",
        b"goredirect.party",
        b"cryptobara.com",
        b"kickass.cd",
        b"morningdigit.com",
    ],
    "known_mining_strings": [
        b"miner.start\(",
        b"coinhive.min.js",
        b"authedmine.min.js",
        b"://coin-?hive\.com/lib",
        b"://coin-?hive\.com/captcha",
        b"://.+\.coin-?hive\.com/proxy",
        b"://jsecoin\.com/server",
        b"://.+\.jsecoin\.com/server",
        b"://server\.jsecoin\.com",
        b"://.+\.server\.jsecoin\.com",
        b"://load\.jsecoin\.com",
        b"://.+\.load\.jsecoin\.com",
        b"://static\.reasedoper\.pw",
        b"://mataharirama\.xyz",
        b"://listat\.biz",
        b"://lmodr\.biz",
        b"://minecrunch\.co/web",
        b"://minemytraffic\.com",
        b"://crypto-loot\.com/lib",
        b"://.+\.crypto-loot\.com/proxy",
        b"://.+\.2giga\.link/wproxy",
        b"://.+\.2giga\.link/hive/lib",
        b"://ppoi\.org/lib",
        b"://.+\.ppoi\.org/lib",
        b"://.+\.ppoi\.org/token",
        b"://coinerra\.com/lib",
        b"://coin-have\.com/c",
        b"://kisshentai\.net/Content/js/c-hive\.js",
        b"://miner\.pr0gramm\.com/xmr\.min\.js",
        b"://kiwifarms\.net/js/Jawsh/xmr/xmr\.min\.js",
        b"://anime\.reactor\.cc/js/ch/cryptonight\.wasm",
        b"://joyreactor\.cc/ws/ch",
        b"://kissdoujin\.com/Content/js/c-hive\.js",
        b"://ppoi\.org/lib",
        b"://minero\.pw/miner\.min\.js",
        b"://coinnebula\.com/lib",
        b"://.+\.coinnebula\.com/proxy",
        b"://.+\.afminer\.com/code",
        b"://.+\.coinblind\.com/lib",
        b"://webmine\.cz/miner",
        b"://monerominer\.rocks/scripts/miner\.js",
        b"://monerominer\.rocks/miner\.php",
        b"://cdn\.cloudcoins\.co/javascript/cloudcoins\.min\.js",
        b"://coinlab\.biz/lib/coinlab\.js",
        b"://papoto\.com/lib",
        b"://cookiescript\.info/libs",
        b"://.+\.cookiescript\.info/libs",
        b"://cookiescriptcdn\.pro/libs",
        b"://rocks\.io/assets",
        b"://.+\.rocks\.io/assets",
        b"://.+\.rocks\.io/proxy",
        b"://ad-miner\.com/lib",
        b"://.+\.ad-miner\.com/lib",
        b"://party-nngvitbizn\.now\.sh",
        b"://cryptoloot\.pro/lib",
        b"://.+\.host\.d-ns\.ga",
        b"://.+\.host\.d-ns\.ga",
        b"://.+\.host\.d-ns\.ga",
        b"://baiduccdn1\.com/lib",
        b"://jsccnn\.com/content/vidm\.min\.js",
        b"://jscdndel\.com/content/vidm\.min\.js",
        b"://mine\.nahnoji\.cz",
        b"://mine\.nahnoji\.cz",
        b"://mine\.nahnoji\.cz",
        b"://.+\.goredirect\.party/assets",
        b"://miner\.pr0gramm\.com/pm\.min\.js",
        b"://miner\.cryptobara\.com/client",
        b"://digger\.cryptobara\.com/client",
        b"://digger\.cryptobara\.com",
        b"://kickass\.cd/m\.js",
        b"://.+\.morningdigit\.com",
        b"://.+\.morningdigit\.com",
        b"morningdigit\.com/",
    ]
}

#@timeout_decorator.timeout(30, timeout_exception=StopIteration)
def runAnalysis(**kwargs):
    """
    Method that runs an analysis

    This method is dinamically loaded by neto.lib.extensions.Extension objects
    to conduct an analysis. The analyst can choose to perform the analysis on
    kwargs["extensionFile"] or on kwargs["unzippedFiles"]. It SHOULD return a
    dictionary with the results of the analysis that will be updated to the
    features property of the Extension.

    Args:
    -----
        kwargs: It currently contain:
            - extensionFile: A string to the local path of the extension.
            - unzippedFiles: A dictionary where the key is the relative path to
                the file and the the value the absolute path to the extension.
                {
                    "manifest.json": "/tmp/extension/manifest.json"
                    …
                }
    Returns:
    --------
        A dictionary where the key is the name given to the analysis and the
            value is the result of the analysis. This result can be of any
            format.
    """
    results = {}

    # Iterate through all the files in the folder
    for f, realPath in kwargs["unzippedFiles"].items():
        if os.path.isfile(realPath):
            fileType = f.split(".")[-1].lower()

            allTypes = {}

            # Extract matching strings from text files
            if fileType in ["js", "html", "htm", "css", "txt"]:
                # Read the data
                raw_data = open(realPath, "rb").read()


                # Iterate through all the regexps
                for e, valuesRe in REGEXPS.items():
                    foundExpresions = []
                    for exp in valuesRe:
                        values = re.findall(exp, raw_data)
                        for v in values:
                            # TODO: properly handle:
                            #   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 29: unexpected end of data
                            try:
                                aux = {
                                    "value": v.decode("utf-8"),
                                    "path": f,
                                    "regexp": exp.decode("utf-8")
                                }
                                foundExpresions.append(aux)
                            except:
                                pass

                    if len(foundExpresions) > 0:
                        allTypes[e] = foundExpresions

            if len(allTypes.keys()) > 0:
                results[f] = allTypes

    return {"cryptojacking": results}
