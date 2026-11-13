/* Native mouse camera: code that runs inside the game (OOT, Switch 2, main build E0F3CCFAF50065AE...).
   Built freestanding for AArch64 and placed in the unused space after the game's code; see build_native_camera_ips.py.

   It reads the mouse through the game's own nn::hid::GetMouseStates (the game already initialises the mouse at boot)
   and turns the movement since the last call into camera angles, one to one: no stick curve, no top speed. */

typedef struct {
    long long sampling_number;
    int x, y;                 /* position in the 1280x720 picture */
    int delta_x, delta_y;
    int wheel_delta_x, wheel_delta_y;
    unsigned buttons;
    unsigned attributes;      /* bit 0: transferable, bit 1: connected (nn::hid::MouseAttribute) */
} MouseState;                 /* 40 bytes, newest entry first */

extern int nn_hid_GetMouseStates(MouseState *out, int count) __asm__("_ZN2nn3hid14GetMouseStatesEPNS0_10MouseStateEi");

/* Settings block. Apply-Settings.ps1 finds the marker in the .ips and writes the two floats:
   degrees per mouse step for yaw and pitch (negative pitch = inverted up/down). */
struct Settings { char marker[8]; float yaw_per_step, pitch_per_step; };
__attribute__((section(".rodata.settings"), used))
const volatile struct Settings oot_mcam_settings = {{'O', 'O', 'T', 'M', 'C', 'A', 'M', '1'},
                                                   0.06f, 0.06f};   /* degrees per step; 0.06 = mouse_sens 5 */

struct State {
    long long last_sampling; int ready; float unused;
    /* diagnostics, readable in guest memory at state + 0x10 (cost: a few stores per frame) */
    unsigned yaw_calls, pitch_calls; int last_n; unsigned last_attributes;   /* calls, calls with movement */
    long long newest_sampling; int last_x, last_y;
};
extern volatile struct State oot_mcam_state;   /* placed in spare game BSS by the linker script */

#define WRAP_X 512   /* must match mouse_capture.h */
#define WRAP_Y 384

static int unwrap(int d, int period) {
    while (d > period / 2) d -= period;
    while (d < -period / 2) d += period;
    return d;
}

/* Mouse movement since the previous call, in degrees (game camera units). Returns 0 when there is none. */
int oot_mouse_delta(float *yaw, float *pitch) {
    MouseState s[16];
    int n = nn_hid_GetMouseStates(s, 16);
    oot_mcam_state.last_n = n;
    if (n > 0) {
        oot_mcam_state.last_attributes = s[0].attributes;
        oot_mcam_state.newest_sampling = s[0].sampling_number;
        oot_mcam_state.last_x = s[0].x;
        oot_mcam_state.last_y = s[0].y;
    }
    *yaw = 0.0f;
    *pitch = 0.0f;
    if (n <= 0 || !(s[0].attributes & 2)) {   /* not connected (Lichii mouse_enabled is off) */
        oot_mcam_state.ready = 0;
        return 0;
    }
    if (!oot_mcam_state.ready) {           /* first sample: only remember where we are */
        oot_mcam_state.last_sampling = s[0].sampling_number;
        oot_mcam_state.ready = 1;
        return 0;
    }
    long long last = oot_mcam_state.last_sampling;
    if (s[n - 1].sampling_number > last + 1) {
        /* the camera did not run for a while (menu, cutscene, loading): drop what the mouse did meanwhile */
        oot_mcam_state.last_sampling = s[0].sampling_number;
        return 0;
    }
    int dx = 0, dy = 0;
    for (int i = n - 1; i >= 0; i--) {     /* oldest to newest */
        if (s[i].sampling_number <= last) continue;
        /* The mouse helper keeps the pointer near the middle of the picture by moving it back exactly
           WRAP_X (or WRAP_Y) game pixels whenever it gets more than half of that from the middle, like a
           clock hand going from 12 to 1. Any jump of about that size is such a move: unwrap it.
           The hand can move up to half of WRAP per sample (every ~8 ms), far beyond any real flick. */
        dx += unwrap(s[i].delta_x, WRAP_X);
        dy += unwrap(s[i].delta_y, WRAP_Y);
    }
    oot_mcam_state.last_sampling = s[0].sampling_number;
    if (dx == 0 && dy == 0) return 0;
    /* Game camera (found by RE, see README): stick right lowers yaw, stick down raises pitch.
       Mouse right / mouse down must do the same. */
    *yaw = -(float)dx * oot_mcam_settings.yaw_per_step;
    *pitch = (float)dy * oot_mcam_settings.pitch_per_step;
    return 1;
}

/* Called by hooks.S each frame in the player camera update (FUN_81199c80, module 0x625370), right after the game
   turned the right stick into this frame's turn: yaw and pitch, in degrees, before it checks whether the camera
   is being turned by hand. Adding the mouse here makes the game take its normal "turned by hand" path, which
   applies both numbers to the camera unchanged (yaw += rate, pitch += rate within the pitch limits). */
void oot_cam_rates(float *yaw_rate, float *pitch_rate) {
    float yaw, pitch;
    oot_mcam_state.yaw_calls++;
    if (!oot_mouse_delta(&yaw, &pitch)) return;
    oot_mcam_state.pitch_calls++;            /* frames that had mouse movement */
    *yaw_rate += yaw;
    *pitch_rate += pitch;
}
