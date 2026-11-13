/* OoT-MouseCapture.exe: the native-camera mouse helper on its own, for people who start the emulator themselves.
   Start it before or after the game; it waits for the game window, works only while the game is in front, and
   quits when the game closes. See mouse_capture.h for what it does. */
#include "mouse_capture.h"

#pragma comment(lib, "kernel32.lib")

static volatile LONG stop_flag = 0;

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
    wprintf(L"Game found. The helper works while the game is in front.\n");
    mc_run(pid, &stop_flag);
    wprintf(L"Game closed. Mouse settings are back to normal.\n");
    return 0;
}
