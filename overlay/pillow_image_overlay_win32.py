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

from PIL import Image
import ctypes
from ctypes import wintypes
import time, math

kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

WS_EX_TOOLWINDOW = 0x80
WS_EX_LAYERED = 0x80000
WS_EX_TOPMOST = 0x8
WS_POPUP = 0x80000000

ULW_ALPHA = 0x2
AC_SRC_OVER = 0x0
AC_SRC_ALPHA = 0x1
WM_DESTROY = 0x0002

if ctypes.sizeof(ctypes.c_void_p) == 8:
    LRESULT = ctypes.c_longlong
else:
    LRESULT = ctypes.c_long

user32.DefWindowProcW.restype = LRESULT
user32.DefWindowProcW.argtypes = (
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
)

class WNDCLASS(ctypes.Structure):
    _fields_ = [
        ("style", ctypes.c_uint),
        ("lpfnWndProc", ctypes.WINFUNCTYPE(
            LRESULT,
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            wintypes.LPARAM)),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HICON),
        ("hCursor", wintypes.HCURSOR),
        ("hbrBackground", wintypes.HBRUSH),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]

class BLENDFUNCTION(ctypes.Structure):
    _fields_ = [
        ("BlendOp", ctypes.c_byte),
        ("BlendFlags", ctypes.c_byte),
        ("SourceConstantAlpha", ctypes.c_byte),
        ("AlphaFormat", ctypes.c_byte)
    ]

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", wintypes.LONG),
        ("biHeight", wintypes.LONG),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", wintypes.LONG),
        ("biYPelsPerMeter", wintypes.LONG),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER),
        ("bmiColors", wintypes.DWORD * 3),
    ]

@ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
def wndproc(hwnd, msg, wparam, lparam):
    if msg == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0
    return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

def create_window(width, height):
    hInstance = kernel32.GetModuleHandleW(None)
    className = "ImageOverlay"

    wndclass = WNDCLASS()
    wndclass.style = 0
    wndclass.lpfnWndProc = wndproc
    wndclass.cbClsExtra = 0
    wndclass.cbWndExtra = 0
    wndclass.hInstance = hInstance
    wndclass.hIcon = None
    wndclass.hCursor = None
    wndclass.hbrBackground = None
    wndclass.lpszMenuName = None
    wndclass.lpszClassName = className

    user32.RegisterClassW(ctypes.byref(wndclass))

    hwnd = user32.CreateWindowExW(
        WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
        className,
        None,
        WS_POPUP,
        300, 200,
        width, height,
        None, None,
        hInstance,
        None
    )

    user32.ShowWindow(hwnd, 1)
    return hwnd

def draw_image(hwnd, image_path, scale=1.0):
    img = Image.open(image_path).convert("RGBA")
    width, height = int(img.width * scale), int(img.height * scale)
    try:
        img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
    except:
        img_resized = img.resize((width, height), Image.ANTIALIAS)
    pixels = img_resized.load()

    hdcScreen = user32.GetDC(None)
    hdcMem = gdi32.CreateCompatibleDC(hdcScreen)

    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFO)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height  # top-down
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = 0
    bmi.bmiHeader.biSizeImage = 0

    bits = ctypes.c_void_p()
    hBitmap = gdi32.CreateDIBSection(hdcMem, ctypes.byref(bmi), 0, ctypes.byref(bits), None, 0)
    gdi32.SelectObject(hdcMem, hBitmap)

    buffer = (ctypes.c_uint32 * (width * height)).from_address(bits.value)

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            buffer[y * width + x] = (a << 24) | (r << 16) | (g << 8) | b

    blend = BLENDFUNCTION(AC_SRC_OVER, 0, 255, AC_SRC_ALPHA)
    ptDst = wintypes.POINT(500, 200)
    ptSrc = wintypes.POINT(0, 0)
    size = wintypes.SIZE(width, height)

    user32.UpdateLayeredWindow(hwnd, hdcScreen, ctypes.byref(ptDst),
                               ctypes.byref(size), hdcMem, ctypes.byref(ptSrc),
                               0, ctypes.byref(blend), ULW_ALPHA)

    gdi32.DeleteObject(hBitmap)
    gdi32.DeleteDC(hdcMem)
    user32.ReleaseDC(None, hdcScreen)

def message_loop():
    msg = wintypes.MSG()
    while user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))

def main():
    hwnd = create_window(600, 600)
    scale = 0.5

    image_path = "test.png"

    t = 0.0
    while t < 20.0:
        current_scale = scale * (0.8 + 0.2 * abs(math.sin(t)))
        draw_image(hwnd, image_path, current_scale)
        message_loop()
        t += 0.03
        time.sleep(0.016)

if __name__ == "__main__":

    main()
