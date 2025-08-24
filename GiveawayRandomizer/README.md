# Giveaway Randomizer — version GUI (noir & blanc)

Projet minimaliste qui **sépare** :
- la **logique de giveaway** (`src/core.py`),
- la **logique d'interface + affichage** (`src/ui_tk.py`),
- et un **point d'entrée** (`src/main_gui.py`).

Interface en noir & blanc (Tkinter), animations :
- compteur de participants (4 s, easing),
- révélation des gagnants façon "roulette".
- export automatique `winners.txt`.

---

## Démarrer en local

1) Installer Python 3.10+ sur Windows.
2) Dans un terminal PowerShell/CMD à la racine du projet :

```bat
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
python src\\main_gui.py
```

## Générer un .exe Windows (PyInstaller)

Toujours dans l'environnement virtuel :

```bat
pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed ^
  --name "GiveawayRandomizer" src\\main_gui.py
```

Le binaire sera dans `dist\\GiveawayRandomizer.exe`.

> Astuce : si vous souhaitez voir les logs console pendant le dev,
> utilisez `--console` à la place de `--windowed`.

## Arborescence

```
giveaway_app/
├─ src/
│  ├─ core.py        # logique pure (nettoyage + tirage)
│  ├─ ui_tk.py       # interface Tkinter + animations
│  └─ main_gui.py    # point d'entrée
└─ README.md
```

## Remarques

- **Encodage** : UTF‑8 (fichiers et sortie).
- **Animations** : sans thread, pilotées avec `after()` de Tkinter.
- **Doublons** : supprimés en ignorant les espaces.
- **Sécurité** : si `gagnants > participants`, le nombre est automatiquement borné.