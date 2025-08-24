=== Giveaway Randomizer (split) ===

Lancement en dev :
  python src/main_gui.py

Structure :
  src/
    core/          -> logique métier (tirage, parsing, I/O)
    ui/            -> interface (thème, animations, fenêtre)
    main_gui.py    -> point d'entrée

Créer un .exe Windows (PyInstaller) :
  pip install pyinstaller
  pyinstaller --noconfirm --onefile --noconsole -n MolonelTirage src/main_gui.py

  Le binaire sera dans dist/MolonelTirage.exe
