# Couleurs (Molonel)
ORANGE = "#E69B05"
BLACK  = "#0F0F0F"
BG      = "#0B0B0B"
SURFACE = "#141414"
CARD    = "#171717"
BORDER  = "#202020"
TEXT    = "#F4F4F4"
MUTED   = "#C7C7C7"
AMBER   = "#FFC042"
GOLD    = "#F5B83D"
SUCCESS = "#5EE17C"
PINK    = "#FF7AC3"
BLUE    = "#55B8FF"
CUSTOM_TITLEBAR = True
TITLEBAR_BG = BLACK
TITLEBAR_FG = ORANGE
WINDOW_BORDER = "#E69B05"   # liseré autour (optionnel)


def _hex_to_rgb(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def _rgb_to_hex(r,g,b):
    return '#%02X%02X%02X' % (max(0,min(255,int(r))), max(0,min(255,int(g))), max(0,min(255,int(b))))
def mix(c1, c2, t):
    r1,g1,b1 = _hex_to_rgb(c1); r2,g2,b2 = _hex_to_rgb(c2)
    r = r1 + (r2-r1)*t; g = g1 + (g2-g1)*t; b = b1 + (b2-b1)*t
    return _rgb_to_hex(r,g,b)
