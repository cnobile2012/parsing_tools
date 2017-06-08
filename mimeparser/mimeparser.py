# -*- coding: utf-8 -*-
#
# mimeparser/mimeparser.py
#
# See MIT License file.
#
"""
Parse MIME types that are usually found in HTTP headers.

Parsing `Accept` headers correctly has become very important with the
ubiquitus use of RESTful web services because, versioning of the service
is often defined in the mine type.

For reference see the following RFCs:

https://tools.ietf.org/html/rfc4288#section-3.2 (Vendor spec)
https://tools.ietf.org/html/rfc7231#section-5.3.1 (quality spec)
https://tools.ietf.org/html/rfc6839 (Suffix spec)

The basic idea of this code I got from Joe Gregorio,
https://github.com/jcgregorio/mimeparse

Entry point:
 - best_match() -- Primary method to find the mime type that would be
                   needed to find the closest match to the available mime
                   types.
 - parse_mime() -- Returns a parsed mime type into it's parts.
"""
__docformat__ = "restructuredtext en"
__author__ = 'Carl J. Nobile'
__email__ = 'carl.nobile@gmail.com'
__license__ = 'MIT License'
__credits__ = ''

__all__ = ('__docformat__', '__author__', '__email__', '__license__',
           '__credits__', 'MIMEParser',)

from decimal import *


class MIMEParser(object):

    def __init__(self):
        getcontext().prec = 3

    def best_match(self, available_mtypes, header_mtypes):
        """
        Return the best match from `header_mtypes` based on the
        `available_mtypes`.

        mtype is a value driectly from any header where mime types can be
        found. ie. Content-Type, Accept

        Examples:
          >>> best_match(['text/html, application/xbel+xml'],
                  'text/*;q=0.3, text/html;q=0.7, text/html;level=1,'
                  ' text/html;level=2;q=0.4, */*;q=0.5')
          
          >>> best_match(['application/xbel+xml', 'text/xml'],
                         'text/*;q=0.5,*/*; q=0.1')
          'text/xml'
        """
        weighted_matches = []
        pos = 0
        header_mtypes = [self.parse_mime(mt)
                         for mt in header_mtypes.split(',')]

        for mtype in available_mtypes:
            parsed_mtype = self.parse_mime(mtype)
            fit_and_q = self.__fitness_and_quality(parsed_mtype, header_mtypes)
            weighted_matches.append((fit_and_q, pos, mtype))
            pos += 1

        weighted_matches.sort()
        return weighted_matches[-1][0][1] and weighted_matches[-1][2] or ''

    def parse_mime(self, mtype):
        """
        Parses a mime-type into its component parts.

        Works with a single mime type and returns it's component parts in
        a tuple as in (type, subtype, suffix, params), where params is a
        dict of all the optional parameters of the mime type.

        For example, 'application/xhtml+xml;q=0.5;ver=1' would result in:

        ('application', 'xhtml', 'xml', {'q': Decimal(0.5),
                                         'ver': Decimal(1)}
        )

        All numeric values to any parameter are returned as a python
        Decimal object.
        """
        parts = mtype.split(';')
        params = {}

        # Split parameters and convert numeric values to a Decimal object.
        for k, v in [param.split('=', 1) for param in parts[1:]]:
            k = k.strip().lower()
            v = v.strip().lower()

            try:
                v = Decimal(v)
            except InvalidOperation:
                pass

            params[k] = v

        # Add/fix quality values.
        quality = params.get('q')

        if 'q' not in params or quality > Decimal(1) or quality < Decimal(0):
            params['q'] = Decimal(1)

        full_type = parts[0].strip().lower()

        # Fix non-standard single asterisk.
        if full_type == '*':
            full_type = '*/*'

        type, sep, subtype = full_type.partition('/')
        subtype, sep, suffix = subtype.partition('+')
        return type.strip(), subtype.strip(), suffix.strip(), params

    def __fitness_and_quality(self, preferred_mtype, ranges):
        """
        Find the best match for a pre-parsed preferred_mtype within
        pre-parsed ranges.

        Returns a tuple of the fitness value and the value of the 'q'
        (quality) parameter of the best match, or (-1, 0) if no match was
        found.
        """
        best_fit = -1
        best_fit_q = 0
        (target_type, target_subtype,
         target_suffix, target_params) = preferred_mtype

        for type, subtype, suffix, params in ranges:
            type_match = (type == target_type or type == '*'
                          or target_type == '*')
            subtype_match = (subtype == target_subtype or subtype == '*'
                             or target_subtype == '*')
            suffix_match = (suffix == target_suffix or suffix == ''
                            or not target_suffix)

            if type_match and subtype_match and suffix_match:
                param_matches = sum(
                    [1 for (key, value) in target_params.items()
                     if key != 'q' and key in params
                     and value == params[key]], 0)
                fitness = 1000 if type == target_type else 0
                fitness += 100 if subtype == target_subtype else 0
                fitness += 10 if suffix == target_suffix else 0
                fitness += param_matches

                if fitness > best_fit:
                    best_fit = fitness
                    best_fit_q = params.get('q', 0)

        return best_fit, Decimal(best_fit_q)
