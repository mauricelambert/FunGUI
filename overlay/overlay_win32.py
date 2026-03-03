import ctypes
from ctypes import wintypes
import math
import time

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

@ctypes.WINFUNCTYPE(
    LRESULT,
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM)
def wndproc(hwnd, msg, wparam, lparam):
    if msg == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0
    return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

def create_window(width, height):
    hInstance = kernel32.GetModuleHandleW(None)

    className = "DragonOverlay"

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
        WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_TOOLWINDOW ,
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

def draw_frame(hwnd, scale):
    width, height = 600, 600

    hdcScreen = user32.GetDC(None)
    if not hdcScreen:
        raise ctypes.WinError()

    hdcMem = gdi32.CreateCompatibleDC(hdcScreen)

    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFO)
    bmi.bmiHeader.biWidth = width
    bmi.bmiHeader.biHeight = -height  # top-down DIB
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = 0  # BI_RGB
    bmi.bmiHeader.biSizeImage = 0

    bits = ctypes.c_void_p()
    hBitmap = gdi32.CreateDIBSection(
        hdcMem,
        ctypes.byref(bmi),
        0,            # DIB_RGB_COLORS
        ctypes.byref(bits),
        None,
        0
    )
    if not hBitmap:
        raise ctypes.WinError()

    gdi32.SelectObject(hdcMem, hBitmap)

    buffer = (ctypes.c_uint32 * (width * height)).from_address(bits.value)

    cx, cy = width // 2, height // 2
    # radius = int(80 * scale)
    radius = int(80 * scale * (0.8 + 0.2 * math.sin(time.time() * 3)))

    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            dist = math.sqrt(dx*dx + dy*dy)

            if dist < radius:
                alpha = int(255 * (1 - dist/radius))
                color = (alpha << 24) | (255 << 16)
                buffer[y * width + x] = color
            else:
                buffer[y * width + x] = 0

            # if dist < radius:
            #     alpha = int(255 * math.exp(-dist**2 / (2*(radius/2)**2)))
            #     color = (alpha << 24) | (255 << 16)  # rouge
            #     buffer[y * width + x] = color
            # else:
            #     buffer[y * width + x] = 0

            # thickness = 5
            # if radius - thickness < dist < radius:
            #     buffer[y * width + x] = (255 << 24) | (255 << 16)
            # elif dist < radius - thickness:
            #     buffer[y * width + x] = (100 << 24) | (255 << 16)
            # else:
            #     buffer[y * width + x] = 0

            # angle = math.atan2(dy, dx)
            # dist_factor = math.cos(5 * angle)
            # if dist < radius * (0.5 + 0.5 * dist_factor):
            #     alpha = int(200 * (1 - dist/radius))
            #     buffer[y * width + x] = (alpha << 24) | (255 << 16)

            # r = 255
            # g = int(255 * dist/radius)
            # b = int(255 * (1 - dist/radius))
            # alpha = int(255 * (1 - dist/radius))
            # buffer[y * width + x] = (alpha << 24) | (r << 16) | (g << 8) | b

    blend = BLENDFUNCTION(AC_SRC_OVER, 0, 255, AC_SRC_ALPHA)

    ptDst = wintypes.POINT(500, 200)
    ptSrc = wintypes.POINT(0, 0)
    size = wintypes.SIZE(width, height)

    user32.UpdateLayeredWindow(
        hwnd,
        hdcScreen,
        ctypes.byref(ptDst),
        ctypes.byref(size),
        hdcMem,
        ctypes.byref(ptSrc),
        0,
        ctypes.byref(blend),
        ULW_ALPHA
    )

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

    scale = 0.2
    while scale < 4.0:
        draw_frame(hwnd, scale)
        message_loop()
        scale *= 1.08
        time.sleep(0.016)

    time.sleep(1)

if __name__ == "__main__":
    main()