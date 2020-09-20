Project Neto: A Toolkit for Analysing Browser Plugins
=====================================================

Overview
--------

Project Neto is a Python 3 package conceived to analyse and unravel hidden
features of browser plugins and extensions for well-known browsers such as
Firefox and Chrome. It automates the process of unzipping the packaged files to
extract these features from relevant resources in a extension like
`manifest.json`, localization folders or Javascript and HTML source files.

Installation
------------

To install the package, the user can choose `pip3`.
```
pip3 install -e . --user
```

Optionally, it can also be installed with administrator privileges using `sudo`:
```
sudo pip3 install -e .
```

A successfull installation can be checked using:
```
python3 -c "import neto; print(neto.__version__)"
```

Quick Start
-----------

To perform the analysis of an extension, the analyst can type the following:
```
neto analyser -u https://yoururl.com/extension-name.xpi
```
The extension will be automatically downloaded and unzipped by default in the system's temporal folder.

However, the analyst can also launch de analysis towards a locally stored extension:
```
neto analyser -e ./my-extension-name.xpi
```

After the static analysis is performed, it will generate a Json file that is stored by default in a newly created folder named `output`.

If you use Python, you can also import the package as a library in your own Python modules:
```
>>> from neto.lib.extensions import Extension
>>> my_extension = Extension ("./sample.xpi")
>>> my_extension.filename
'adblock_for_firefox-3.8.0-an+fx.xpi'
>>> my_extension.digest
'849ec142a8203da194a73e773bda287fe0e830e4ea59b501002ee05121b85a2b'
```

Apart from accesing to the elements found in the extension using properties, the 
analyst can always have access to it as a dictionary:
```
>>> my_extension.__dict__
{'_analyser_version': '0.0.1', '_digest': '849ec142a8203da194a73e773bda287fe0e830e4ea59b501002ee05121b85a2b'…
```

If you are not using Python, you can use the JSON RPC daemon:
```
$ neto daemon

         ____            _           _      _   _      _
        |  _ \ _ __ ___ (_) ___  ___| |_   | \ | | ___| |_ ___
        | |_) | '__/ _ \| |/ _ \/ __| __|  |  \| |/ _ \ __/ _ \ 
        |  __/| | | (_) | |  __/ (__| |_   | |\  |  __/ || (_) |
        |_|   |_|  \___// |\___|\___|\__|  |_| \_|\___|\__\___/
                      |__/

                                    Developed by @ElevenPaths
                                    Version: 0.5.0b


 * Running on http://localhost:14041/ (Press CTRL+C to quit)
```
You can then run commands using your preferred JSON RPC library to write a client 
(we have written a short demo in the `bin` folder) or even `curl`:
```
 curl --data-binary '{"id":0, "method":"remote", "params":["https://example.com/myextension.xpi"], "jsonrpc": "2.0"}'  -H 'content-type:text/json;' http://localhost:14041
```

Features
--------

The following is a non-exhaustive list of the features included in this package are the following:
- Manifest analysis.
- Internal file hashing.
- Entities extraction using regular expressions: IPv4, email, cryptocurrency addresses, URL, etc.
- Comments extraction from HTML, CSS and JS files.
- Cryptojacking detection engine based on known mining domains and expressions.
- Suspicious Javascript code detection such as `eval()`.
- Certificate analysis if provided.
- Batch analysis of previously downloaded extensions.
