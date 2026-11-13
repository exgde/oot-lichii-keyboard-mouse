// Native mouse camera: the two entry points the patched game instructions branch to.
// They run in the middle of game functions, so they keep every register the game could be using
// (all general registers the C code may change, all 32 vector registers, the flags) and only
// change the register the replaced instruction was meant to set.

.macro SAVE_ALL
    sub     sp, sp, #(176 + 32*16)
    stp     x0, x1, [sp, #0]
    stp     x2, x3, [sp, #16]
    stp     x4, x5, [sp, #32]
    stp     x6, x7, [sp, #48]
    stp     x8, x9, [sp, #64]
    stp     x10, x11, [sp, #80]
    stp     x12, x13, [sp, #96]
    stp     x14, x15, [sp, #112]
    stp     x16, x17, [sp, #128]
    stp     x18, x30, [sp, #144]
    mrs     x9, nzcv
    str     x9, [sp, #160]
    stp     q0, q1, [sp, #176]
    stp     q2, q3, [sp, #208]
    stp     q4, q5, [sp, #240]
    stp     q6, q7, [sp, #272]
    stp     q8, q9, [sp, #304]
    stp     q10, q11, [sp, #336]
    stp     q12, q13, [sp, #368]
    stp     q14, q15, [sp, #400]
    stp     q16, q17, [sp, #432]
    stp     q18, q19, [sp, #464]
    stp     q20, q21, [sp, #496]
    stp     q22, q23, [sp, #528]
    stp     q24, q25, [sp, #560]
    stp     q26, q27, [sp, #592]
    stp     q28, q29, [sp, #624]
    stp     q30, q31, [sp, #656]
.endm

// restores everything except v0 (the result) when \keep_v0 is 1
.macro RESTORE_ALL keep_v0
    .if \keep_v0
    ldr     q1, [sp, #192]
    .else
    ldp     q0, q1, [sp, #176]
    .endif
    ldp     q2, q3, [sp, #208]
    ldp     q4, q5, [sp, #240]
    ldp     q6, q7, [sp, #272]
    ldp     q8, q9, [sp, #304]
    ldp     q10, q11, [sp, #336]
    ldp     q12, q13, [sp, #368]
    ldp     q14, q15, [sp, #400]
    ldp     q16, q17, [sp, #432]
    ldp     q18, q19, [sp, #464]
    ldp     q20, q21, [sp, #496]
    ldp     q22, q23, [sp, #528]
    ldp     q24, q25, [sp, #560]
    ldp     q26, q27, [sp, #592]
    ldp     q28, q29, [sp, #624]
    ldp     q30, q31, [sp, #656]
    ldr     x9, [sp, #160]
    msr     nzcv, x9
    ldp     x0, x1, [sp, #0]
    ldp     x2, x3, [sp, #16]
    ldp     x4, x5, [sp, #32]
    ldp     x6, x7, [sp, #48]
    ldp     x8, x9, [sp, #64]
    ldp     x10, x11, [sp, #80]
    ldp     x12, x13, [sp, #96]
    ldp     x14, x15, [sp, #112]
    ldp     x16, x17, [sp, #128]
    ldp     x18, x30, [sp, #144]
    add     sp, sp, #(176 + 32*16)
.endm

    .text
    .global oot_hook_rates

// Replaces `str s0, [sp, #12]` at module 0x625370, in the player camera update. There s9 holds this frame's
// yaw change and s0 the pitch change (degrees) computed from the right stick, and s1 = s9*s9 was just computed.
// The mouse is added to both (through their saved copies), then the replaced work is redone.
oot_hook_rates:
    SAVE_ALL
    add     x0, sp, #(176 + 9*16)    // saved v9 (yaw)
    add     x1, sp, #176             // saved v0 (pitch)
    bl      oot_cam_rates
    RESTORE_ALL 0
    fmul    s1, s9, s9
    str     s0, [sp, #12]
    ret
