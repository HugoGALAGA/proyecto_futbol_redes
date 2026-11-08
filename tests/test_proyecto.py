import networkx as nx
import pytest

from src import datos
from src.arbol import (
    _imprimir_kruskal,
    _imprimir_prim,
    kruskal_maximo,
    prim_maximo,
)
from src.centralidad import (
    _imprimir,
    _imprimir_arbol,
    construir_arbol,
    tabla_arbol,
    tabla_completa,
)
from src.config import EQUIPOS
from src.datos import cargar_pases
from src.dibujo import (
    dibujar_dirigido,
    dibujar_no_dirigido,
    posiciones,
    tabla_pases,
)
from src.grafos import construir_dirigido, construir_no_dirigido

ENCABEZADO = "origen,destino,pases\n"


def _grafos(equipo):
    pases = cargar_pases(equipo)
    D = construir_dirigido(equipo, pases)
    U = construir_no_dirigido(equipo, pases)
    return pases, D, U


# ---------- datos ----------
def test_cargar_pases_cantidades():
    assert len(cargar_pases("A")) == 51
    assert len(cargar_pases("B")) == 62


def test_archivo_inexistente(tmp_path, monkeypatch):
    monkeypatch.setattr(datos, "DATA", tmp_path)
    with pytest.raises(FileNotFoundError):
        datos.cargar_pases("A")


def test_columnas_invalidas(tmp_path, monkeypatch):
    (tmp_path / "equipo_A_pases.csv").write_text("a,b,c\n", encoding="utf-8")
    monkeypatch.setattr(datos, "DATA", tmp_path)
    with pytest.raises(ValueError):
        datos.cargar_pases("A")


@pytest.mark.parametrize(
    "fila",
    [
        "Portero,Lateral derecho,0",
        "Portero,Lateral derecho,-3",
        "Portero,Lateral derecho,x",
        "Fantasma,Lateral derecho,3",
        "Portero,Portero,3",
        "Portero,Lateral derecho,3\nPortero,Lateral derecho,4",
    ],
)
def test_filas_invalidas(tmp_path, monkeypatch, fila):
    (tmp_path / "equipo_A_pases.csv").write_text(
        ENCABEZADO + fila + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(datos, "DATA", tmp_path)
    with pytest.raises(ValueError):
        datos.cargar_pases("A")


# ---------- grafos ----------
@pytest.mark.parametrize("equipo, arcos, aristas", [("A", 51, 28), ("B", 62, 37)])
def test_grafos_tamanos(equipo, arcos, aristas):
    pases, D, U = _grafos(equipo)
    assert D.number_of_nodes() == U.number_of_nodes() == 11
    assert D.number_of_edges() == arcos
    assert U.number_of_edges() == aristas
    suma_d = sum(w for *_, w in D.edges(data="weight"))
    suma_u = sum(w for *_, w in U.edges(data="weight"))
    assert suma_d == suma_u == sum(p for *_, p in pases)


def test_no_dirigido_suma_ida_y_vuelta():
    _, _, U = _grafos("A")
    assert U["Portero"]["Defensa central derecho"]["weight"] == 12


# ---------- árboles ----------
def test_prim_equipo_a():
    _, _, U = _grafos("A")
    filas = prim_maximo(U, "A", "Portero")
    assert len(filas) == 10
    assert filas[-1][3] == 153


def test_kruskal_equipo_b():
    _, _, U = _grafos("B")
    filas = kruskal_maximo(U, "B")
    agregadas = [f for f in filas if f[3] == "agregada"]
    assert len(agregadas) == 10
    assert filas[-1][4] == 138
    assert any(f[3] == "descartada" for f in filas)


def test_prim_inicio_invalido():
    _, _, U = _grafos("A")
    with pytest.raises(ValueError):
        prim_maximo(U, "A", "Fantasma")


def test_arboles_desconexos():
    G = nx.Graph()
    G.add_nodes_from(EQUIPOS["A"])
    G.add_edge("Portero", "Lateral derecho", weight=3)
    with pytest.raises(ValueError):
        prim_maximo(G, "A", "Portero")
    with pytest.raises(ValueError):
        kruskal_maximo(G, "A")


def test_imprimir_arboles(capsys):
    _, _, UA = _grafos("A")
    _, _, UB = _grafos("B")
    _imprimir_prim("A", prim_maximo(UA, "A", "Portero"))
    _imprimir_kruskal("B", kruskal_maximo(UB, "B"))
    salida = capsys.readouterr().out
    assert "153" in salida and "138" in salida


# ---------- centralidad ----------
def test_fuerza_igual_entrada_mas_salida():
    _, D, U = _grafos("A")
    for f in tabla_completa(U, D):
        assert f["fuerza"] == f["f_entrada"] + f["f_salida"]


def test_tabla_ordenada_por_fuerza():
    _, D, U = _grafos("B")
    fuerzas = [f["fuerza"] for f in tabla_completa(U, D)]
    assert fuerzas == sorted(fuerzas, reverse=True)


def test_arbol_grados_suman_20(capsys):
    _, D, U = _grafos("A")
    filas = prim_maximo(U, "A", "Portero")
    T = construir_arbol(U, [(u, v, w) for u, v, w, _ in filas])
    datos_arbol = tabla_arbol(T)
    assert sum(g for _, g, _ in datos_arbol) == 20
    _imprimir("A", tabla_completa(U, D))
    _imprimir_arbol("A", datos_arbol)
    assert "Dorsal" in capsys.readouterr().out


# ---------- dibujo ----------
def test_posiciones_y_tabla():
    assert len(posiciones("A")) == 11
    pases = cargar_pases("A")
    ordenada = tabla_pases(pases)
    assert ordenada[0][2] == max(p for *_, p in pases)


def test_dibujos_generan_archivo(tmp_path):
    _, D, U = _grafos("A")
    dibujar_dirigido(D, "A", tmp_path / "d.png")
    dibujar_no_dirigido(U, "A", tmp_path / "u.png")
    assert (tmp_path / "d.png").exists()
    assert (tmp_path / "u.png").exists()
