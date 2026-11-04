# Casos de Prueba

Estado: ✅ implementado · ⬜ pendiente

## Fixture: grafo mínimo de 4 jugadores

Pases dirigidos (origen → destino: pases):

```text
P1 → P2: 5     P2 → P1: 2     P2 → P3: 4
P3 → P4: 6     P4 → P2: 1     P1 → P4: 3
```

Valores calculados a mano:

```text
No dirigido: P1-P2=7, P2-P3=4, P3-P4=6, P2-P4=1, P1-P4=3  (suma = 21)
Grado:       P1=2, P2=3, P3=2, P4=3
Fuerza:      P1=10, P2=12, P3=10, P4=10  (suma = 42 = 2 x 21)
Fuerza salida P1=8, entrada P1=2
Árbol máximo: P1-P2 (7), P3-P4 (6), P2-P3 (4)  -> peso 17, camino P1-P2-P3-P4
Cercanía en el árbol: P1=0.50, P2=0.75, P3=0.75, P4=0.50
```

## Datos (`datos.py`)

| ID | Tipo | Descripción | Resultado esperado | Estado |
|----|------|-------------|--------------------|--------|
| TC-DAT-01 | unit | Leer equipo A | 51 registros (verificar con `wc -l`) | ⬜ |
| TC-DAT-02 | unit | Columnas del CSV | `origen`, `destino`, `pases` | ✅ |
| TC-DAT-03 | unit | Jugadores distintos | Exactamente 11 por equipo | ✅ |
| TC-DAT-04 | unit | Pases válidos | Enteros > 0 y nombres no vacíos | ✅ |
| TC-DAT-05 | unit | Archivo inexistente | `FileNotFoundError` | ⬜ |
| TC-DAT-06 | unit | Columnas faltantes o distintas | `ValueError` | ⬜ |
| TC-DAT-07 | unit | `pases` no numérico, cero o negativo | `ValueError` | ⬜ |
| TC-DAT-08 | unit | Jugador que no existe en la formación | `ValueError` | ⬜ |
| TC-DAT-09 | unit | Auto-pase (`origen == destino`) | `ValueError` | ⬜ |
| TC-DAT-10 | unit | Par origen-destino duplicado | `ValueError` | ⬜ |
| TC-DAT-11 | unit | Espacios sobrantes en nombres | Se normalizan con `strip()` | ⬜ |

## Configuración (`config.py`)

| ID | Tipo | Descripción | Resultado esperado | Estado |
|----|------|-------------|--------------------|--------|
| TC-CFG-01 | unit | Formaciones | 11 posiciones únicas por equipo, dorsales 1 a 11 | ⬜ |
| TC-CFG-02 | unit | Mapeo posición → dorsal | Biyectivo y coincide con la tabla del enunciado | ⬜ |
| TC-CFG-03 | unit | Posiciones de los CSV | Todas existen en la configuración del equipo | ⬜ |
| TC-CFG-04 | unit | Coordenadas en cancha | 11 por equipo, sin pares repetidos | ⬜ |

## Grafos (`grafos.py`)

| ID | Tipo | Descripción | Resultado esperado | Estado |
|----|------|-------------|--------------------|--------|
| TC-GRA-01 | unit | Fixture, grafo dirigido | 6 arcos con los pesos indicados | ⬜ |
| TC-GRA-02 | unit | Fixture, arista con pases en ambos sentidos | P1-P2 pesa 7 | ⬜ |
| TC-GRA-03 | unit | Fixture, arista con un solo sentido | P3-P4 pesa 6 | ⬜ |
| TC-GRA-04 | unit | Tipos de grafo | `DiGraph` para dirigido, `Graph` para no dirigido | ⬜ |
| TC-GRA-05 | integration | Equipo A completo | 11 vértices, 51 arcos, 28 aristas | ⬜ |
| TC-GRA-06 | integration | Peso de arco real | Portero → Defensa central derecho = 8 | ⬜ |
| TC-GRA-07 | integration | Conservación de pases (A) | Suma de pesos dirigido = no dirigido = 270 | ⬜ |
| TC-GRA-08 | integration | Conexidad | El no dirigido de A y de B es conexo | ⬜ |
| TC-GRA-09 | property | Matrices aleatorias | Suma de pesos igual en ambos grafos; aristas ≤ arcos | ⬜ |

## Árbol de expansión máximo (`arbol.py`)

| ID | Tipo | Descripción | Resultado esperado | Estado |
|----|------|-------------|--------------------|--------|
| TC-ARB-01 | unit | Fixture con Kruskal | Peso 17, aristas P1-P2, P3-P4, P2-P3 | ⬜ |
| TC-ARB-02 | unit | Fixture con Prim desde P1 | Mismo peso 17 y mismo conjunto de aristas | ⬜ |
| TC-ARB-03 | integration | Número de aristas | 10 en A y en B (n − 1) | ⬜ |
| TC-ARB-04 | integration | Estructura | `nx.is_tree` verdadero | ⬜ |
| TC-ARB-05 | integration | Aceptación equipo A | Prim desde el Portero da peso 153 | ⬜ |
| TC-ARB-06 | integration | Aceptación equipo B | Kruskal da peso 138 | ⬜ |
| TC-ARB-07 | integration | Arista de mayor peso | Pertenece al árbol (A: Volante de contención – Volante interior derecho, 22) | ⬜ |
| TC-ARB-08 | integration | Consistencia entre algoritmos | Prim y Kruskal dan igual peso total en A y en B | ⬜ |
| TC-ARB-09 | integration | Validación cruzada | Peso propio = peso de `nx.maximum_spanning_tree` | ⬜ |
| TC-ARB-10 | unit | Grafo desconexo | `ValueError` | ⬜ |
| TC-ARB-11 | unit | Vértice inicial inexistente en Prim | `ValueError` | ⬜ |
| TC-ARB-12 | unit | Tabla de Kruskal | Incluye aristas descartadas; último acumulado = peso total | ⬜ |
| TC-ARB-13 | unit | Empates de peso | Resultado determinista con desempate documentado | ⬜ |
| TC-ARB-14 | property | Grafos conexos aleatorios | Prim, Kruskal y NetworkX dan el mismo peso; n − 1 aristas | ⬜ |

## Centralidad (`centralidad.py`)

| ID | Tipo | Descripción | Resultado esperado | Estado |
|----|------|-------------|--------------------|--------|
| TC-CEN-01 | unit | Grado en fixture | P1=2, P2=3, P3=2, P4=3 | ⬜ |
| TC-CEN-02 | unit | Fuerza en fixture | P1=10, P2=12, P3=10, P4=10 | ⬜ |
| TC-CEN-03 | unit | Fuerza entrada y salida en fixture | P1: salida 8, entrada 2 | ⬜ |
| TC-CEN-04 | unit | Cercanía en el árbol del fixture | 0.50, 0.75, 0.75, 0.50 | ⬜ |
| TC-CEN-05 | integration | Cercanía manual contra NetworkX (árbol) | Iguales con tolerancia 1e-9; diferencias documentadas | ⬜ |
| TC-CEN-06 | integration | Grado manual contra NetworkX (árbol) | Iguales | ⬜ |
| TC-CEN-07 | integration | Conservación de fuerzas | Suma de fuerzas = 2 × suma de pesos; entrada total = salida total = 270 (A) | ⬜ |
| TC-CEN-08 | integration | Portero del equipo A | Grado 5, fuerza 30, salida 23, entrada 7 | ⬜ |
| TC-CEN-09 | unit | Intermediación | Valores en [0, 1] con `normalized=True`; hojas del árbol = 0 | ⬜ |
| TC-CEN-10 | integration | Tabla final | 11 filas, columnas esperadas, ordenada por fuerza descendente | ⬜ |
| TC-CEN-11 | unit | Cercanía en grafo desconexo | Comportamiento definido y documentado | ⬜ |

## Dibujo (`dibujo.py`)

| ID | Tipo | Descripción | Resultado esperado | Estado |
|----|------|-------------|--------------------|--------|
| TC-DIB-01 | unit | Posiciones | 11 nodos con coordenadas dentro de la cancha | ⬜ |
| TC-DIB-02 | unit | Grafo dirigido | Se genera la figura sin error (backend `Agg`) | ⬜ |
| TC-DIB-03 | unit | Grafo no dirigido | Una etiqueta de peso por arista | ⬜ |
| TC-DIB-04 | unit | Guardado | PNG creado en `tmp_path` con tamaño > 0 | ⬜ |
| TC-DIB-05 | unit | Árbol resaltado | 10 aristas resaltadas | ⬜ |

## Integración y CI

| ID | Tipo | Descripción | Resultado esperado | Estado |
|----|------|-------------|--------------------|--------|
| TC-INT-01 | integration | Flujo completo equipo A | CSV → grafos → árbol → tabla de 11 filas sin errores | ⬜ |
| TC-INT-02 | integration | Flujo completo equipo B | Igual que TC-INT-01 | ⬜ |
| TC-INT-03 | integration | Reproducibilidad | Dos ejecuciones dan resultados idénticos | ⬜ |
| TC-CI-01 | gate | Pull request hacia `main` | Pipeline en verde y cobertura ≥ 80 % | ⬜ |