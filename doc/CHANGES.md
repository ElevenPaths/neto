Project Neto's Changelog
========================

Full details of the changes committed with each version.

0.6.0, 2018/05/21 -- Add t

- Add `neto console` as an interactive way of dealing 
with Neto.
- Add some text to the terminal to show some of the data
extracted from the extension. All the data is still 
reachable in the generated JSON file, but the most 
important features are now printed in the terminal.
- Refactor of the extension plugins: they now can be
written to analyse either unzipped extensions or the zipped
files.
- Add Virustotal assesment
- Add a locally stored configuration folder for different OS
- Add to .gitignore output folder

0.5.1, 2018/05/08 -- Add werkzeug dependency

Hotfix to add a dependency for many Python3 users by adding
werkzeug library.

0.5.0, 2018/05/07 -- First public release

Some work has been done to make the usage easier for third 
parties such as providing a sample JSONRPC client written in
Python. Many other bugfixes and code cleaning.

0.4.0, 2018/04/20 -- Stability release

Amongst the changes:
- Inclusion of a JSONRPC daemon
- Merge of each entry_point into a single util (neto) with
different subcommands.
- Standarization of the modules found inside.

0.3.0, 2018/03/15 -- Plugin release

Inclusion of a plugin infrastructe to let analysts perform
custom treatments of whatever they find inside an extension.

0.2.0, 2018/01/30 -- First analytic release

First operative relase including neto-analyser and an 
interface to interact with the analysers within Python.

0.1.0, 2017/12/31 -- Initial release
