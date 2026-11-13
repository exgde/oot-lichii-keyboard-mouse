/* OoT-MouseCapture.exe: the native-camera mouse helper on its own, for people who start the emulator themselves.
   Start it before or after the game; it waits for the game window, works only while the game is in front, and
   quits when the game closes. See mouse_capture.h for what it does. */
#include "mouse_capture.h"

#pragma comment(lib, "kernel32.lib")

static volatile LONG stop_flag = 0;

static void print_status(const wchar_t *msg) {
    SYSTEMTIME t;
    GetLocalTime(&t);
    wprintf(L"[%02d:%02d:%02d] %ls\n", t.wHour, t.wMinute, t.wSecond, msg);
}

static BOOL WINAPI on_console(DWORD type) {
    (void)type;
    InterlockedExchange(&stop_flag, 1);
    mc_release();                        /* closing this window gives the normal mouse settings back */
    return TRUE;
}

int main(void) {
    SetConsoleCtrlHandler(on_console, TRUE);
    setvbuf(stdout, NULL, _IONBF, 0);          /* show each line at once */
    wprintf(L"OOT mouse helper (native mouse camera)\n\n"
            L"Waiting for the game window... Start the game if you have not.\n"
            L"In the game: click the picture once, then press Ctrl+F9 once (it hides the pointer).\n"
            L"Alt+Tab gives the normal mouse back at any time. Close this window to stop.\n\n");
    McFind f = {0, NULL};
    while (!f.top && !stop_flag) {
        EnumWindows(mc_find_top, (LPARAM)&f);
        if (!f.top) Sleep(500);
    }
    if (stop_flag) return 0;
    DWORD pid = 0;
    GetWindowThreadProcessId(f.top, &pid);
    wchar_t title[256] = L"", exe[MAX_PATH] = L"?";
    DWORD n = MAX_PATH;
    HANDLE p = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
    if (p) {
        QueryFullProcessImageNameW(p, 0, exe, &n);
        CloseHandle(p);
    }
    GetWindowTextW(f.top, title, 256);
    wprintf(L"Game found: %ls\n  (%ls)\nThe helper works while the game is in front. Status:\n", title, exe);
    mc_log = print_status;
    mc_run(pid, &stop_flag);
    wprintf(L"Game closed. Mouse settings are back to normal.\n");
    return 0;
}
