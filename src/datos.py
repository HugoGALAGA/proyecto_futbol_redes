import csv
from pathlib import Path

from src.config import EQUIPOS

DATA = Path(__file__).resolve().parents[1] / "data"
COLUMNAS = ["origen", "destino", "pases"]


def cargar_pases(equipo: str) -> list[tuple[str, str, int]]:
    ruta = DATA / f"equipo_{equipo}_pases.csv"
    nombres = EQUIPOS[equipo]
    pases = []
    vistos = set()

    with open(ruta, encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        if lector.fieldnames != COLUMNAS:
            raise ValueError(f"Columnas inválidas: {lector.fieldnames}")

        for fila in lector:
            origen = fila["origen"].strip()
            destino = fila["destino"].strip()
            cantidad = int(fila["pases"])
            if cantidad <= 0:
                raise ValueError(f"Pases debe ser positivo: {cantidad}")
            if origen not in nombres or destino not in nombres:
                raise ValueError(f"Jugador desconocido: {origen} -> {destino}")
            if origen == destino:
                raise ValueError(f"Origen igual a destino: {origen}")
            if (origen, destino) in vistos:
                raise ValueError(f"Par repetido: {origen} -> {destino}")
            vistos.add((origen, destino))
            pases.append((origen, destino, cantidad))

    return pases
