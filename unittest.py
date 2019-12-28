import unittest
from image import Image, Template, Target
from process import template_select
"""
DESCRIPTION
    Python unit testing framework, based on Haoqiu Yan's and Yinru Ye's
    Smalltalk testing framework

    This module contains the core framework classes that form the basis of
    specific test cases and suites ()
"""

class TestCase(unittest.TestCase):


    def test_template_select(self):
        Input = r"gestures\f_target.jpg"
        Input_path = Image(Input)
        expect = Template(r'templates\f_template.jpg').image_path
        output = template_select(Input_path).image_path
        self.assertEqual(expect,output)


if __name__ == '__main__':
    unittest.main()