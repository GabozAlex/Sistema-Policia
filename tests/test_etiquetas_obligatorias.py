import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ["DB_MODE"] = "test"

import tkinter as tk

import ui as ui_mod


def etiquetas(widget):
    resultado = []
    for hijo in widget.winfo_children():
        if isinstance(hijo, tk.Label):
            resultado.append(hijo)
        resultado.extend(etiquetas(hijo))
    return resultado


def main():
    root = tk.Tk()
    root.withdraw()
    try:
        app = ui_mod.UI(root)
        app.usuario_actual = "tester"
        app.usuario_rol = "admin"
        app.mostrar_registrar_usuario()
        root.update()

        contenedor = tk.Frame(root, bg=app.bg_card)
        obligatoria = app._etiqueta(
            contenedor, "Nombres:", obligatorio=True,
            font=(ui_mod.FONT, 10), fg=app.text)
        condicional = app._etiqueta(
            contenedor, "Municipio:", condicional=True,
            font=(ui_mod.FONT, 10), fg=app.text)
        root.update()

        partes = obligatoria.winfo_children()
        assert [w.cget("text") for w in partes] == ["Nombres:", "*"]
        assert str(partes[1].cget("fg")) == app.danger

        partes = condicional.winfo_children()
        assert [w.cget("text") for w in partes] == ["Municipio:", "**"]
        assert str(partes[1].cget("fg")) == app.accent

        antes = len([w for w in etiquetas(root)
                     if w.cget("text") == "*" and str(w.cget("fg")) == app.danger])
        dobles = [w for w in etiquetas(root)
                  if w.cget("text") == "**" and str(w.cget("fg")) == app.accent]
        assert antes >= 20, antes
        assert len(dobles) >= 6, len(dobles)

        app.crear_nuevo_panel_familiar()
        root.update()
        despues = len([w for w in etiquetas(root)
                       if w.cget("text") == "*" and str(w.cget("fg")) == app.danger])
        assert despues == antes + 3, (antes, despues)

        print("etiquetas obligatorias OK")
    finally:
        root.destroy()


if __name__ == "__main__":
    main()
