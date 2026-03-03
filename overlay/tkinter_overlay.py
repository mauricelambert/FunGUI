#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implements fun, creative, and sometimes
#    slightly chaotic GUI experiments. 
#    Copyright (C) 2026  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This package implements fun, creative, and sometimes
slightly chaotic GUI experiments.
"""

__version__ = "0.0.1"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = """
This package implements fun, creative, and sometimes
slightly chaotic GUI experiments.
"""
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/FunGUI"

copyright = """
FunGUI  Copyright (C) 2026  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = []
print(copyright)

import tkinter as tk

WIDTH = 600
HEIGHT = 600

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "white")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0)
canvas.pack()

face = canvas.create_oval(200, 200, 400, 400, fill="yellow", outline="")
eye1 = canvas.create_oval(250, 260, 290, 300, fill="black")
eye2 = canvas.create_oval(310, 260, 350, 300, fill="black")
mouth = canvas.create_arc(260, 300, 340, 360, start=180, extent=180, style="chord")

items = [face, eye1, eye2, mouth]

def animate():
    for item in items:
        canvas.scale(item, WIDTH/2, HEIGHT/2, 1.03, 1.03)

    x1, y1, x2, y2 = canvas.bbox(face)

    if x1 <= 0 or y1 <= 0 or x2 >= WIDTH or y2 >= HEIGHT:
        root.destroy()
        return

    root.after(16, animate)

animate()

root.mainloop()
