************
Python Utils
************

This repository contains multiple small projects each of which may have an
individual pip install associated with it. I see no reason to create different
repositories for each one though different pip installs may be useful.

Current Projects
================

mimeparser
----------

This tool would be used to parse HTTP headers to derive the 'best fit' mime
type. It handles suffix and quality parsing and can be used to find the best
match from an `Accept` header from a list of available mime types.

xml2dict
--------

This tool will parse any XML document into a dict. The dict becomes very
verbose since it will indicate any attributes, elements and namespaces used
in the XML document.

