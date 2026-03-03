//    This package implements fun, creative, and sometimes
//    slightly chaotic GUI experiments. 
//    Copyright (C) 2026  Maurice Lambert

//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.

//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.

//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <https://www.gnu.org/licenses/>.

// "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
// cl /LD overlay.cpp /O2 /MT

// g++ -shared -O2 -static -static-libgcc -static-libstdc++ overlay.cpp -o overlay.dll -lgdiplus -lgdi32 -luser32 -lkernel32
// g++ -shared -O2 -static -static-libgcc -static-libstdc++ overlay.cpp -o overlay.dll -lgdiplus -lgdi32 -luser32 -lkernel32 -Wl,--export-all-symbols

/*
import ctypes
dll = ctypes.WinDLL("overlay.dll")
dll.StartOverlay()
*/

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <objidl.h>
#include <gdiplus.h>
#include <math.h>

#pragma comment(lib, "gdiplus.lib")

using namespace Gdiplus;

#define DLL_EXPORT __declspec(dllexport)

static HWND g_hwnd = NULL;
static ULONG_PTR g_gdiplusToken;

LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    if (msg == WM_DESTROY)
    {
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProc(hwnd, msg, wParam, lParam);
}

HWND CreateOverlayWindow(int width, int height)
{
    WNDCLASSW wc = {0};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = L"ImageOverlay";

    RegisterClassW(&wc);

    HWND hwnd = CreateWindowExW(
        WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
        wc.lpszClassName,
        NULL,
        WS_POPUP,
        300, 200,
        width, height,
        NULL, NULL,
        wc.hInstance,
        NULL
    );

    ShowWindow(hwnd, SW_SHOW);
    return hwnd;
}

void DrawImageScaled(HWND hwnd, const wchar_t* path, float scale)
{
    Bitmap image(path);
    UINT width = (UINT)(image.GetWidth() * scale);
    UINT height = (UINT)(image.GetHeight() * scale);

    HDC hdcScreen = GetDC(NULL);
    HDC hdcMem = CreateCompatibleDC(hdcScreen);

    BITMAPINFO bmi = {0};
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bmi.bmiHeader.biWidth = width;
    bmi.bmiHeader.biHeight = -(LONG)height;
    bmi.bmiHeader.biPlanes = 1;
    bmi.bmiHeader.biBitCount = 32;
    bmi.bmiHeader.biCompression = BI_RGB;

    void* bits = NULL;
    HBITMAP hBitmap = CreateDIBSection(hdcMem, &bmi, DIB_RGB_COLORS, &bits, NULL, 0);
    SelectObject(hdcMem, hBitmap);

    Graphics graphics(hdcMem);
    graphics.SetInterpolationMode(InterpolationModeHighQualityBicubic);
    graphics.DrawImage(&image, 0, 0, width, height);

    POINT ptDst = {500, 200};
    SIZE size = {(LONG)width, (LONG)height};
    POINT ptSrc = {0, 0};

    BLENDFUNCTION blend = {AC_SRC_OVER, 0, 255, AC_SRC_ALPHA};

    UpdateLayeredWindow(
        hwnd,
        hdcScreen,
        &ptDst,
        &size,
        hdcMem,
        &ptSrc,
        0,
        &blend,
        ULW_ALPHA
    );

    DeleteObject(hBitmap);
    DeleteDC(hdcMem);
    ReleaseDC(NULL, hdcScreen);
}

DWORD WINAPI OverlayThread(LPVOID param)
{
    const wchar_t* imagePath = L"test.png";
    float baseScale = 0.5f;
    float t = 0.0f;

    g_hwnd = CreateOverlayWindow(600, 600);

    MSG msg;
    while (t < 20.0f)
    {
        float currentScale = baseScale * (0.8f + 0.2f * fabsf(sinf(t)));

        DrawImageScaled(g_hwnd, imagePath, currentScale);

        while (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }

        Sleep(16);
        t += 0.03f;
    }

    return 0;
}

#ifdef __cplusplus
extern "C" {
#endif

DLL_EXPORT void StartOverlay()
{
    GdiplusStartupInput gdiplusStartupInput;
    GdiplusStartup(&g_gdiplusToken, &gdiplusStartupInput, NULL);

    CreateThread(NULL, 0, OverlayThread, NULL, 0, NULL);
}

#ifdef __cplusplus
}
#endif

BOOL APIENTRY DllMain(HMODULE hModule,
                      DWORD  ul_reason_for_call,
                      LPVOID lpReserved)
{
    if (ul_reason_for_call == DLL_PROCESS_DETACH)
    {
        GdiplusShutdown(g_gdiplusToken);
    }
    return TRUE;

}
