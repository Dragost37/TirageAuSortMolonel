from ui.window import run_app
import sys

if sys.platform.startswith("win"):
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Molonel.GiveawayRandomizer")
    except Exception:
        pass

from ui.window import run_app

if __name__ == "__main__":
    run_app()
