#!/usr/bin/env python3
"""Compara el esquema y los catalogos entre la BD de produccion y la de prueba.

Solo lectura: no modifica ninguna base de datos.
Devuelve codigo 0 si son consistentes y 1 si hay diferencias.
"""
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "src", "data")
PROD = os.path.join(DATA_DIR, "funcionarios.db")
TEST = os.path.join(DATA_DIR, "funcionarios_prueba.db")

CATALOG_TABLES = {
    "catalogos": ("tipo", "valor", "detalle", "orden", "activo"),
    "operadora_prefijos": ("prefijo", "operadora"),
}


def connect(path):
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


def tables(conn):
    cur = conn.cursor()
    return {
        r[0]
        for r in cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    }


def columns(conn, table):
    """Devuelve {nombre: (tipo, notnull, default, pk)} sin depender del orden."""
    cur = conn.cursor()
    return {
        r[1]: (r[2], r[3], r[4], r[5])
        for r in cur.execute(f"PRAGMA table_info('{table}')")
    }


def read_rows(conn, table, cols):
    cur = conn.cursor()
    query = f"SELECT {', '.join(cols)} FROM '{table}' ORDER BY 1, 2"
    return [tuple(r) for r in cur.execute(query)]


def compare_schema(prod, test):
    diffs = []
    tp, tt = tables(prod), tables(test)
    if tp != tt:
        if tp - tt:
            diffs.append(f"Tablas solo en prod: {sorted(tp - tt)}")
        if tt - tp:
            diffs.append(f"Tablas solo en test: {sorted(tt - tp)}")

    for table in sorted(tp & tt):
        cp, ct = columns(prod, table), columns(test, table)
        if cp != ct:
            diffs.append(f"Columnas distintas en '{table}':")
            if cp.keys() - ct.keys():
                diffs.append(f"  solo prod: {sorted(cp.keys() - ct.keys())}")
            if ct.keys() - cp.keys():
                diffs.append(f"  solo test: {sorted(ct.keys() - cp.keys())}")
            for name in sorted(cp.keys() & ct.keys()):
                if cp[name] != ct[name]:
                    diffs.append(f"  '{name}': prod={cp[name]} test={ct[name]}")
    return diffs


def compare_catalogs(prod, test):
    diffs = []
    for table, cols in CATALOG_TABLES.items():
        in_prod = table in tables(prod)
        in_test = table in tables(test)
        if not in_prod or not in_test:
            donde = "prod" if not in_prod else "test"
            diffs.append(f"Tabla '{table}' no existe en {donde}")
            continue
        rp = read_rows(prod, table, cols)
        rt = read_rows(test, table, cols)
        if rp != rt:
            diffs.append(f"Catalogo '{table}' difiere ({len(rp)} filas prod vs {len(rt)} test)")
            solo_prod = [r for r in rp if r not in rt]
            solo_test = [r for r in rt if r not in rp]
            if solo_prod:
                diffs.append(f"  solo prod: {solo_prod}")
            if solo_test:
                diffs.append(f"  solo test: {solo_test}")
    return diffs


def main():
    faltan = [p for p in (PROD, TEST) if not os.path.exists(p)]
    if faltan:
        print("Faltan bases de datos: " + ", ".join(faltan))
        return 1

    prod, test = connect(PROD), connect(TEST)
    try:
        diffs = compare_schema(prod, test) + compare_catalogs(prod, test)
    finally:
        prod.close()
        test.close()

    if diffs:
        print("INCONGRUENCIAS ENCONTRADAS:")
        for d in diffs:
            print(" -", d)
        return 1

    print("OK: esquema y catalogos consistentes entre prod y test.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
