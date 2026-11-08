import networkx as nx

from src.config import EQUIPOS


def construir_dirigido(equipo, pases) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_nodes_from(EQUIPOS[equipo])
    for u, v, p in pases:
        G.add_edge(u, v, weight=p)
    return G


def construir_no_dirigido(equipo, pases) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(EQUIPOS[equipo])
    for u, v, p in pases:
        if G.has_edge(u, v):
            G[u][v]["weight"] += p
        else:
            G.add_edge(u, v, weight=p)
    return G
