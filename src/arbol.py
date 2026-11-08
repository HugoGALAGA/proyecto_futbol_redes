from src.config import EQUIPOS
from src.datos import cargar_pases
from src.grafos import construir_no_dirigido


def _dorsal(equipo, nombre):
    return EQUIPOS[equipo][nombre]["dorsal"]


def _clave(equipo, u, v, w):
    """Mayor peso primero; empate: menor dorsal, luego menor dorsal del otro."""
    a, b = sorted((_dorsal(equipo, u), _dorsal(equipo, v)))
    return (-w, a, b)


def prim_maximo(G, equipo, inicio):
    """Devuelve filas (u, v, peso, acumulado); u está dentro, v es el nuevo."""
    if inicio not in G:
        raise ValueError(f"Vértice inicial inexistente: {inicio}")
    dentro = {inicio}
    acumulado = 0
    filas = []
    while len(dentro) < G.number_of_nodes():
        candidatas = [
            (u, v, d["weight"])
            for u in dentro
            for v, d in G[u].items()
            if v not in dentro
        ]
        if not candidatas:
            raise ValueError("Grafo desconexo")
        u, v, w = min(candidatas, key=lambda e: _clave(equipo, *e))
        dentro.add(v)
        acumulado += w
        filas.append((u, v, w, acumulado))
    return filas


def kruskal_maximo(G, equipo):
    """Devuelve filas (u, v, peso, estado, acumulado); se detiene en n-1 aristas."""
    padre = {n: n for n in G}

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    aristas = sorted(
        ((u, v, d["weight"]) for u, v, d in G.edges(data=True)),
        key=lambda e: _clave(equipo, *e),
    )
    acumulado = 0
    elegidas = 0
    filas = []
    for u, v, w in aristas:
        ru, rv = raiz(u), raiz(v)
        if ru == rv:
            filas.append((u, v, w, "descartada", acumulado))
            continue
        padre[ru] = rv
        acumulado += w
        elegidas += 1
        filas.append((u, v, w, "agregada", acumulado))
        if elegidas == G.number_of_nodes() - 1:
            break
    if elegidas != G.number_of_nodes() - 1:
        raise ValueError("Grafo desconexo")
    return filas


def _imprimir_prim(equipo, filas):
    print(f"Equipo {equipo}: Prim desde el Portero")
    print("Paso | Arista | Peso | Acumulado")
    for i, (u, v, w, acum) in enumerate(filas, start=1):
        a, b = _dorsal(equipo, u), _dorsal(equipo, v)
        print(f"{i:>4} | {a:>2}-{b:<3} | {w:>4} | {acum:>9}")
    print(f"Aristas: {len(filas)}, peso total: {filas[-1][3]}\n")


def _imprimir_kruskal(equipo, filas):
    print(f"Equipo {equipo}: Kruskal")
    print("Arista | Peso | Estado     | Acumulado")
    for u, v, w, estado, acum in filas:
        a, b = _dorsal(equipo, u), _dorsal(equipo, v)
        print(f"{a:>2}-{b:<4} | {w:>4} | {estado:<10} | {acum:>9}")
    agregadas = sum(1 for f in filas if f[3] == "agregada")
    print(f"Aristas: {agregadas}, peso total: {filas[-1][4]}\n")


if __name__ == "__main__":
    UA = construir_no_dirigido("A", cargar_pases("A"))
    UB = construir_no_dirigido("B", cargar_pases("B"))
    _imprimir_prim("A", prim_maximo(UA, "A", "Portero"))
    _imprimir_kruskal("B", kruskal_maximo(UB, "B"))
