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

ascii_art = r"""
   /\_/\
  ( o.o )
   > ^ <
"""

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-transparentcolor", "white")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0)
canvas.pack()

text = canvas.create_text(
    WIDTH/2, HEIGHT/2,
    text=ascii_art,
    font=("Courier", 20),
    fill="red"
)

size = 20

def animate():
    global size
    size += 1
    canvas.itemconfig(text, font=("Courier", size))

    x1, y1, x2, y2 = canvas.bbox(text)

    if x1 <= 0 or y1 <= 0 or x2 >= WIDTH or y2 >= HEIGHT:
        root.destroy()
        return

    root.after(30, animate)

animate()

root.mainloop()
