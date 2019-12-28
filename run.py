# -*- coding: utf-8 -*-
__verson__ = 2.0
__copyright__ = "Yinru Ye(320180940480), Wanfeng Zhu(320180940691),"
"Qiyuan Zhang(320180940541), Haoqiu Yan(320180940440) Copyright 2019"

import threading
import os
import thread


def main():
    target = []
    condition = threading.Condition()
    t_gui = thread.Gui(condition, target)
    t_processor = thread.Processor(condition, target)
    t_gui.start()
    print('run!')
    t_processor.start()
    t_gui.join()
    t_processor.join(2)
    print("Preparation for exiting.")
    os._exit(0)


if __name__ == '__main__':
    main()
