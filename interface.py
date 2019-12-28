# -*- coding: utf-8 -*-
__verson__ = 2.0
__copyright__ = "Yinru Ye(320180940480), Wanfeng Zhu(320180940691),"
"Qiyuan Zhang(320180940541), Haoqiu Yan(320180940440) Copyright 2019"

import tkinter as tk
import time


def show_windows():
    window=tk.Tk()
    window.title("my window")
    window.geometry('500x500')
    entry_var = tk.StringVar()
    entry=tk.Entry(window,textvariable=entry_var,bg="white",font=("a",12),width=15)
    entry.pack()
    return window, entry


def get_entry(entry, self):
    target = entry.get()
    self.condition.acquire()
    self.target.append(target)
    print(self.target)
    self.condition.notify()
    self.condition.release()
    time.sleep(1)


