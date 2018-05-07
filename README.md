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
neto analysis -e https://yoururl.com/extension-name.xpi
```
The extension will be automatically downloaded and unzipped by default in the system's temporal folder.
After the static analysis is performed, it will generate a Json file that is stored by default in a newly created folder named `output`.


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
