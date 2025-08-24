import time, random
import tkinter.font as tkfont
from .theme import ORANGE, AMBER, SUCCESS, PINK, BLUE, TEXT, _hex_to_rgb, _rgb_to_hex

def pop_font(root, font: tkfont.Font, base: int, delta: int, ms: int):
    steps = 5
    for i in range(steps+1):
        t = i/steps
        size = int(base + delta * (1 - (2*t-1)**2))
        root.after(int(ms*i/steps), lambda s=size: font.configure(size=s))

def animate_count(root, label, total: int, font: tkfont.Font, on_done=None, duration=650):
    if total <= 0:
        label.config(text="0 participant")
        if on_done: on_done()
        return
    start = int(time.time()*1000)
    last_value = -1
    def ease_out_quad(t): return 1 - (1-t)*(1-t)
    def tick():
        nonlocal last_value
        now = int(time.time()*1000)
        progress = min(1.0, (now - start)/duration)
        value = int(total * ease_out_quad(progress))
        if value != last_value:
            txt = f"{value} participant" if value == 1 else f"{value} participants"
            label.config(text=txt); last_value = value
        if progress >= 1.0:
            pop_font(root, font, base=font['size'], delta=2, ms=120)
            if on_done: on_done()
        else:
            root.after(16, tick)
    tick()

def confetti_burst(root, canvas, n=120, life=1400, on_end=None):
    """Dessine des confettis *dans le même Canvas* que le contenu → labels visibles."""
    canvas.update_idletasks()
    w = max(2, canvas.winfo_width())
    h = max(2, canvas.winfo_height())
    if w <= 2 or h <= 2:
        canvas.after(30, lambda: confetti_burst(root, canvas, n, life, on_end))
        return

    colors = [ORANGE, AMBER, SUCCESS, PINK, BLUE, TEXT]
    canvas.delete("confetti")

    parts = []
    for _ in range(n):
        x = random.randint(int(w*0.1), int(w*0.9))
        y = random.randint(0, int(h*0.15))
        vx = random.uniform(-3.0, 3.0)
        vy = random.uniform(0.5, 2.4)
        size = random.randint(3, 6)
        c = random.choice(colors)
        it = canvas.create_rectangle(x, y, x+size, y+size, fill=c, outline="", tags=("confetti",))
        parts.append([it, x, y, vx, vy, size, c, 0])

    start = int(time.time()*1000)
    def step():
        now = int(time.time()*1000)
        if now - start > life:
            canvas.delete("confetti")
            if on_end: root.after(250, on_end)
            return
        for p in parts:
            it,x,y,vx,vy,size,c,phase = p
            vy += 0.06; x += vx; y += vy
            p[1], p[2], p[4], p[7] = x, y, vy, phase+1
            canvas.move(it, vx, vy)
            if p[7] % 6 == 0:
                r,g,b = _hex_to_rgb(c)
                k = 0.7 if (p[7]//6) % 2 else 1.0
                canvas.itemconfig(it, fill=_rgb_to_hex(r*k, g*k, b*k))
        canvas.after(16, step)
    step()
