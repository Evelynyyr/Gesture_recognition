# -*- coding: utf-8 -*-
__verson__ = 2.0
__copyright__ = "Yinru Ye(320180940480), Wanfeng Zhu(320180940691),"
"Qiyuan Zhang(320180940541), Haoqiu Yan(320180940440) Copyright 2019"

import numpy as np
import cv2


class Image(object):
    def __init__(self, image_path):
        self.image_path = image_path
        self.row = cv2.imread(self.image_path).shape[0]
        self.col = cv2.imread(self.image_path).shape[1]
        self.image_skin_path = ''
        self.hash_str = ''

    @property
    def gray_read(self):
        return cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

    @property
    def color_read(self):
        return cv2.imread(self.image_path, cv2.IMREAD_COLOR)

    @property
    def unchanged_read(self):
        return cv2.imread(self.image_path, cv2.IMREAD_UNCHANGED)

    def skin_recognition(self, image_name):
        """YCr component and Otsu threshold segmentation of CrCb color space, using cr_otsu method"""
        print(image_name)
        img = self.color_read
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
        (y, cr, cb) = cv2.split(ycrcb)
        cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
        _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        dst = cv2.bitwise_and(img, img, mask=skin)
        image_skin_path = r"processed\{}_skinRecognition.jpg".format(image_name)
        cv2.imwrite(image_skin_path, dst)
        print("Target image has been saved in", image_skin_path)
        return Image(image_skin_path)

    def hash(self):
        img = cv2.resize(self.color_read, (8, 8), interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        pixel_sum = 0
        for x in range(8):
            for y in range(8):
                pixel_sum = pixel_sum + gray[x, y]
        avg = pixel_sum / 64
        for x in range(8):
            for y in range(8):
                if gray[x, y] > avg:
                    self.hash_str = self.hash_str + '1'
                else:
                    self.hash_str = self.hash_str + '0'
        return self.hash_str


class Template(Image):
    def cr_otsu(self, image_name):
        img = self.color_read
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
        (y, cr, cb) = cv2.split(ycrcb)
        cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
        _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        dst = cv2.bitwise_and(img, img, mask=skin)
        save_location = r'templates\{}.jpg'.format(image_name)
        cv2.imwrite(save_location, dst)
        print("Template has been saved in ", save_location)
        return save_location

    def descriptor(self):
        image = self.gray_read
        sift = cv2.xfeatures2d.SIFT_create()
        key_points, descriptors = sift.detectAndCompute(image, None)
        # Set file name and save feature data to npy file
        descriptor_file = self.image_path.replace(self.image_path.split('.')[-1], "npy")
        np.save(descriptor_file, descriptors)
        print("Descriptors of the template has been saved in", descriptor_file)

    def creator(self, image_name):
        # Building templates (generating pictures and feature files after skin color extraction)
        self.cr_otsu(image_name)
        self.descriptor()


class Target(Image):
    def descriptor(self):
        image = self.gray_read
        sift = cv2.xfeatures2d.SIFT_create()
        key_points, descriptors = sift.detectAndCompute(image, None)
        return key_points, descriptors

    def skin_recognition(self, image_name):
        img = self.color_read
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
        (y, cr, cb) = cv2.split(ycrcb)
        cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
        _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        dst = cv2.bitwise_and(img, img, mask=skin)
        image_skin_path = r"processed\{}_skinRecognition.jpg".format(image_name)
        cv2.imwrite(image_skin_path, dst)
        print("Target image has been saved in", image_skin_path)
        return Target(image_skin_path)

if __name__ == "__main__":
    image = Image(r'gestures\f_target.jpg')
    image.skin_recognition('f_skin')






