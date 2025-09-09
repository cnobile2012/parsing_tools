*************
Parsing Tools
*************

.. image:: https://img.shields.io/badge/license-MIT-green
   :target: https://en.wikipedia.org/wiki/MIT_License
   :alt: License

.. image:: http://img.shields.io/pypi/v/parsing_tools.svg
    :target: https://pypi.python.org/pypi/parsing_tools
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/parsing_tools.svg
    :target: https://pypi.python.org/pypi/parsing_tools
    :alt: PY Versions

.. image:: https://github.com/cnobile2012/parsing_tools/actions/workflows/main.yml/badge.svg?branch=master
   :target: https://github.com/cnobile2012/parsing_tools/actions/workflows/main.yml
   :alt: Build Status

.. image:: http://img.shields.io/coveralls/cnobile2012/parsing_tools/master.svg?branch=master&dummy=987654321
    :target: https://coveralls.io/github/cnobile2012/parsing_tools?branch=master
    :alt: Test Coverage

.. image:: https://img.shields.io/pypi/dm/parsing_tools.svg
    :target: https://pypi.python.org/pypi/parsing_tools
    :alt: PyPI Downloads

The MIT License (MIT)

This repository contains multiple small projects each of which can be used
separately. There are, at this point, no dependencies between them.

This would be a great package to use when creating your own custom Django
REST Framework renderers and parsers based on custom MIME types.

Current Projects
================

mimeparser
----------

This tool would be used to parse HTTP headers to derive the 'best fit' mime
type. It handles suffix and quality parsing and can be used to find the best
match from an `Accept` header from a list of available mime types.

xml2dict
--------

This tool should be able to parse any XML document into Python objects. The
output will become very verbose since it will include all attributes,
elements and namespaces found in the XML document.
