import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ["DB_MODE"] = "test"

import tkinter as tk

import ui as ui_mod


CLAVES = (
    "num_sala",
    "num_sala_comedor",
    "num_cocina",
    "num_cocina_comedor",
    "num_bano",
    "num_dormitorio",
    "num_lavadero",
    "num_patio_terraza",
    "num_frente_porche",
    "num_garaje_estacionamiento",
    "num_deposito_almacen",
)


def main():
    root = tk.Tk()
    root.geometry("1150x760+40+40")
    try:
        app = ui_mod.UI(root)
        app.usuario_actual = "tester"
        app.usuario_rol = "admin"
        app.mostrar_registrar_usuario()
        app.tab_vivienda_plan.master.select(app.tab_vivienda_estado)
        root.update()

        entradas = [app._estado_entries[clave] for clave in CLAVES]
        posiciones = {entrada.winfo_x() for entrada in entradas}
        anchos = {entrada.winfo_width() for entrada in entradas}

        assert len(posiciones) == 1, posiciones
        assert len(anchos) == 1, anchos
        assert next(iter(anchos)) > 0, anchos
        assert all(entrada.grid_info()["column"] == 1 for entrada in entradas)
        assert all(str(entrada.cget("justify")) == "center" for entrada in entradas)

        print("alineacion ambientes OK")
    finally:
        root.destroy()


if __name__ == "__main__":
    main()
