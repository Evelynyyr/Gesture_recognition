# -*- coding: utf-8 -*-
__verson__ = 2.0
__copyright__ = "Yinru Ye(320180940480), Wanfeng Zhu(320180940691),"
"Qiyuan Zhang(320180940541), Haoqiu Yan(320180940440) Copyright 2019"

import threading
import cv2
import tkinter as tk
import process
import interface


class Gui(threading.Thread):
    def __init__(self, condition, target):
        super().__init__()
        self.condition = condition
        self.target = target

    def run(self):
        window, entry = interface.show_windows()
        press = tk.Button(window, text="press", width="50",
                          command=lambda: interface.get_entry(entry, self))
        press.pack()
        b_quit = tk.Button(window, text='quit', width=20, command=window.quit)
        b_quit.pack()
        window.mainloop()


class Processor(threading.Thread):
    def __init__(self, condition, target):
        super().__init__()
        self.condition = condition
        self.target = target

    def run(self):
        while True:
            self.condition.acquire()
            while True:
                if self.target:
                    target_img = self.target.pop()
                    print(target_img)
                    processed_img = process.run(target_img)
                    cv2.imshow('result', processed_img)
                    cv2.waitKey(5000)  # Press any key to continue execution
                    cv2.destroyAllWindows()
                    break
                print('condition wait by %s' % self.name)
                self.condition.wait()
            print('condition released by %s' % self.name)
            self.condition.release()
