cd "YOURPATHHERE\GiveawayRandomizer"
. .\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel pyinstaller
python -m PyInstaller --noconfirm --clean --onedir --noconsole --noupx --icon assets\kdo.ico --add-data "assets;assets" --version-file version_info.txt -n MolonelTirage src\main_gui.py