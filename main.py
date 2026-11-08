from pathlib import Path

from src.datos import cargar_pases
from src.dibujo import dibujar_dirigido, dibujar_no_dirigido
from src.grafos import construir_dirigido, construir_no_dirigido

SALIDA = Path("informe/figuras")
SALIDA.mkdir(parents=True, exist_ok=True)

for eq in ("A", "B"):
    pases = cargar_pases(eq)
    D = construir_dirigido(eq, pases)
    U = construir_no_dirigido(eq, pases)
    print(
        eq,
        D.number_of_edges(),
        U.number_of_edges(),
        sum(p for *_, p in pases),
        sum(w for *_, w in U.edges(data="weight")),
    )
    dibujar_dirigido(D, eq, SALIDA / f"equipo_{eq}_dirigido.png")
    dibujar_no_dirigido(U, eq, SALIDA / f"equipo_{eq}_no_dirigido.png")
