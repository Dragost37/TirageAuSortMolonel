# Molonel - Giveaway Randomizer (GUI)

Appli Tkinter **modulaire** pour tirages au sort, thème **noir & orange** (Molonel), animations fluides et export automatique des gagnants.

## Points clés

* Séparation claire :

  * **Logique** (nettoyage + tirage + sauvegarde) : `src/core/`
  * **UI & animations** : `src/ui/`
  * **Entrée** : `src/main_gui.py`
* Animations :

  * Compteur de participants (easing)
  * Révélation “roulette”
  * **Confettis** visibles en même temps que les noms gagnants
* Import de liste `.txt` (un pseudo par ligne), **déduplication** (ignore les espaces)
* Export automatique des résultats : `gagnants.txt`
* Raccourcis : **Ctrl+Entrée** (tirage), **Ctrl+O** (import)

---

## Arborescence

```
giveaway_app/
├─ assets/
│  ├─ *.ico
│  └─ ... (png, etc.)
├─ src/
│  ├─ main_gui.py        # point d'entrée (UI + icônes + AppUserModelID)
│  ├─ core/
│  │  ├─ __init__.py     # export : list_to_array, draw, save_winners
│  │  └─ core.py         # logique pure (nettoyage + tirage + sauvegarde)
│  └─ ui/
│     ├─ window.py       # fenêtre, widgets, canevas unique (texte + confettis)
│     ├─ animations.py   # pop_font, animate_count, confetti_burst
│     └─ theme.py        # palette Molonel, options (CUSTOM_TITLEBAR, etc.)
├─ version_info.txt      # métadonnées pour l’EXE (éditeur, version…)
└─ README.md
```

## Options d’interface utiles

* **Barre de titre personnalisée** (sans bordure Windows) :

  * Dans `src/ui/theme.py`, passer `CUSTOM_TITLEBAR = True/False`
  * Avec `True`, les boutons **réduction/fermeture** sont gérés par l’app (patché pour Windows).
  * Avec `False`, on garde la barre native de Windows (alt-tab, snap, etc.).

* **Icônes** :

  * Fenêtre & barre des tâches : `assets/molonel.ico`
  * `main_gui.py` charge aussi un PNG (fallback multi-OS) si présent.

---

## Bonnes pratiques & stabilité

* Les confettis sont rendus **dans le même Canvas** que les labels de résultats → pas de problèmes de superposition : les **noms restent visibles** pendant l’animation.
* Animations **sans threads**, uniquement via `after()`.
* Si vous modifiez le titre personnalisé (`CUSTOM_TITLEBAR=True`) :

  * Les clics des boutons **ne** se propagent pas à la zone de drag (fermeture au **premier** clic).
  * La réduction utilise la séquence Windows : désactiver temporairement `overrideredirect`, `iconify()`, puis réactiver à la remontée.

---

## Licence

Ajoute ici la licence de ton choix (ex. MIT) si tu souhaites open-sourcer le projet.

---

## Crédit

Conception UI/animations & refactor : projet Molonel — Giveaway Randomizer.
