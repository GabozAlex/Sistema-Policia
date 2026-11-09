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

CEDULA = "99999990"
CEDULA_NORM = "V-99999990"
OTRA = ["Alquilada", "Terreno Familiar"]
TIEMPO = ["Menos de 1 año", "De 1 a 3 años", "De 3 a 5 años", "De 5 a 10 años", "Más de 10 años"]


def limpiar():
    conn = sqlite3.connect(logic.DB_FILE)
    try:
        conn.execute("DELETE FROM egresos_mensuales WHERE funcionario_cedula LIKE ?", ("%99999990%",))
        conn.execute("DELETE FROM familiares WHERE funcionario_cedula LIKE ?", ("%99999990%",))
        conn.execute("DELETE FROM funcionarios WHERE cedula LIKE ?", ("%99999990%",))
        conn.execute("DELETE FROM auditoria WHERE detalle LIKE ?", ("%99999990%",))
        conn.commit()
    finally:
        conn.close()


def set_entry(app, attr, valor):
    w = getattr(app, attr)
    w.delete(0, "end")
    w.insert(0, valor)


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

            for v in ("", "0", "1", "9", "10"):
                assert app._validar_entero_0_10(v), v
            for v in ("-1", "11", "100", "1.5", "a", " 2"):
                assert not app._validar_entero_0_10(v), v
            assert not hasattr(app, "input_otros") and not hasattr(app, "input_especificacion")
            set_entry(app, "input_num_sala", "11")
            assert app.input_num_sala.get() == ""
            set_entry(app, "input_num_sala", "")
            print("ambientes validacion OK")

            assert list(app.input_tenencia_tierra_otra.cget("values")) == OTRA
            assert list(app.input_tiempo_ocupacion.cget("values")) == TIEMPO
            assert app.input_tenencia_tierra_otra.master.winfo_ismapped()
            app.tenencia_tierra.set("Propia")
            root.update()
            assert not app.input_tenencia_tierra_otra.master.winfo_ismapped()
            assert app.input_tenencia_tierra_otra.get() == ""
            app.tenencia_tierra.set("Otra")
            root.update()
            assert app.input_tenencia_tierra_otra.master.winfo_ismapped()
            print("estado vivienda opciones OK")

            app.gestion_organismo.set("SI")
            app.organismo_publico.set("Otra")
            app.organismo_privado.set("Otra")
            root.update()
            assert app._fila_organismo_publico_otro.winfo_ismapped()
            assert app._fila_organismo_privado_otro.winfo_ismapped()
            app.gestion_organismo.set("NO")
            assert app.organismo_publico.get() == ""
            assert app.organismo_privado.get() == ""
            assert app.input_fecha_gestion.get() == ""
            print("plan dependencias OK")

            muns = logic.valores_catalogo("municipio")
            mun_per, mun_viv = muns[0], muns[1]
            pueblo_per = [p["valor"] for p in logic.cargar_catalogo("pueblo") if p["detalle"] == mun_per][0]
            pueblo_viv = [p["valor"] for p in logic.cargar_catalogo("pueblo") if p["detalle"] == mun_viv][0]

            app.input_cedula.delete(0, "end"); app.input_cedula.insert(0, CEDULA)
            app.input_nombre.insert(0, "Test")
            app.input_apellido.insert(0, "Regresion")
            app.input_fecha_nacimiento.set("10/10/1985", True)
            app.input_operadora.set("412")
            app.input_telefono.delete(0, "end"); app.input_telefono.insert(0, "1234567")
            app.input_peso.insert(0, "70")
            app.input_altura.insert(0, "1.75")
            app.input_estado_civil.set(logic.valores_catalogo("estado_civil")[0])
            app.input_genero.set("Masculino")
            app.input_residencia_municipio.set(mun_per)
            app._filtrar_pueblos_residencia()
            app.input_residencia_pueblo.set(pueblo_per)
            app.input_residencia.insert(0, "Calle 9, casa 16")
            app.input_jerarquia.set(logic.valores_catalogo("jerarquia")[0])
            app.input_lugar_servicio.set(logic.valores_catalogo("lugar_servicio")[0])
            app.input_tiempo_servicio.set("10 años")
            app.input_ingreso_mensual.insert(0, "1000,00")

            app.posee_terreno.set("SI")
            app.input_municipio.set(mun_viv)
            app._filtrar_pueblos()
            app.input_pueblo.set(pueblo_viv)
            app.posee_vivienda.set("SI")
            app.input_condicion_vivienda.set(logic.valores_catalogo("condicion_vivienda")[0])
            app.gestion_organismo.set("SI")
            app.organismo_publico.set("Otra")
            app.organismo_privado.set("Otra")
            root.update()
            app.input_organismo_publico_otro.insert(0, "Fundacion X")
            app.input_organismo_privado_otro.insert(0, "Banco Y")
            app.input_fecha_gestion.set("04/11/2026", True)

            app.tenencia_tierra.set("Otra")
            app.input_tenencia_tierra_otra.set("Alquilada")
            app.input_tiempo_ocupacion.set("De 1 a 3 años")

            valores = {
                "input_num_sala": "2", "input_num_sala_comedor": "1",
                "input_num_cocina": "1", "input_num_cocina_comedor": "0",
                "input_num_bano": "2", "input_num_dormitorio": "3",
                "input_num_lavadero": "1", "input_num_patio_terraza": "1",
                "input_num_frente_porche": "0", "input_num_garaje_estacionamiento": "1",
                "input_num_deposito_almacen": "0",
            }
            for attr, val in valores.items():
                set_entry(app, attr, val)

            app.guardar_funcionario()
            root.update()
            assert not avisos["warn"] and not avisos["error"], avisos
            f = next(x for x in logic.cargar_funcionarios(incluir_inactivos=True) if x.cedula == CEDULA_NORM)
            assert f.municipio == mun_viv and f.pueblo == pueblo_viv
            assert f.condicion_vivienda == logic.valores_catalogo("condicion_vivienda")[0]
            assert f.organismo_publico == "Otra" and f.organismo_publico_otro == "Fundacion X"
            assert f.organismo_privado == "Otra" and f.organismo_privado_otro == "Banco Y"
            assert f.fecha_gestion == "04/11/2026"
            assert f.tenencia_tierra == "Otra" and f.tenencia_tierra_otra == "Alquilada"
            assert f.tiempo_ocupacion == "De 1 a 3 años"
            esperado = ("Sala:2, Sala-Comedor:1, Cocina:1, Cocina-Comedor:0, "
                        "Bano:2, Dormitorios:3, Lavadero:1, Patio / Terraza:1, "
                        "Frente / Porche:0, Garaje / Estacionamiento:1, Depósito / Almacén:0")
            assert f.ambiente_vivienda == esperado, f.ambiente_vivienda
            print("guardado integral OK")

            app._cargar_datos_en_formulario(f)
            root.update()
            assert app.input_tiempo_servicio.get() == "10 años"
            assert app.input_ingreso_mensual.get() == "1000.00"
            assert app.input_organismo_publico_otro.get() == "Fundacion X"
            assert app.input_tenencia_tierra_otra.get() == "Alquilada"
            assert app.input_tiempo_ocupacion.get() == "De 1 a 3 años"
            for attr, val in valores.items():
                assert getattr(app, attr).get() == val, (attr, getattr(app, attr).get(), val)
            print("recarga integral OK")

            app.posee_terreno.set("NO")
            app.posee_vivienda.set("NO")
            app.gestion_organismo.set("NO")
            app.tenencia_tierra.set("Propia")
            app.guardar_funcionario()
            root.update()
            assert not avisos["warn"] and not avisos["error"], avisos
            f2 = next(x for x in logic.cargar_funcionarios(incluir_inactivos=True) if x.cedula == CEDULA_NORM)
            assert f2.municipio == "" and f2.pueblo == ""
            assert f2.condicion_vivienda == ""
            assert f2.organismo_publico == "" and f2.organismo_privado == ""
            assert f2.organismo_publico_otro == "" and f2.organismo_privado_otro == ""
            assert f2.fecha_gestion == ""
            assert f2.tenencia_tierra == "Propia" and f2.tenencia_tierra_otra == ""
            assert f2.tiempo_ocupacion == "De 1 a 3 años"
            print("vaciado integral al guardar NO OK")

            f_legacy = logic.Funcionario(
                "V-99999991", "Legacy", "Datos", "10/10/1985", "41", "", "", "",
                "", "")
            f_legacy.plan_vivienda("NO", "", "Buena", mun_viv, pueblo_viv, "Vivienda",
                                   "INAVI", "Entidad Bancaria", "NO", "04/11/2026",
                                   "Vieja X", "Vieja Y")
            f_legacy.estado_vivienda("Propia", "", "2 años", "", "", "")
            f_legacy.tenencia_tierra_otra = "Alquilada"
            f_legacy.ambiente_vivienda = (
                "Sala:15, Sala-Comedor:abc, Cocina:2, Otros:3, Especifique:Patio, "
                "Lavadero:01, Garaje / Estacionamiento:10")
            app._cargar_datos_en_formulario(f_legacy)
            root.update()
            assert app.input_municipio.get() == "" and app.input_pueblo.get() == ""
            assert app.input_condicion_vivienda.get() == ""
            assert app.organismo_publico.get() == "" and app.organismo_privado.get() == ""
            assert app.input_fecha_gestion.get() == ""
            assert app.input_tenencia_tierra_otra.get() == ""
            assert app.input_tiempo_ocupacion.get() == ""
            assert app.input_num_sala.get() == ""
            assert app.input_num_sala_comedor.get() == ""
            assert app.input_num_cocina.get() == "2"
            assert app.input_num_lavadero.get() == "1"
            assert app.input_num_garaje_estacionamiento.get() == "10"
            print("legado y limpieza al abrir OK")

    finally:
        try:
            root.destroy()
        except Exception:
            pass
        limpiar()
        print("limpieza OK")


if __name__ == "__main__":
    main()
