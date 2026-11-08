import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from src.config import EQUIPOS  # noqa: E402


def posiciones(equipo) -> dict[str, tuple[float, float]]:
    return {n: (d["x"], d["y"]) for n, d in EQUIPOS[equipo].items()}


def _cancha(ax):
    ax.add_patch(Rectangle((0, 0), 100, 100, fill=False, ec="black", lw=2))
    ax.axvline(50, color="black", lw=1)
    ax.set_xlim(-2, 102)
    ax.set_ylim(-2, 102)
    ax.axis("off")


def _nodos(G, equipo, pos, ax):
    nx.draw_networkx_nodes(
        G, pos, node_size=700, node_color="#9ecae1", edgecolors="black", ax=ax
    )
    dorsales = {n: EQUIPOS[equipo][n]["dorsal"] for n in G.nodes}
    nx.draw_networkx_labels(
        G, pos, labels=dorsales, font_size=11, font_weight="bold", ax=ax
    )
    for n, (x, y) in pos.items():
        ax.text(x, y - 5, n, ha="center", va="top", fontsize=7)


def dibujar_no_dirigido(G, equipo, ruta):
    pos = posiciones(equipo)
    fig, ax = plt.subplots(figsize=(12, 8))
    _cancha(ax)
    nx.draw_networkx_edges(G, pos, edge_color="gray", ax=ax)
    _nodos(G, equipo, pos, ax)
    etiquetas = {(u, v): w for u, v, w in G.edges(data="weight")}
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=etiquetas,
        font_size=7,
        ax=ax,
        bbox=dict(boxstyle="round", fc="white", ec="none", alpha=0.85),
    )
    fig.savefig(ruta, dpi=200, bbox_inches="tight")
    plt.close(fig)


def dibujar_dirigido(G, equipo, ruta):
    pos = posiciones(equipo)
    fig, ax = plt.subplots(figsize=(12, 8))
    _cancha(ax)
    w_max = max(w for _, _, w in G.edges(data="weight"))
    anchos = [0.5 + 3 * w / w_max for _, _, w in G.edges(data="weight")]
    nx.draw_networkx_edges(
        G,
        pos,
        width=anchos,
        arrows=True,
        arrowstyle="-|>",
        connectionstyle="arc3,rad=0.15",
        edge_color="gray",
        node_size=700,
        ax=ax,
    )
    _nodos(G, equipo, pos, ax)
    fig.savefig(ruta, dpi=200, bbox_inches="tight")
    plt.close(fig)


def tabla_pases(pases) -> list[tuple]:
    return sorted(pases, key=lambda t: (-t[2], t[0], t[1]))
