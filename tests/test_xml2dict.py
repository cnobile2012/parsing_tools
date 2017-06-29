# -*- coding: utf-8 -*-
#
# tests/test_xml2dict.py
#

import io
import unittest
import logging

import defusedxml.ElementTree as ET

from xml2dict import XML2Dict


class TestXML2Dict(unittest.TestCase):
    malformed_xml = '''<?xml version="1.0" encoding="UTF-8" ?>
<root>
  Missing end root tag.
'''

    def __init__(self, name):
        super(TestXML2Dict, self).__init__(name)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_logging_level(self):
        """
        Test that setting the logging level works.
        """
        level = logging.ERROR
        x2d = XML2Dict(level=level)

        with io.open('tests/FATCA-FFILIST-1.0.xsd', 'r') as f:
            # Test with file object
            data = x2d.parse(f)
            log = logging.getLogger()
            found_level = log.getEffectiveLevel()
            msg = "Found level: {}, should be: {}".format(found_level, level)
            self.assertEqual(found_level, level, msg)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_invalid_xml(self):
        """
        Test parsing of invalid XML.
        """
        bad_xml = '''<?xml version="1.0" encoding="UTF-8"?>'''
        x2d = XML2Dict()

        with self.assertRaises(ET.ParseError) as cm:
            data = x2d.parse(bad_xml)

        error = "no element found: line 1, column 38"
        found_error = str(cm.exception)
        msg = "Found error: {}, should be: ()".format(found_error, error)
        self.assertTrue(error in found_error, msg)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_basic_xml(self):
        """
        Test that basic xml parsing works.
        """
        x2d = XML2Dict()

        with io.open('tests/simple.xml', 'r') as f:
            data = x2d.parse(f)
            msg = "data: {}".format(data)
            self.assertTrue(isinstance(data[0].get('attrib'), dict), msg)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_namespaced_xml(self):
        """
        Test that namespaced xml parsing works.
        """
        x2d = XML2Dict()

        with io.open('tests/FATCA-FFILIST-1.0.xsd', 'r') as f:
            # Test with file object
            data = x2d.parse(f)
            msg = "data: {}".format(data)
            self.assertTrue(isinstance(data[0].get('attrib'), dict), msg)
            # Test with string
            f.seek(0)
            data = x2d.parse(f.read())
            msg = "data: {}".format(data)
            self.assertTrue(isinstance(data[0].get('attrib'), dict), msg)
            # Test that namespaces exist in the dict
            ns1 = 'http://www.w3.org/2001/XMLSchema'
            found_ns1 = data[0].get('element', {}).get('nspace')
            msg = "Found namspace: {}, should be: {}".format(found_ns1, ns1)
            self.assertTrue(ns1 in found_ns1, msg)
            ns2 = 'urn:us:gov:treasury:irs:fatcaffilist'
            found_ns2 = data[0].get(
                'children', [])[0].get('children', [])[0].get(
                'children', [])[0].get('children', [])[0].get(
                'element').get('nspace')
            self.assertTrue(ns2 in found_ns2, msg)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_strip_list(self):
        """
        Test that the list can be stripped from the underlying dict.
        """
        x2d = XML2Dict(strip_list=True)

        with io.open('tests/simple.xml', 'r') as f:
            # Test with file object
            data = x2d.parse(f)
            msg = "data: {}".format(data)
            self.assertTrue(isinstance(data, dict), msg)
            self.assertTrue(isinstance(data.get('attrib'), dict), msg)

    #@unittest.skip("Temporarily skipped.")
    def test_parse_exception(self):
        """
        Test that the list can be stripped from the underlying dict.
        """
        x2d = XML2Dict(strip_list=True)

        with self.assertRaises(ET.ParseError) as cm:
            data = x2d.parse(self.malformed_xml)


if __name__ == '__main__':
    unittest.main()
