@echo off
REM Script d'aide à la génération d'un .exe
python -m venv .venv
call .venv\Scripts\activate
pip install --upgrade pip
pip install pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name "GiveawayRandomizer" src\main_gui.py
echo.
echo Build terminé. Fichier : dist\GiveawayRandomizer.exe
pause
