import networkx as nx

from src.arbol import kruskal_maximo, prim_maximo
from src.config import EQUIPOS
from src.datos import cargar_pases
from src.grafos import construir_dirigido, construir_no_dirigido


def construir_arbol(U, aristas):
    T = nx.Graph()
    T.add_nodes_from(U)
    for u, v, w in aristas:
        T.add_edge(u, v, weight=w)
    return T


def tabla_completa(U, D):
    cercania = nx.closeness_centrality(U)
    intermediacion = nx.betweenness_centrality(U)
    filas = []
    for n in U:
        filas.append(
            {
                "jugador": n,
                "fuerza": U.degree(n, weight="weight"),
                "grado": U.degree(n),
                "cercania": cercania[n],
                "intermediacion": intermediacion[n],
                "f_entrada": D.in_degree(n, weight="weight"),
                "f_salida": D.out_degree(n, weight="weight"),
            }
        )
    return sorted(filas, key=lambda f: -f["fuerza"])


def tabla_arbol(T):
    cercania = nx.closeness_centrality(T)
    return [(n, T.degree(n), cercania[n]) for n in T]


def _imprimir(equipo, filas):
    print(f"Equipo {equipo}: grafo completo (ordenado por fuerza)")
    print("Dorsal | Fuerza | Grado | Cercanía | Interm. | F.entrada | F.salida")
    for f in filas:
        d = EQUIPOS[equipo][f["jugador"]]["dorsal"]
        print(
            f"{d:>6} | {f['fuerza']:>6} | {f['grado']:>5} | "
            f"{f['cercania']:>8.3f} | {f['intermediacion']:>7.3f} | "
            f"{f['f_entrada']:>9} | {f['f_salida']:>8}"
        )
    print()


def _imprimir_arbol(equipo, filas):
    print(f"Equipo {equipo}: árbol")
    print("Dorsal | Grado | Cercanía")
    for n, g, c in sorted(filas, key=lambda f: EQUIPOS[equipo][f[0]]["dorsal"]):
        d = EQUIPOS[equipo][n]["dorsal"]
        print(f"{d:>6} | {g:>5} | {c:>8.3f}")
    print()


if __name__ == "__main__":
    for eq in ("A", "B"):
        pases = cargar_pases(eq)
        U = construir_no_dirigido(eq, pases)
        D = construir_dirigido(eq, pases)
        if eq == "A":
            filas = prim_maximo(U, eq, "Portero")
            aristas = [(u, v, w) for u, v, w, _ in filas]
        else:
            filas = kruskal_maximo(U, eq)
            aristas = [(u, v, w) for u, v, w, e, _ in filas if e == "agregada"]
        T = construir_arbol(U, aristas)
        _imprimir(eq, tabla_completa(U, D))
        _imprimir_arbol(eq, tabla_arbol(T))

if __name__ == "__main__":  # pragma: no cover
    for eq in ("A", "B"):
        ...
