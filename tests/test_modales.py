import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ["DB_MODE"] = "test"

import tkinter as tk

import ui as ui_mod


def cerrar_toplevels(root):
    for widget in list(root.winfo_children()):
        if isinstance(widget, tk.Toplevel):
            try:
                widget.grab_release()
            except Exception:
                pass
            widget.destroy()


def main():
    root = tk.Tk()
    errores = []
    root.report_callback_exception = lambda exc, val, tb: errores.append((exc, val))
    try:
        app = ui_mod.UI(root)
        app.usuario_actual = "admin"
        app.usuario_rol = "admin"
        root.update()

        win = tk.Toplevel(root)
        ui_mod._activar_modal(win)
        assert win.grab_current() == win
        cerrar_toplevels(root)
        print("activacion modal OK")

        app.mostrar_registrar_usuario()
        root.update()

        app.input_fecha_nacimiento.abrir()
        root.update()
        assert not errores, errores
        assert cerrar_toplevels(root) is None
        print("selector de fecha modal OK")

        tree = app._bal_tree
        items = tree.get_children()
        assert items
        tree.selection_set(items[0])
        app._abrir_editor_egreso(tree, items[0])
        root.update()
        assert not errores, errores
        assert [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)]
        cerrar_toplevels(root)
        print("edicion de egreso modal OK")

        for accion in (app.abrir_catalogos, app.gestionar_usuarios, app.ver_auditoria):
            accion()
            root.update()
            assert not errores, errores
            assert [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)]
            cerrar_toplevels(root)
        print("catalogos, usuarios y auditoria modales OK")
    finally:
        try:
            root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    main()
