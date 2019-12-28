import unittest
from image import Image, Template, Target
from process import match, run
"""
DESCRIPTION
    Python unit testing framework, based on Haoqiu Yan's and Yinru Ye's
    Smalltalk testing framework

    This module contains the core framework classes that form the basis of
    specific test cases and suites ()
"""

class TestCase(unittest.TestCase):


    def test_skin_recognkiton(self,image_name):
        expect = Image(r"processed\f_skinRecognition.jpg")
        result = Image.skin_recognition(r'gestures\f_template.jpg')
        self.assertEqual(expect, result)


    def test_cr_otsu(self,image_name):
        expetct = r'templates\f.jpg'
        result = Template.cr_otsu(r'gestures\f_template.jpg')
        self.assertEqual(expetct, result)


    def test_descriptor(self,image_path):
        expect = r'templates\f.jpg'
        template_path = r'gestures\f_template.jpg'
        result = Target.descriptor(template_path)
        self.assertEqual(expect,result)

    def test_match(self,template, target, target_skin, flann_fitter):
        expect =1
        self.assertEqual(r"templates\f_template.jpg", r"gestures\f_template.jpg",
                        r"processed\f_skinRecognition.jpg")

    def test_run(target_path):
        self.assertEqual(r"gestures\f_template.jpg",
                         match(best_match, target, target_skin, flan_fitter))
