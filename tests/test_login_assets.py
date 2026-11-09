import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ["DB_MODE"] = "test"

import tkinter as tk

try:
    from PIL import Image
except ImportError:
    Image = None

import ui as ui_mod


def main():
    if Image is None:
        print("Pillow no disponible; prueba omitida")
        return

    with tempfile.TemporaryDirectory() as tmp:
        images = Path(tmp) / "images"
        images.mkdir()
        Image.new("RGBA", (64, 64), (201, 162, 39, 255)).save(images / "logo.png")
        Image.new("RGBA", (400, 300), (15, 42, 74, 255)).save(images / "login_bg.png")

        original = ui_mod._ruta_recurso
        ui_mod._ruta_recurso = lambda *partes: os.path.join(tmp, *partes)
        root = tk.Tk()
        try:
            app = ui_mod.UI(root)
            root.update()
            assert app._logo_login_photo is not None
            assert app._logo_sidebar_photo is not None
            assert app._logo_sidebar_photo.width() <= 64
            assert app._logo_sidebar_photo.height() <= 64
            assert app._login_bg_original is not None
            assert app._login_bg_label is not None
            app._renderizar_fondo_login(400, 300)
            assert app._login_bg_photo is not None
            print("carga de logo y fondo de login OK")
        finally:
            ui_mod._ruta_recurso = original
            root.destroy()


if __name__ == "__main__":
    main()
