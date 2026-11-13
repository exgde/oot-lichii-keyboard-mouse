/* Test of cave.c on the PC (no game needed): a fake nn::hid::GetMouseStates feeds mouse samples, including the
   mouse helper's clock-hand moves, and checks the camera turn per frame.
     clang -O1 -target x86_64-pc-windows-msvc -fuse-ld=lld test_cave.c cave.c -o test_cave.exe && test_cave.exe
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
typedef struct { long long sampling_number; int x, y, delta_x, delta_y, wy, wx; unsigned buttons, attributes; } MS;
struct State { long long last_sampling; int ready; float unused; unsigned a, b; int c; unsigned d; long long e; int f, g; };
volatile struct State oot_mcam_state;
static MS hist[64]; static int nhist = 0; static long long seq = 100; static int px = 640, py = 360;
static void sample(int x, int y) { MS m = {0}; m.sampling_number = ++seq; m.x = x; m.y = y; m.delta_x = x - px; m.delta_y = y - py; m.attributes = 2; px = x; py = y; hist[nhist++ % 64] = m; }
int nn_hid_GetMouseStates(MS *out, int count) __asm__("_ZN2nn3hid14GetMouseStatesEPNS0_10MouseStateEi");
int nn_hid_GetMouseStates(MS *out, int count) { int n = nhist < count ? nhist : count; for (int i = 0; i < n; i++) out[i] = hist[(nhist - 1 - i) % 64]; return n; }
void oot_cam_rates(float *yaw_rate, float *pitch_rate);
static int fails = 0;
#define K 0.06f
#define NEAR(a, b) (fabsf((a) - (b)) < 1e-3f)
#define CHECK(c, ...) do { if (!(c)) { fails++; printf("FAIL line %d: ", __LINE__); printf(__VA_ARGS__); printf("\n"); } } while (0)
static void frame(float *yaw, float *pitch) { *yaw = 0; *pitch = 0; oot_cam_rates(yaw, pitch); }
/* the hand moves (hx,hy) during one HID sample; the helper (polling every ms) wraps the pointer by one period,
   with a rounding error of `err` pixels, whenever it is more than half a period from the middle */
static int cx = 640, cy = 360;
static void hand(int hx, int hy, int err) {
    int x = px, y = py, steps = 8;
    for (int s = 1; s <= steps; s++) {
        x += hx * s / steps - hx * (s - 1) / steps;
        y += hy * s / steps - hy * (s - 1) / steps;
        if (x - 640 > 256) x -= 512 + err; else if (640 - x > 256) x += 512 + err;
        if (y - 360 > 192) y -= 384 + err; else if (360 - y > 192) y += 384 + err;
    }
    sample(x, y);
}
int main(void) {
    float y, p;
    sample(640, 360);
    frame(&y, &p); CHECK(NEAR(y, 0) && NEAR(p, 0), "first frame only syncs");
    hand(4, 2, 0); hand(3, 1, 0); hand(3, 2, 0);
    frame(&y, &p); CHECK(NEAR(y, -10 * K) && NEAR(p, 5 * K), "slow move: yaw %f pitch %f", y, p);
    frame(&y, &p); CHECK(NEAR(y, 0) && NEAR(p, 0), "idle");
    for (int speed = 20; speed <= 240; speed += 55) {
        for (int err = -1; err <= 1; err++) {
            float total = 0; int hand_total = 0, backwards = 0;
            for (int f = 0; f < 60; f++) {
                hand(speed, speed / 3, err); hand(speed, speed / 3, err); hand_total += 2 * speed;
                frame(&y, &p); total += y; if (y > 0) backwards++;
            }
            float want = -hand_total * K;
            CHECK(backwards == 0, "speed %d err %d: %d frames went backwards", speed, err, backwards);
            CHECK(fabsf(total - want) < fabsf(want) * 0.01f + 1.0f, "speed %d err %d: yaw %f want %f", speed, err, total, want);
        }
    }
    /* direction changes at speed */
    hand(200, 0, 0); frame(&y, &p); CHECK(NEAR(y, -200 * K), "flick right: %f", y);
    hand(-200, 0, 0); frame(&y, &p); CHECK(NEAR(y, 200 * K), "flick left: %f", y);
    hand(0, -150, 0); frame(&y, &p); CHECK(NEAR(p, -150 * K), "flick up: %f", p);
    /* pause longer than 16 samples (menu): dropped */
    for (int k = 0; k < 30; k++) hand(5, 0, 0);
    frame(&y, &p); CHECK(NEAR(y, 0), "after menu: no jump (%f)", y);
    hand(3, 0, 0); frame(&y, &p); CHECK(NEAR(y, -3 * K), "resumes 1:1: %f", y);
    printf(fails ? "%d FAILED\n" : "ALL OK\n", fails);
    return fails;
}
