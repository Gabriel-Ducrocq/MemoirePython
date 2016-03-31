#!/usr/bin/env python
#-*- coding: utf-8 -*-

from GUI import Cadre
import os
import Tkinter as tk




if __name__ == '__main__':

    if not os.path.exists("data/account"):
        os.makedirs("data/account")

    root = tk.Tk()
    root.wm_title("Léonie")
    app = Cadre(root)
    root.mainloop()