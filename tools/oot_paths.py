"""Where the tools keep what they extract from YOUR game dump (none of it goes to git).

  OOT_WORK    working folder (default: tools/work)  -> Common.bntx, ZsDic.pack.zs, fonts/, out/, preview/
  OOT_ASSETS  folder of the keyboard and mouse pictures (default: tools/assets; created if missing)
"""
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.environ.get("OOT_WORK") or os.path.join(TOOLS, "work"))
FONTS = os.path.join(WORK, "fonts")
OUT = os.path.join(WORK, "out")
PREVIEW = os.path.join(WORK, "preview")
ASSETS = os.path.abspath(os.environ.get("OOT_ASSETS") or os.path.join(TOOLS, "assets"))

for _d in (WORK, FONTS, OUT, PREVIEW):
    os.makedirs(_d, exist_ok=True)
