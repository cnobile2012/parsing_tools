# -*- coding: utf-8 -*-
#
# tests/test_mimeparser.py
#

import unittest
from decimal import Decimal

from mimeparser import MIMEParser


class TestMIMEParser(unittest.TestCase):

    def __init__(self, name):
        super(TestMIMEParser, self).__init__(name)

    def setUp(self):
        self.mp = MIMEParser()

    #@unittest.skip("Temporarily skipped.")
    def test_parse_mime(self):
        """
        Test that parse_mime() returns the correctly parsed objects.
        """
        mime = 'application/xhtml+xml;q=0.5;ver=1'
        result = self.mp.parse_mime(mime)
        options = ';'.join(["{}={}".format(x, y)
                            for x, y in result[3].items()])
        sep = ';' if options != '' else ''
        found_mime = "{}/{}+{}{}{}".format(
            result[0], result[1], result[2], sep, options)
        msg = "Found mime: {}, should be: {}".format(found_mime, mime)
        self.assertEqual(found_mime, mime, msg)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_mime_quality_domain_errors(self):
        """
        Test that if a q value is below 0 or above 1 that it is coalesced
        to a 1.
        """
        # Test q below 0
        mime = 'application/vnd.example.project.endpoint+json;q=-1'
        result = self.mp.parse_mime(mime)
        quality = result[3].get('q')
        msg = "Found a q of: {}, should be 1, mimetype: {}".format(
            quality, mime)
        self.assertEqual(quality, 1, msg)
        # Test q above 1
        mime = 'application/vnd.example.project.endpoint+json;q=2'
        result = self.mp.parse_mime(mime)
        quality = result[3].get('q')
        msg = "Found a q of: {}, should be 1, mimetype: {}".format(
            quality, mime)
        self.assertEqual(quality, 1, msg)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_mime_quality_non_numeric_errors(self):
        """
        Test that a non-numeric quality value is coalesced to a 1 and that
        a non-quality value is left untouched.
        """
        # Test non-numeric quality value
        mime = 'application/vnd.example.project.endpoint+json;q=no'
        result = self.mp.parse_mime(mime)
        quality = result[3].get('q')
        msg = "Found a q of: {}, should be: 1, mimetype: {}".format(
            quality, mime)
        self.assertEqual(quality, 1, msg)
        # Test non-numeric/non-quality values
        realm = 'localhost'
        mime = 'application/vnd.example.project.endpoint+json;realm='
        result = self.mp.parse_mime(mime + realm)
        found_realm = result[3].get('realm')
        msg = "Found realm: {}, should be: '{}', mimetype: {}".format(
            realm, realm, mime)
        self.assertEqual(found_realm, realm, msg)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_mime_non_standard_mime(self):
        """
        Test that the non-standard * is coalesced to a */* and parsed
        correctly.
        """
        mime = "*"
        result = self.mp.parse_mime(mime)
        type = result[0]
        subtype = result[1]
        msg = "Found type: {}, subtype: {}, should be: *, *".format(
            type, subtype)
        self.assertEqual(type, '*', msg)
        self.assertEqual(subtype, '*', msg)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_mime_use_quotes_in_params(self):
        """
        Test that quotes are allowed in the parameter values.
        """
        # Test the removal of quotes on numeric values
        mime = 'application/vnd.example.project.endpoint+json;q=".9"'
        result = self.mp.parse_mime(mime)
        quality = result[3].get('q')
        msg = ("Found a q of: {}, should be: 0.9, mimetype: {}, "
               "results: {}").format(quality, mime, result)
        self.assertEqual(quality, Decimal('0.9'), msg)
        # Test the removal of quotes on non-numeric values
        mime = 'application/vnd.example.project.endpoint+json;charset="utf-8"'
        result = self.mp.parse_mime(mime)
        charset = result[3].get('charset')
        msg = ("Found a charset of: {}, should be: utf-8, mimetype: {}, "
               "results: {}").format(quality, mime, result)
        self.assertEqual(charset, 'utf-8', msg)

    #@unittest.skip("Temporarily skipped.")
    def test__fitness_and_quality(self):
        """
        Test that the correct mime type was found.
        """
        available_mtypes = [ # Refers to mime types that your system supports
            'text/html',
            'text/plain',
            'text/xml;ver=1;charset=utf-8',
            'application/xml;ver=1',
            'application/json',
            'application/vnd.example.project.endpoint+json',
            ]
        header_mtypes = [ # Refers to mime types coming from an Accept header
            '*/html;q=.2',
            'text/*;q=.4',
            'text/xml;q=.8;ver=1',
            'application/xml;ver=1;charset=utf-8',
            'application/json;q=.7'
            ]
        parsed_mtypes = [self.mp.parse_mime(mt)
                         for mt in ', '.join(header_mtypes).split(',')]
        expected_results = [
            (1010, Decimal('0.4')),
            (1010, Decimal('0.4')),
            (1111, Decimal('0.8')),
            (1111, Decimal('1.0')),
            (1110, Decimal('0.7')),
            (-1, Decimal('0.0')),
            ]
        msg = "Found: {}, should be: {}, mime type: {}"

        for idx, available_mtype in enumerate(available_mtypes):
            available_mtype = self.mp.parse_mime(available_mtype)
            result = self.mp._fitness_and_quality(
                available_mtype, parsed_mtypes)
            self.assertEqual(result, expected_results[idx], msg.format(
                result, expected_results[idx], available_mtype))

    #@unittest.skip("Temporarily skipped.")
    def test_best_match_single_mime_single_mime_list(self):
        """
        Test that a single mimetype is found from a list of one.
        """
        mime = 'application/vnd.example.project.endpoint+json;q=-1'
        available_mtypes = ['application/vnd.example.project.endpoint+json']
        result = self.mp.best_match(available_mtypes, mime)
        msg = "Found mime: {}, should be: {}".format(
            result, available_mtypes[0])
        self.assertEqual(result, available_mtypes[0], msg)

    #@unittest.skip("Temporarily skipped.")
    def test_best_match_single_mime_multiple_mime_list(self):
        """
        Test that a single mimetype is found from a list of multiple mimes.
        """
        mime = 'application/xhtml+xml'
        available_mtypes = ['application/vnd.example.project.endpoint+json',
                            'text/xhtml', 'application/xhtml']
        result = self.mp.best_match(available_mtypes, mime)
        msg = "Found mime: {}, should be: {}".format(
            result, available_mtypes[2])
        self.assertEqual(result, available_mtypes[2], msg)

    #@unittest.skip("Temporarily skipped.")
    def test_best_match_multiple_mimes_multiple_mime_list(self):
        """
        Test that with multiple mimes provided, the best match can be
        found from a multiple mime list.
        """
        mime = 'application/xhtml+xml;q=.9, text/xml;q=.5, text/html;q=.1'
        available_mtypes = ['application/vnd.example.project.endpoint+json',
                            'text/xhtml', 'text/*;q=.3', 'application/json']
        result = self.mp.best_match(available_mtypes, mime)
        msg = "Found mime: {}, should be: {}".format(
            result, available_mtypes[2])
        self.assertEqual(result, available_mtypes[2], msg)

if __name__ == '__main__':
    unittest.main()
