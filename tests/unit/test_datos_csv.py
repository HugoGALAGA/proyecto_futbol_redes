import csv
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

DATA = Path(__file__).resolve().parents[2] / "data"
ARCHIVOS = ["equipo_A_pases.csv", "equipo_B_pases.csv"]


def _leer(archivo: str) -> list[dict]:
    with open(DATA / archivo, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


@pytest.mark.parametrize("archivo", ARCHIVOS)
def test_columnas_esperadas(archivo):
    filas = _leer(archivo)
    assert set(filas[0].keys()) == {"origen", "destino", "pases"}


@pytest.mark.parametrize("archivo", ARCHIVOS)
def test_dorsales_y_pases_validos(archivo):
    for fila in _leer(archivo):
        assert 1 <= int(fila["origen"]) <= 11
        assert 1 <= int(fila["destino"]) <= 11
        assert int(fila["pases"]) > 0