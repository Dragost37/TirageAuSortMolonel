# Quick Start
## Lancer
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src\main_gui.py
```

## Build
pyinstaller --noconfirm --onefile --noconsole --icon assets\kdo.ico --add-data "assets;assets" --version-file version_info.txt -n MolonelTirage src\main_gui.py