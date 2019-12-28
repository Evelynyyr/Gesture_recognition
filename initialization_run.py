# -*- coding: utf-8 -*-
__verson__ = 2.0
__copyright__ = "Yinru Ye(320180940480), Wanfeng Zhu(320180940691),"
"Qiyuan Zhang(320180940541), Haoqiu Yan(320180940440) Copyright 2019"

import image


# initialization
if __name__ == '__main__':
    f_template = image.Template(r'gestures\f_template.jpg')
    l_template = image.Template(r'gestures\l_template.jpg')
    f_template.creator('f_template')
    l_template.creator('l_template')

