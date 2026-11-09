import os
import sys
import sqlite3
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ["DB_MODE"] = "test"

import tkinter as tk
import logic
import ui as ui_mod

CEDULA = "99999980"
CEDULA_NORM = "V-99999980"
CEDULA_LEGACY = "V-99999989"


def limpiar():
    conn = sqlite3.connect(logic.DB_FILE)
    try:
        for cedula in (CEDULA_NORM, CEDULA_LEGACY):
            conn.execute("DELETE FROM egresos_mensuales WHERE funcionario_cedula = ?", (cedula,))
            conn.execute("DELETE FROM familiares WHERE funcionario_cedula = ?", (cedula,))
            conn.execute("DELETE FROM funcionarios WHERE cedula = ?", (cedula,))
            conn.execute("DELETE FROM auditoria WHERE detalle LIKE ?", (f"%{cedula}%",))
        conn.commit()
    finally:
        conn.close()


def set_entry(app, attr, valor):
    w = getattr(app, attr)
    w.delete(0, "end")
    w.insert(0, valor)


def llenar_requeridos(app):
    muns = logic.valores_catalogo("municipio")
    mun_res = muns[0]
    pueblos_res = [p["valor"] for p in logic.cargar_catalogo("pueblo") if p["detalle"] == mun_res]

    app.input_cedula.delete(0, "end"); app.input_cedula.insert(0, CEDULA)
    app.input_nombre.insert(0, "Obligatorios")
    app.input_apellido.insert(0, "Test")
    app.input_fecha_nacimiento.set("10/10/1985", True)
    app.input_genero.set("Masculino")
    app.input_estado_civil.set(logic.valores_catalogo("estado_civil")[0])
    app.input_operadora.set("412")
    app.input_telefono.delete(0, "end"); app.input_telefono.insert(0, "1234567")
    app.input_residencia_municipio.set(mun_res)
    app._filtrar_pueblos_residencia()
    if pueblos_res:
        app.input_residencia_pueblo.set(pueblos_res[0])
    app.input_residencia.insert(0, "Calle 1, casa 2")

    app.input_jerarquia.set(logic.valores_catalogo("jerarquia")[0])
    app.input_lugar_servicio.set(logic.valores_catalogo("lugar_servicio")[0])
    app.input_tiempo_servicio.set("De 1 a 3 años")
    app.input_ingreso_mensual.delete(0, "end"); app.input_ingreso_mensual.insert(0, "1000,00")

    app.posee_terreno.set("NO")
    app.posee_vivienda.set("NO")
    app.necesidad_habiacion.set("Vivienda")
    app.gestion_organismo.set("NO")

    app.tenencia_tierra.set("Propia")
    app.input_tiempo_ocupacion.set("De 1 a 3 años")
    for attr in (
        "input_num_sala", "input_num_sala_comedor", "input_num_cocina",
        "input_num_cocina_comedor", "input_num_bano", "input_num_dormitorio",
    ):
        set_entry(app, attr, "0")


def agregar_familiar(app, nombre, apellido, edad):
    app.crear_nuevo_panel_familiar()
    inputs = app.familiares_panels[-1][1]
    inputs["nombre"].insert(0, nombre)
    inputs["apellido"].insert(0, apellido)
    inputs["parentesco"].set(logic.valores_catalogo("parentesco")[0])
    if edad:
        inputs["edad"].insert(0, edad)
    return inputs


def main():
    limpiar()
    avisos = {"warn": [], "error": [], "info": []}

    def rec(kind):
        def f(title, msg, **kw):
            avisos[kind].append((title, msg))
        return f

    root = tk.Tk()
    try:
        with mock.patch.object(ui_mod.messagebox, "showwarning", rec("warn")), \
             mock.patch.object(ui_mod.messagebox, "showerror", rec("error")), \
             mock.patch.object(ui_mod.messagebox, "showinfo", rec("info")):
            app = ui_mod.UI(root)
            app.usuario_actual = "tester"
            app.usuario_rol = "admin"
            app.mostrar_registrar_usuario()
            root.update()

            assert app._validar_edad_familiar("")
            for v in ("1", "01", "200"):
                assert app._validar_edad_familiar(v), v
            for v in ("0", "201", "-1", "1.5", "a", " 1", "²", "1000", "0001"):
                assert not app._validar_edad_familiar(v), v
            assert app._edad_familiar_valida("")
            assert app._edad_familiar_valida("200")
            assert not app._edad_familiar_valida("201")
            assert app._normalizar_edad_familiar("01") == "1"
            assert app._normalizar_edad_familiar("") == ""
            assert app._normalizar_edad_familiar("201") == ""
            print("edad familiar validacion OK")

            llenar_requeridos(app)
            inputs = agregar_familiar(app, "Hijo", "Uno", "")
            root.update()
            assert app._faltantes_obligatorios() == [], app._faltantes_obligatorios()
            print("formulario requerido OK")

            inputs["edad"].insert(0, "201")
            assert inputs["edad"].get() == ""
            inputs["edad"].insert(0, "0")
            assert inputs["edad"].get() == ""
            inputs["edad"].insert(0, "200")
            assert inputs["edad"].get() == "200"
            inputs["edad"].delete(0, "end")
            root.update()
            print("edad familiar teclado OK")

            app.input_telefono.delete(0, "end"); app.input_telefono.insert(0, "-")
            falt = app._faltantes_obligatorios()
            assert "Datos personales: Telefono" in falt, falt
            app.input_telefono.delete(0, "end"); app.input_telefono.insert(0, "1234567")

            inputs["nombre"].delete(0, "end")
            avisos["warn"].clear()
            app.guardar_funcionario()
            assert avisos["warn"], avisos
            assert "Familiar #1: Nombre" in avisos["warn"][-1][1]
            assert not [f for f in logic.cargar_funcionarios(incluir_inactivos=True)
                        if f.cedula == CEDULA_NORM]
            inputs["nombre"].insert(0, "Hijo")
            print("faltante familiar bloquea guardado OK")

            inputs["edad"].config(validate="none")
            inputs["edad"].delete(0, "end"); inputs["edad"].insert(0, "201")
            avisos["warn"].clear()
            app.guardar_funcionario()
            assert avisos["warn"], avisos
            assert "Familiar #1: Edad (1 a 200)" in avisos["warn"][-1][1]
            assert not [f for f in logic.cargar_funcionarios(incluir_inactivos=True)
                        if f.cedula == CEDULA_NORM]
            inputs["edad"].config(
                validate="key",
                validatecommand=(root.register(app._validar_edad_familiar), "%P"),
            )
            inputs["edad"].delete(0, "end")
            print("edad invalida bloquea guardado OK")

            app.posee_terreno.set("SI")
            falt = app._faltantes_obligatorios()
            assert "Plan Vivienda: Municipio del terreno" in falt, falt
            muns = logic.valores_catalogo("municipio")
            mun_viv = muns[1]
            app.input_municipio.set(mun_viv)
            app._filtrar_pueblos()
            pueblos_viv = [p["valor"] for p in logic.cargar_catalogo("pueblo") if p["detalle"] == mun_viv]
            if pueblos_viv:
                falt = app._faltantes_obligatorios()
                assert "Plan Vivienda: Pueblo del terreno" in falt, falt
                app.input_pueblo.set(pueblos_viv[0])
            assert app._faltantes_obligatorios() == [], app._faltantes_obligatorios()
            app.posee_terreno.set("NO")

            app.posee_vivienda.set("SI")
            falt = app._faltantes_obligatorios()
            assert "Plan Vivienda: Condicion de la vivienda" in falt, falt
            app.input_condicion_vivienda.set(logic.valores_catalogo("condicion_vivienda")[0])
            assert app._faltantes_obligatorios() == [], app._faltantes_obligatorios()
            app.posee_vivienda.set("NO")

            app.gestion_organismo.set("SI")
            falt = app._faltantes_obligatorios()
            assert "Plan Vivienda: Organismo publico o privado" in falt, falt
            app.organismo_publico.set("Otra")
            falt = app._faltantes_obligatorios()
            assert "Plan Vivienda: Especifique organismo publico" in falt, falt
            app.input_organismo_publico_otro.insert(0, "Fundacion X")
            falt = app._faltantes_obligatorios()
            assert "Plan Vivienda: Fecha de gestion" in falt, falt
            app.input_fecha_gestion.set("04/11/2025", True)
            assert app._faltantes_obligatorios() == [], app._faltantes_obligatorios()
            app.gestion_organismo.set("NO")

            app.tenencia_tierra.set("Otra")
            falt = app._faltantes_obligatorios()
            assert "Estado Vivienda: Especifique tenencia de tierra" in falt, falt
            app.input_tenencia_tierra_otra.set("Alquilada")
            assert app._faltantes_obligatorios() == [], app._faltantes_obligatorios()
            app.tenencia_tierra.set("Propia")

            app._serv_vars["serv_otro"].set("SI")
            falt = app._faltantes_obligatorios()
            assert "Estado Vivienda: Especifique servicio otros" in falt, falt
            app._estado_entries["serv_especifico"].insert(0, "Internet")
            assert app._faltantes_obligatorios() == [], app._faltantes_obligatorios()
            app._serv_vars["serv_otro"].set("NO")

            set_entry(app, "input_num_sala", "")
            falt = app._faltantes_obligatorios()
            assert "Estado Vivienda: Ambientes - Sala" in falt, falt
            set_entry(app, "input_num_sala", "0")

            app._bal_entries["ingreso_trabajador"].delete(0, "end")
            falt = app._faltantes_obligatorios()
            assert "Balance: Ingreso del trabajador" in falt, falt
            app._bal_entries["ingreso_trabajador"].insert(0, "abc")
            falt = app._faltantes_obligatorios()
            assert "Balance: Ingreso del trabajador (numero valido)" in falt, falt
            app._bal_entries["ingreso_trabajador"].delete(0, "end")
            app._bal_entries["ingreso_trabajador"].insert(0, "0")

            app.input_ingreso_mensual.delete(0, "end")
            falt = app._faltantes_obligatorios()
            assert "Datos laborales: Ingreso mensual" in falt, falt
            app.input_ingreso_mensual.insert(0, "1000,00")
            print("obligatorios condicionales OK")

            agregar_familiar(app, "Hijo", "Dos", "01")
            root.update()
            assert app._faltantes_obligatorios() == [], app._faltantes_obligatorios()

            avisos["warn"].clear(); avisos["error"].clear(); avisos["info"].clear()
            app.guardar_funcionario()
            root.update()
            assert not avisos["warn"] and not avisos["error"], avisos
            assert avisos["info"], avisos
            f = next(x for x in logic.cargar_funcionarios(incluir_inactivos=True)
                     if x.cedula == CEDULA_NORM)
            assert len(f.grupo_familiar) == 2, f.grupo_familiar
            assert f.grupo_familiar[0].edad == "", f.grupo_familiar[0].edad
            assert f.grupo_familiar[1].edad == "1", f.grupo_familiar[1].edad
            print("guardado con edad opcional y normalizada OK")

            f_legacy = logic.Funcionario(
                CEDULA_LEGACY, "Legacy", "Edad", "10/10/1980", "46",
                "1234567", "", "", logic.valores_catalogo("estado_civil")[0], "Calle 3"
            )
            f_legacy.agregar_familiar(logic.Familiar(
                "Hijo", "Legacy", logic.valores_catalogo("parentesco")[0], "999",
                "Masculino", "", "", "", "", "", ""
            ))
            avisos["warn"].clear()
            app._cargar_datos_en_formulario(f_legacy)
            root.update()
            assert avisos["warn"], avisos
            assert avisos["warn"][-1][0] == "Edad familiar invalida"
            assert app.familiares_panels[0][1]["edad"].get() == ""
            print("edad legacy invalida limpiada OK")

    finally:
        try:
            root.destroy()
        except Exception:
            pass
        limpiar()
        print("limpieza OK")


if __name__ == "__main__":
    main()
