# Plan de Pruebas

Proyecto: Redes de pases, ¿quién es el jugador más importante?
Curso: Matemática Discreta Aplicada (UFM)

## 1. Objetivo

Asegurar que cada etapa del análisis (lectura de datos, grafos, árbol de expansión máximo, centralidad y dibujo) produzca resultados correctos, reproducibles y verificables contra el enunciado y contra NetworkX, **antes** de que el código llegue a `main`.

## 2. Alcance

**Dentro del alcance**
- Lectura y validación de `data/equipo_A_pases.csv` y `data/equipo_B_pases.csv`.
- Construcción del grafo dirigido y no dirigido ponderado de cada equipo.
- Algoritmos de Prim y Kruskal en su versión de peso máximo.
- Medidas de centralidad calculadas a mano y con NetworkX.
- Generación de dibujos sobre la cancha (verificación de estructura, no de estética).

**Fuera del alcance**
- Calidad visual de los dibujos (se revisa manualmente).
- Redacción del informe y respuestas interpretativas.

## 3. Estrategia por niveles

| Nivel | Marker | Qué verifica |
|-------|--------|--------------|
| Unitario | `unit` | Cada función con entradas pequeñas y resultados calculados a mano |
| Integración | `integration` | Flujo completo CSV → grafos → árbol → centralidad → tabla |
| Propiedades | `property` | Invariantes sobre grafos aleatorios (Hypothesis) |
| Validación cruzada | `unit` / `integration` | Implementación propia contra NetworkX |
| Aceptación | `integration` | Valores de referencia del enunciado (árbol A = 153, árbol B = 138) |

## 4. Módulos bajo prueba

| Módulo | Responsabilidad | Pruebas principales |
|--------|-----------------|---------------------|
| `config.py` | Posiciones, dorsales y coordenadas en cancha | Unitarias |
| `datos.py` | Leer y validar los CSV | Unitarias (casos válidos e inválidos) |
| `grafos.py` | Grafo dirigido y no dirigido | Unitarias, propiedades |
| `arbol.py` | Prim y Kruskal de peso máximo | Unitarias, propiedades, aceptación |
| `centralidad.py` | Grado, fuerza, cercanía, intermediación | Unitarias, validación cruzada |
| `dibujo.py` | Figuras sobre la cancha | Estructurales (humo) |

## 5. Datos de prueba

1. **Reales:** los dos CSV de `data/`. Los jugadores se identifican por nombre de posición (por ejemplo `Portero`), no por dorsal.
2. **Sintético mínimo (fixture en `conftest.py`):** grafo de 4 jugadores con resultados calculables a mano (ver `test-cases.md`, sección Fixture).
3. **Valores de referencia del enunciado:** peso del árbol A = 153, peso del árbol B = 138, y la arista de mayor peso siempre pertenece al árbol.
4. **Aleatorios:** grafos conexos generados con Hypothesis.

## 6. Criterios de entrada y salida

**Entrada (empezar a probar un módulo):** el caso de prueba está escrito en `test-cases.md` antes de implementar la función.

**Salida (módulo terminado):**
- Todos sus casos pasan.
- `ruff check` y `ruff format --check` sin errores.
- Cobertura global ≥ 80 %.
- Pipeline en verde en el pull request.

## 7. Entorno y herramientas

Python 3.11, `uv`, `pytest`, `pytest-cov`, `hypothesis`, `ruff`, `pre-commit`, GitHub Actions. Los dibujos se prueban con el backend `Agg` de matplotlib (sin ventana).

## 8. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Empates de peso hacen que Prim y Kruskal den árboles distintos | Comparar **peso total**, no aristas exactas, y documentar el desempate |
| Confundir normalización entre cálculo manual y NetworkX | Fijar el parámetro `normalized` de forma explícita y probar ambos |
| Nombres de posición con espacios o tildes distintas | Normalizar con `strip()` y validar contra `config.py` |
| Resultado correcto por casualidad | Validación cruzada con NetworkX y fixture calculado a mano |
| Cobertura inflada por módulos vacíos | Revisar el reporte HTML por módulo, no solo el total |

## 9. Trazabilidad con el enunciado

| Parte del enunciado | Módulos | Casos |
|---------------------|---------|-------|
| Parte 2: modelo y dibujos | `datos`, `grafos`, `dibujo`, `config` | TC-DAT, TC-CFG, TC-GRA, TC-DIB |
| Parte 3: árbol de expansión máximo | `arbol` | TC-ARB |
| Parte 4: centralidad | `centralidad` | TC-CEN |
| Todas | todos | TC-INT, TC-CI |

## 10. Orden de trabajo

1. `config` y `datos`
2. `grafos`
3. `arbol`
4. `centralidad`
5. `dibujo`
6. Pruebas de integración y revisión de cobertura

Cada paso se trabaja en una rama desde `dev` y se fusiona con pull request.