#!/usr/bin/env python3
"""Sincroniza los catalogos desde produccion hacia la BD de prueba.

Copia el contenido de 'catalogos' y 'operadora_prefijos' de funcionarios.db a
funcionarios_prueba.db. Antes de escribir crea un respaldo de la BD de prueba.

Uso:
    python3 scripts/sync_catalogs.py --dry-run   # solo muestra diferencias
    python3 scripts/sync_catalogs.py             # aplica los cambios
"""
import argparse
import datetime
import os
import shutil
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "src", "data")
PROD = os.path.join(DATA_DIR, "funcionarios.db")
TEST = os.path.join(DATA_DIR, "funcionarios_prueba.db")

TABLES = {
    "catalogos": ("tipo", "valor", "detalle", "orden", "activo"),
    "operadora_prefijos": ("prefijo", "operadora"),
}


def read_rows(conn, table, cols):
    cur = conn.cursor()
    query = f"SELECT {', '.join(cols)} FROM '{table}' ORDER BY 1, 2"
    return [tuple(r) for r in cur.execute(query)]


def main():
    parser = argparse.ArgumentParser(description="Sincroniza catalogos prod -> test")
    parser.add_argument("--dry-run", action="store_true", help="solo mostrar diferencias")
    args = parser.parse_args()

    faltan = [p for p in (PROD, TEST) if not os.path.exists(p)]
    if faltan:
        print("Faltan bases de datos: " + ", ".join(faltan))
        return 1

    source = sqlite3.connect(f"file:{PROD}?mode=ro", uri=True)
    data = {}
    try:
        for table, cols in TABLES.items():
            try:
                data[table] = read_rows(source, table, cols)
            except sqlite3.OperationalError:
                print(f"ERROR: la tabla '{table}' no existe en produccion.")
                return 1
    finally:
        source.close()

    if args.dry_run:
        target = sqlite3.connect(f"file:{TEST}?mode=ro", uri=True)
        try:
            for table, cols in TABLES.items():
                if table not in {
                    r[0]
                    for r in target.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    )
                }:
                    print(f"[dry-run] '{table}' no existe en la BD de prueba (requiere migracion).")
                    continue
                actual = read_rows(target, table, cols)
                if actual == data[table]:
                    print(f"[dry-run] '{table}': sin cambios ({len(actual)} filas).")
                else:
                    print(
                        f"[dry-run] '{table}': prod={len(data[table])} filas, "
                        f"test={len(actual)} filas (se reemplazaria)."
                    )
        finally:
            target.close()
        return 0

    backup = TEST + ".bak-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(TEST, backup)

    conn = sqlite3.connect(TEST)
    try:
        for table, cols in TABLES.items():
            existe = conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
            ).fetchone()
            if not existe:
                conn.rollback()
                print(
                    f"ERROR: la tabla '{table}' no existe en la BD de prueba.\n"
                    "Ejecuta primero la migracion (abre la app con DB_MODE=test)."
                )
                return 1
            conn.execute(f"DELETE FROM '{table}'")
            placeholders = ", ".join("?" for _ in cols)
            conn.executemany(
                f"INSERT INTO '{table}' ({', '.join(cols)}) VALUES ({placeholders})",
                data[table],
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    print(f"Sincronizacion completada. Respaldo: {backup}")
    for table in TABLES:
        print(f"  {table}: {len(data[table])} filas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
