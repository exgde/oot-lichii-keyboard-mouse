/* Mouse capture for the "native" mouse camera.

   In native mode the game reads the real mouse (Lichii setting mouse_enabled=true). Lichii gives it the pointer
   position inside the picture, so on its own the camera would stop turning at the edge of the picture.
   While the game window is in front (and the pointer is over the picture) this helper:
     - keeps the pointer near the middle of the picture by moving it back by exactly 512 (or 384) game pixels
       when it gets half of that away. The game patch undoes jumps of exactly that size, so the camera never
       sees them, however fast the mouse moves;
     - turns off Windows "Enhance pointer precision" (mouse acceleration) and sets the pointer speed so that one
       mouse count is one pixel of the game's 1280x720 picture: the camera then follows the hand 1:1, at any
       window size. Both are restored as soon as the game loses focus or closes, and are never written to the
       Windows settings (the next start also restores them if a crash interrupted it).
   It never hides, clips or locks the pointer: Lichii hides it itself once Ctrl+F9 is pressed in the game, and
   Alt+Tab always gives it back. */
#pragma once
#include <windows.h>
#include <wchar.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#pragma comment(lib, "user32.lib")
#pragma comment(lib, "winmm.lib")

typedef struct { DWORD pid; HWND top; } McFind;

/* Is pid an emulator of the Lichii family (lichii, eden, yuzu and their forks)? */
static BOOL mc_is_emulator(DWORD pid) {
    static const wchar_t *names[] = {L"lichii", L"fritchii", L"eden", L"yuzu", L"citron", L"sudachi", L"suyu", L"torzu"};
    wchar_t path[MAX_PATH];
    DWORD n = MAX_PATH;
    BOOL ok = FALSE;
    HANDLE p = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
    if (!p) return FALSE;
    if (QueryFullProcessImageNameW(p, 0, path, &n)) {
        wchar_t *base = wcsrchr(path, L'\\');
        base = base ? base + 1 : path;
        _wcslwr_s(base, wcslen(base) + 1);
        for (int i = 0; i < (int)(sizeof(names) / sizeof(names[0])); i++)
            if (wcsncmp(base, names[i], wcslen(names[i])) == 0) ok = TRUE;
    }
    CloseHandle(p);
    return ok;
}

static BOOL CALLBACK mc_find_top(HWND h, LPARAM lp) {
    McFind *f = (McFind *)lp;
    DWORD pid = 0;
    wchar_t title[512];
    GetWindowThreadProcessId(h, &pid);
    /* the game window: an emulator window whose title has the game's name (it contains "Ocarina") */
    if ((f->pid == 0 || pid == f->pid) && IsWindowVisible(h) && GetWindowTextW(h, title, 512) &&
        wcsstr(title, L"Ocarina") && (f->pid != 0 || mc_is_emulator(pid))) {
        f->top = h;
        return FALSE;
    }
    return TRUE;
}

typedef struct { HWND best; LONG area; } McChild;

static BOOL CALLBACK mc_largest_child(HWND h, LPARAM lp) {
    McChild *c = (McChild *)lp;
    RECT r;
    if (IsWindowVisible(h) && GetWindowRect(h, &r)) {
        LONG a = (r.right - r.left) * (r.bottom - r.top);
        if (a > c->area) { c->area = a; c->best = h; }
    }
    return TRUE;
}

/* ---- the emulator's "Aspect Ratio" setting: the game picture (and the mouse area the game sees) follows it ---- */

/* height / width of the picture; 0 = Stretch (the whole render area). Lichii: 0 16:9, 1 4:3, 2 21:9, 3 16:10, 4 Stretch */
static double mc_aspect = 9.0 / 16.0;
static wchar_t mc_config_dir[MAX_PATH] = L"";   /* Lichii's data folder (has config\qt-config.ini); empty = guess */

static int mc_read_aspect_setting(const wchar_t *ini, int *value) {
    FILE *f = _wfopen(ini, L"r");
    char line[512];
    int found = 0;
    if (!f) return 0;
    while (fgets(line, sizeof(line), f))
        if (strncmp(line, "aspect_ratio=", 13) == 0) { *value = atoi(line + 13); found = 1; }
    fclose(f);
    return found;
}

static int mc_try_folder(const wchar_t *dir, int *value) {
    wchar_t p[MAX_PATH];
    swprintf(p, MAX_PATH, L"%s\\config\\custom\\0400486024DEC000.ini", dir);   /* per-game setting first */
    if (mc_read_aspect_setting(p, value)) return 1;
    swprintf(p, MAX_PATH, L"%s\\config\\qt-config.ini", dir);
    return mc_read_aspect_setting(p, value);
}

/* OoT-MouseCapture.exe sits in Lichii's data folder (the installers put it there); else portable user\ or %APPDATA%\lichii */
static void mc_load_aspect(void) {
    wchar_t dir[MAX_PATH], tmp[MAX_PATH];
    int v = 0, ok = 0;
    if (mc_config_dir[0]) ok = mc_try_folder(mc_config_dir, &v);
    if (!ok && GetModuleFileNameW(NULL, dir, MAX_PATH)) {
        wchar_t *s = wcsrchr(dir, L'\\');
        if (s) *s = 0;
        ok = mc_try_folder(dir, &v);
        if (!ok) { swprintf(tmp, MAX_PATH, L"%s\\user", dir); ok = mc_try_folder(tmp, &v); }
    }
    if (!ok && GetEnvironmentVariableW(L"APPDATA", dir, MAX_PATH)) {
        swprintf(tmp, MAX_PATH, L"%s\\lichii", dir);
        ok = mc_try_folder(tmp, &v);
    }
    static const double aspects[] = {9.0 / 16.0, 3.0 / 4.0, 9.0 / 21.0, 10.0 / 16.0, 0.0};
    mc_aspect = (ok && v >= 0 && v <= 4) ? aspects[v] : 9.0 / 16.0;
}

/* The picture inside the render area, exactly like the emulator lays it out (framebuffer_layout.cpp). */
static void mc_fit_aspect(const RECT *r, double aspect, RECT *out) {
    LONG w = r->right - r->left, h = r->bottom - r->top, pw = w, ph = h;
    if (aspect > 0) {
        if ((double)h / w > aspect) ph = (LONG)(w * aspect + 0.5);   /* window taller than the picture: bars above and below */
        else pw = (LONG)(h / aspect + 0.5);                          /* wider: bars left and right */
    }
    out->left = r->left + (w - pw) / 2;
    out->top = r->top + (h - ph) / 2;
    out->right = out->left + pw;
    out->bottom = out->top + ph;
}

/* Screen rectangle of the game picture: the emulator draws into its largest child window. */
static BOOL mc_picture_rect(HWND top, RECT *out) {
    McChild c = {NULL, 0};
    RECT r, cr;
    EnumChildWindows(top, mc_largest_child, (LPARAM)&c);
    if (!(c.best && GetWindowRect(c.best, &r) && r.right - r.left > 64)) {
        if (!GetClientRect(top, &cr)) return FALSE;
        POINT a = {cr.left, cr.top}, b = {cr.right, cr.bottom};
        ClientToScreen(top, &a);
        ClientToScreen(top, &b);
        SetRect(&r, a.x, a.y, b.x, b.y);
    }
    if (r.right - r.left < 64 || r.bottom - r.top < 36) return FALSE;
    mc_fit_aspect(&r, mc_aspect, out);
    return TRUE;
}

/* Work in real screen pixels, like the emulator (otherwise Windows display scaling of 125 % / 150 % would
   round the positions and the clock-hand jumps would no longer be exact). */
static void mc_dpi_aware(void) {
    HMODULE u = GetModuleHandleW(L"user32.dll");
    typedef BOOL(WINAPI * SetCtx)(HANDLE);
    SetCtx set = u ? (SetCtx)GetProcAddress(u, "SetProcessDpiAwarenessContext") : NULL;
    if (!(set && set((HANDLE)-4))) SetProcessDPIAware();   /* -4 = per-monitor aware v2 */
}

/* ---- Windows pointer speed and acceleration, changed only while the game is in front ---- */

/* Pointer speed 1..20 -> pixels moved per mouse count (acceleration off). */
static const double mc_speed_mult[21] = {0, 1.0 / 32, 1.0 / 16, 1.0 / 8, 2.0 / 8, 3.0 / 8, 4.0 / 8, 5.0 / 8,
                                         6.0 / 8, 7.0 / 8, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0,
                                         3.25, 3.5};

typedef struct { int saved; int speed; int mouse[3]; } McPointer;
static McPointer mc_orig;

static void mc_restore_file(wchar_t *path) {
    wchar_t dir[MAX_PATH];
    if (!GetEnvironmentVariableW(L"LOCALAPPDATA", dir, MAX_PATH)) GetTempPathW(MAX_PATH, dir);
    swprintf(path, MAX_PATH, L"%s\\OoT-MouseCapture-restore.txt", dir);
}

static void mc_pointer_restore(void) {
    wchar_t path[MAX_PATH];
    if (mc_orig.saved) {
        SystemParametersInfoW(SPI_SETMOUSE, 0, mc_orig.mouse, 0);
        SystemParametersInfoW(SPI_SETMOUSESPEED, 0, (PVOID)(INT_PTR)mc_orig.speed, 0);
        mc_orig.saved = 0;
    }
    mc_restore_file(path);
    DeleteFileW(path);
}

/* A previous run that ended without restoring (crash) left its saved values: put them back. */
static void mc_pointer_recover(void) {
    wchar_t path[MAX_PATH];
    mc_restore_file(path);
    FILE *f = _wfopen(path, L"r");
    if (!f) return;
    McPointer p = {0};
    if (fscanf(f, "%d %d %d %d", &p.speed, &p.mouse[0], &p.mouse[1], &p.mouse[2]) == 4 && p.speed >= 1 &&
        p.speed <= 20) {
        SystemParametersInfoW(SPI_SETMOUSE, 0, p.mouse, 0);
        SystemParametersInfoW(SPI_SETMOUSESPEED, 0, (PVOID)(INT_PTR)p.speed, 0);
    }
    fclose(f);
    DeleteFileW(path);
}

static int mc_speed_for(LONG picture_width) {
    double want = (double)picture_width / 1280.0;   /* one count = one pixel of the 1280-wide game picture */
    int best = 10;
    for (int s = 1; s <= 20; s++)
        if (fabs(mc_speed_mult[s] - want) < fabs(mc_speed_mult[best] - want)) best = s;
    return best;
}

static void mc_pointer_apply(LONG picture_width) {
    wchar_t path[MAX_PATH];
    if (!mc_orig.saved) {
        if (!SystemParametersInfoW(SPI_GETMOUSESPEED, 0, &mc_orig.speed, 0) ||
            !SystemParametersInfoW(SPI_GETMOUSE, 0, mc_orig.mouse, 0))
            return;
        mc_restore_file(path);
        FILE *f = _wfopen(path, L"w");
        if (f) {
            fprintf(f, "%d %d %d %d\n", mc_orig.speed, mc_orig.mouse[0], mc_orig.mouse[1], mc_orig.mouse[2]);
            fclose(f);
        }
        mc_orig.saved = 1;
    }
    int noaccel[3] = {mc_orig.mouse[0], mc_orig.mouse[1], 0};
    SystemParametersInfoW(SPI_SETMOUSE, 0, noaccel, 0);   /* last argument 0: not saved to the user's settings */
    SystemParametersInfoW(SPI_SETMOUSESPEED, 0, (PVOID)(INT_PTR)mc_speed_for(picture_width), 0);
}

/* ---- main loop ---- */

#define MC_WRAP_X 512   /* game pixels; must match WRAP_X / WRAP_Y in the game patch (cave.c) */
#define MC_WRAP_Y 384

static volatile LONG mc_active = 0;
static LONG mc_active_width = 0;

static void mc_release(void) {
    if (InterlockedExchange(&mc_active, 0)) mc_pointer_restore();
    mc_active_width = 0;
}

/* Runs until process `pid` exits (pid 0: until `*stop` becomes non-zero). */
static void mc_run(DWORD pid, volatile LONG *stop) {
    HANDLE proc = pid ? OpenProcess(SYNCHRONIZE, FALSE, pid) : NULL;
    if (pid && !proc) return;
    mc_dpi_aware();
    mc_load_aspect();
    mc_pointer_recover();
    timeBeginPeriod(1);
    McFind f = {pid, NULL};
    DWORD last_search = 0;
    for (;;) {
        if (proc && WaitForSingleObject(proc, 0) == WAIT_OBJECT_0) break;
        if (stop && *stop) break;
        DWORD now = GetTickCount();
        if (!f.top || !IsWindow(f.top)) {
            f.top = NULL;
            if (now - last_search > 500) {
                last_search = now;
                EnumWindows(mc_find_top, (LPARAM)&f);
                if (f.top) mc_load_aspect();               /* the game (re)started: read Aspect Ratio again */
            }
        }
        RECT r = {0};
        POINT pt = {0};
        HWND fg = GetForegroundWindow();
        BOOL in_game = f.top && (fg == f.top || GetAncestor(fg, GA_ROOT) == f.top) && !IsIconic(f.top) &&
                       mc_picture_rect(f.top, &r) && GetCursorPos(&pt) && PtInRect(&r, pt);
        if (!in_game) {             /* another window, the menu bar, a second screen: leave the pointer alone */
            mc_release();
            Sleep(f.top ? 20 : 250);
            continue;
        }
        LONG width = r.right - r.left;
        if (!InterlockedExchange(&mc_active, 1) || width != mc_active_width) {
            mc_pointer_apply(width);   /* again when the window changes size */
            mc_active_width = width;
        }
        /* Keep the pointer near the middle like a clock hand: when it is more than half a period away, move it
           back by exactly one period (512 x 384 pixels of the game picture). The game patch undoes any jump of
           that size (see cave.c, WRAP_X / WRAP_Y), so the camera never sees it, at any mouse speed. */
        int cx = (r.left + r.right) / 2, cy = (r.top + r.bottom) / 2;
        int wrap_x = (int)((r.right - r.left) * MC_WRAP_X / 1280.0 + 0.5);
        int wrap_y = (int)((r.bottom - r.top) * MC_WRAP_Y / 720.0 + 0.5);
        int nx = pt.x, ny = pt.y;
        if (nx - cx > wrap_x / 2) nx -= wrap_x; else if (cx - nx > wrap_x / 2) nx += wrap_x;
        if (ny - cy > wrap_y / 2) ny -= wrap_y; else if (cy - ny > wrap_y / 2) ny += wrap_y;
        if (nx != pt.x || ny != pt.y) SetCursorPos(nx, ny);
        Sleep(1);
    }
    mc_release();
    timeEndPeriod(1);
    if (proc) CloseHandle(proc);
}
