"""Measurements and strokes of the "Basic Controls" screen of OOT (measured in game).
The controller picture (Controller_Pro1, 1160x680) and the guide-line sheets (ControllerGuide_Pro_00..04, 1555x1511) are drawn
overlapped and centred; the picture is shown magnified 1.12x around the point (777.5, 842) of the line sheet."""
import math

PW, PH = 1160, 680                       # picture texture
SW, SH = 1555, 1511                      # guide-line sheet
S = 1.12                                 # sheet pixels per picture pixel
CX, CY = 777.5, 842.0                    # sheet position of the picture centre (580, 340)

LW = 6          # line width
DOT = 9         # end-dot radius
TICK = 14       # half height of the tick on the text side

# fixed text rows of the game (sheet coordinates) and the label columns
ROWS = dict(zl=336, l=449, minus=562, lstick=670, dpad=1019, zr=335, r=449, plus=559, abxy=715, rstick=1226)
LX, RX = 144, 1410


def to_sheet(p):
    """picture point -> line-sheet point"""
    return ((p[0] - 580) * S + CX, (p[1] - 340) * S + CY)


def line(d, pts):
    d.line(pts, fill=255, width=LW, joint="curve")


def dot(d, p):
    d.ellipse((p[0] - DOT, p[1] - DOT, p[0] + DOT, p[1] + DOT), fill=255)


def tick(d, x, y):
    d.line([(x, y - TICK), (x, y + TICK)], fill=255, width=LW)
