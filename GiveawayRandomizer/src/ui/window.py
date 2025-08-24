import tkinter as tk, tkinter.font as tkfont
from tkinter import filedialog, messagebox
from .theme import ORANGE, BLACK, BG, SURFACE, CARD, BORDER, TEXT, MUTED, GOLD, AMBER, mix
from .animations import pop_font, animate_count, confetti_burst
from core import list_to_array, draw, save_winners
import os, sys
from .theme import CUSTOM_TITLEBAR, TITLEBAR_BG, TITLEBAR_FG, WINDOW_BORDER

def resource_path(rel):
    # compatible PyInstaller (sys._MEIPASS) et exécution dev
    base = getattr(sys, "_MEIPASS", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    return os.path.join(base, rel)


class XButton(tk.Label):
    def __init__(self, master, text, command=None, primary=False, **kw):
        super().__init__(master, **kw)
        self.command = command; self.primary = primary
        self.config(text=text, bg=ORANGE if primary else SURFACE, fg=BLACK if primary else TEXT,
                    bd=0, padx=14, pady=8, cursor="hand2", font=("Helvetica", 11, "bold"),
                    relief="flat", highlightthickness=1,
                    highlightbackground=GOLD if primary else BORDER)
        self._bg_norm = self['bg']
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
    def _on_enter(self, _=None): self.config(bg=AMBER if self.primary else mix(SURFACE, BORDER, 0.5))
    def _on_leave(self, _=None): self.config(bg=self._bg_norm)
    def _on_click(self, _=None):
        old = self['bg']; self.config(bg=GOLD if self.primary else BORDER)
        self.after(120, lambda: self.config(bg=old))
        if self.command: self.command()

class Card(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, bg=CARD, **kw)
        self.configure(highlightthickness=1, highlightbackground=BORDER)

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Mon Outil Loterie")
        self.root.configure(bg=BG); self.root.minsize(900, 560)

        # Fonts
        self.font_title = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.font_count = tkfont.Font(family="Helvetica", size=26, weight="bold")
        self.font_text  = tkfont.Font(family="Helvetica", size=11)

        # --- Titlebar custom robuste ---
        self._closing = False  # évite toute logique pendant la fermeture

        if CUSTOM_TITLEBAR:
            self.root.overrideredirect(True)

            # Contour + conteneur
            outer = tk.Frame(self.root, bg=WINDOW_BORDER)
            outer.pack(fill="both", expand=True)
            container = tk.Frame(outer, bg=BG)
            container.pack(fill="both", expand=True, padx=1, pady=1)

            root_container = container  # <-- utilise root_container ensuite (header/body...)

            # Barre de titre (36px)
            tb = tk.Frame(root_container, bg=TITLEBAR_BG, height=36)
            tb.pack(fill="x")
            tb.pack_propagate(False)

            # Zone de drag séparée des boutons
            drag_area = tk.Frame(tb, bg=TITLEBAR_BG)
            drag_area.pack(side="left", fill="both", expand=True)

            title = tk.Label(drag_area, text="Mon Outil Loterie",
                            bg=TITLEBAR_BG, fg=TITLEBAR_FG, font=("Helvetica", 11, "bold"))
            title.pack(side="left", padx=10)

            btns = tk.Frame(tb, bg=TITLEBAR_BG)
            btns.pack(side="right")

            btn_min = tk.Label(btns, text="—", bg=TITLEBAR_BG, fg="#DDDDDD",
                            padx=12, pady=6, cursor="hand2")
            btn_close = tk.Label(btns, text="✕", bg=TITLEBAR_BG, fg="#DDDDDD",
                                padx=12, pady=6, cursor="hand2")
            btn_min.pack(side="left")
            btn_close.pack(side="left")

            # ----- Drag (uniquement sur la zone de drag) -----
            self._drag_start = None
            def _start_move(e):
                if self._closing:
                    return "break"
                self._drag_start = (e.x_root, e.y_root, self.root.winfo_x(), self.root.winfo_y())
            def _do_move(e):
                if self._drag_start and not self._closing:
                    xr, yr, x0, y0 = self._drag_start
                    self.root.geometry(f"+{x0 + (e.x_root - xr)}+{y0 + (e.y_root - yr)}")
            def _end_move(e):
                self._drag_start = None

            drag_area.bind("<Button-1>", _start_move)
            drag_area.bind("<B1-Motion>", _do_move)
            drag_area.bind("<ButtonRelease-1>", _end_move)

            # ----- Boutons (couper la propagation !) -----
            def _on_close(e=None):
                if self._closing:
                    return "break"
                self._closing = True
                try:
                    self.root.unbind("<Map>")  # pas de ré-application d'overrideredirect pendant la fermeture
                except Exception:
                    pass
                # feedback instantané → puis fermeture propre
                try:
                    self.root.overrideredirect(False)  # évite certains glitches Windows
                except Exception:
                    pass
                self.root.withdraw()
                self.root.after(10, self.root.destroy)
                return "break"

            def _on_minimize(e=None):
                if self._closing:
                    return "break"
                # Windows: autoriser iconify()
                self.root.overrideredirect(False)
                self.root.update_idletasks()
                self.root.iconify()
                return "break"

            btn_close.bind("<Button-1>", _on_close)
            btn_min.bind("<Button-1>", _on_minimize)

            # Quand la fenêtre revient après réduction : réactiver overrideredirect
            def _reapply_overrideredirect(_=None):
                if self._closing:
                    return
                if self.root.state() == "normal":
                    self.root.overrideredirect(True)
            self.root.bind("<Map>", _reapply_overrideredirect)

            # Alt+F4 / close système
            self.root.protocol("WM_DELETE_WINDOW", _on_close)
        else:
            root_container = self.root


        # Header
        self.header = tk.Frame(root_container, bg=BLACK); self.header.pack(fill="x")
        tk.Label(self.header, text="Tirage au sort", bg=BLACK, fg=ORANGE,
                 font=self.font_title, padx=16, pady=12).pack(side="left")

        # Body
        self.body = tk.Frame(root_container, bg=BG); self.body.pack(fill="both", expand=True, padx=16, pady=16)
        left = tk.Frame(self.body, bg=BG);  left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(self.body, bg=BG); right.pack(side="left", fill="both", expand=True, padx=(16,0))

        # Left (participants)
        self.input_card = Card(left); self.input_card.pack(fill="both", expand=True)
        tk.Label(self.input_card, text="Participants (un par ligne)", bg=CARD, fg=MUTED,
                 anchor="w", padx=12, pady=10, font=self.font_text).pack(fill="x")
        self.txt = tk.Text(self.input_card, height=16, bg=SURFACE, fg=TEXT, insertbackground=TEXT,
                           bd=0, padx=12, pady=12, font=("Courier New", 11))
        self.txt.pack(fill="both", expand=True, padx=12, pady=(0,12))

        controls = tk.Frame(self.input_card, bg=CARD); controls.pack(fill="x", padx=12, pady=(0,12))
        tk.Label(controls, text="Nombre de gagnants", bg=CARD, fg=MUTED, font=self.font_text).pack(side="left")
        self.winner_var = tk.StringVar(value="1")
        self.spin = tk.Spinbox(controls, from_=1, to=9999, textvariable=self.winner_var, width=6,
                               bg=SURFACE, fg=TEXT, bd=0, insertbackground=TEXT,
                               highlightthickness=1, highlightbackground=BORDER, justify="center")
        self.spin.pack(side="left", padx=8)
        self.btn_draw = XButton(controls, "Tirer au sort", command=self.on_draw, primary=True); self.btn_draw.pack(side="left", padx=(8,0))
        self.btn_load = XButton(controls, "Importer (.txt)", command=self.load_txt); self.btn_load.pack(side="left", padx=(8,0))

        # Right (results) —> UN SEUL CANVAS qui contient tout (texte + confettis)
        self.results_card = Card(right); self.results_card.pack(fill="both", expand=True)

        topbar = tk.Frame(self.results_card, bg=CARD, height=72)
        topbar.pack(fill="x"); topbar.pack_propagate(False)
        self.count_label = tk.Label(topbar, text="0 participant", bg=CARD, fg=TEXT,
                                    font=self.font_count, padx=12, pady=10, anchor="w",
                                    width=22, justify="left")
        self.count_label.pack(side="left", fill="x", expand=True)

        # Canvas plein pour résultats + confettis + (les lignes comme window-items)
        self.fx_canvas = tk.Canvas(self.results_card, bg=CARD, highlightthickness=0)
        self.fx_canvas.pack(fill="both", expand=True, padx=12, pady=(0,12))
        
        # --- Barre de statut en bas (gauche) avec icône info ---
        self.status_bar = tk.Frame(self.results_card, bg=CARD)
        self.status_bar.pack(fill="x", padx=12, pady=(0, 12))

        # Petit logo (i) – on utilise le caractère Unicode 'ⓘ'
        self.status_chip = tk.Label(
            self.status_bar, text="ⓘ",
            bg=mix(BLACK, CARD, 0.40), fg=TEXT,
            padx=6, pady=2, font=("Helvetica", 12, "bold")
        )
        self.status_chip.pack(side="left")

        # Texte de statut à côté de l’icône
        self.status = tk.Label(
            self.status_bar, text="Prêt.",
            bg=CARD, fg=MUTED, font=("Helvetica", 10)
        )
        self.status.pack(side="left", padx=(6, 0))


        # Frame logique (lignes) rendu *dans* le Canvas
        self.results_container = tk.Frame(self.fx_canvas, bg=CARD)
        self.content_win = self.fx_canvas.create_window(0, 0, window=self.results_container, anchor="nw")

        # Maintenir la largeur du frame = largeur canvas (layout stable)
        def _on_canvas_resize(e):
            self.fx_canvas.itemconfigure(self.content_win, width=e.width)
        self.fx_canvas.bind("<Configure>", _on_canvas_resize)

        # Raccourcis
        self.root.bind("<Control-Return>", lambda e: self.on_draw())
        self.root.bind("<Control-o>",      lambda e: self.load_txt())

        self.current_participants = []

    # Utils
    def set_status(self, text: str):
        self.status.config(text=text)
        # petit pulse de l'icône info
        self._pulse_status()

    def _pulse_status(self, steps=10, i=0):
        # Animation de fond de l'icône (i)
        if i >= steps:
            self.status_chip.config(bg=mix(BLACK, CARD, 0.40))
            return
        t = i / steps
        # va-et-vient entre noir et doré
        self.status_chip.config(bg=mix(BLACK, GOLD, 0.10 + 0.10 * abs(0.5 - t)))
        self.root.after(30, lambda: self._pulse_status(steps, i + 1))


    def load_txt(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path: return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.txt.delete("1.0", "end"); self.txt.insert("1.0", f.read())
            self.set_status(f"Importé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier.\n\n{e}")

    def clear_results(self):
        for child in list(self.results_container.children.values()):
            child.destroy()
        # aussi nettoyer d’éventuels confettis restants
        self.fx_canvas.delete("confetti")

    # Anim & actions
    def animate_winner_reveal(self, label: tk.Label, final_name: str, pool: list, on_done=None):
        spin_steps = [(12, 60), (6, 140)]
        def run_stage(stage_idx=0, i=0):
            if stage_idx >= len(spin_steps):
                label.config(text=f"{final_name}", fg=ORANGE)
                try:
                    f = tkfont.nametofont(label.cget("font"))
                    pop_font(self.root, f, base=f['size'], delta=3, ms=180)
                except Exception:
                    pass
                # ⚠️ Ici : confettis dessinés DANS le même Canvas -> les labels restent visibles
                confetti_burst(self.root, self.fx_canvas, on_end=on_done)
                return
            total_iter, delay = spin_steps[stage_idx]
            if i < total_iter:
                fake = pool[int(self.root.tk.eval('clock clicks')) % len(pool)]  # évite time()*1000 fluctuations lente
                label.config(text=f"🎲 {fake}", fg=MUTED)
                self.root.after(delay, lambda: run_stage(stage_idx, i+1))
            else:
                self.root.after(100, lambda: run_stage(stage_idx+1, 0))
        run_stage()

    def on_draw(self):
        raw = self.txt.get("1.0", "end")
        participants = list_to_array(raw)
        self.current_participants = participants
        total = len(participants)
        self.clear_results()

        try:
            winners_count = int(self.winner_var.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le nombre de gagnants doit être un entier.")
            return
        if total == 0:
            messagebox.showwarning("Aucun participant", "Ajoute au moins un nom.")
            return

        winners_count = max(1, min(winners_count, total))
        self.set_status("Comptage des participants…")

        def after_count():
            self.set_status("Tirage en cours…")
            winners = draw(participants.copy(), winners_count)

            # lignes de résultats (dans results_container, qui est un window-item du Canvas)
            lines = []
            for i in range(1, winners_count+1):
                row = tk.Frame(self.results_container, bg=CARD); row.pack(anchor="w")
                tk.Label(row, text=f"Gagnant {i} :", bg=CARD, fg=MUTED, font=self.font_text).pack(side="left", padx=(0,6), pady=2)
                f = tkfont.Font(family="Helvetica", size=12)
                lbl = tk.Label(row, text="—", bg=CARD, fg=TEXT, font=f)
                lbl.pack(side="left", pady=2)
                lines.append(lbl)

            pool = participants + winners
            def reveal_next(idx=0):
                if idx >= len(winners):
                    try:
                        save_winners("gagnants.txt", winners)
                        self.set_status("Résultats sauvegardés dans gagnants.txt")
                    except Exception as e:
                        self.set_status(f"Erreur de sauvegarde : {e}")
                    return
                self.animate_winner_reveal(lines[idx], winners[idx], pool, on_done=lambda: reveal_next(idx+1))
            reveal_next()
        animate_count(self.root, self.count_label, total, self.font_count, on_done=after_count)

def run_app():
    root = tk.Tk()
    # Icônes de la fenêtre
    try:
        ico = resource_path("assets/kdo.ico")
        png = resource_path("assets/kdo_256.png")

        # Windows: définit l'icône .ico (barre des tâches + alt-tab si lancé en .exe)
        if sys.platform.startswith("win") and os.path.exists(ico):
            root.iconbitmap(default=ico)

        # Tous OS: icône Tk (peut afficher plusieurs tailles si fournies)
        if os.path.exists(png):
            root.iconphoto(True, tk.PhotoImage(file=png))
    except Exception as e:
        print("Icon load error:", e)

    app = App(root)
    root.mainloop()
