# ⚽ Redes de Pases: ¿Quién es el jugador más importante?

[![QA Pipeline](https://github.com/HugoGALAGA/proyecto_futbol_redes/actions/workflows/qa-pipeline.yml/badge.svg)](https://github.com/HugoGALAGA/proyecto_futbol_redes/actions/workflows/qa-pipeline.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)
![Coverage](https://img.shields.io/badge/coverage-%3E80%25-brightgreen)

Proyecto final de **Matemática Discreta Aplicada** (Universidad Francisco Marroquín, Ciencias de la Computación). Modela un partido de fútbol como una **red** y usa teoría de grafos para responder una pregunta de cualquier aficionado: **¿quién es el jugador más importante de un equipo?**

El repositorio está organizado bajo prácticas de **Shift-Left QA** e **Integración Continua**: cada parte del análisis es un módulo independiente, con pruebas automáticas y un pipeline que bloquea código defectuoso antes de llegar a `main`.

---

## 📑 Contenido

1. [Descripción del proyecto](#-1-descripción-del-proyecto)
2. [Los datos](#-2-los-datos)
3. [Metodología](#-3-metodología)
4. [Estructura del repositorio](#-4-estructura-del-repositorio)
5. [Stack tecnológico](#-5-stack-tecnológico)
6. [Instalación](#-6-instalación)
7. [Uso](#-7-uso)
8. [Estrategia de QA](#-8-estrategia-de-qa)
9. [Pipeline de CI](#-9-pipeline-de-ci)
10. [Flujo de trabajo del equipo](#-10-flujo-de-trabajo-del-equipo)
11. [Nota académica](#-11-nota-académica)
12. [Integrantes y licencia](#-12-integrantes-y-licencia)

---

## 📐 1. Descripción del proyecto

Un partido de fútbol se puede ver como una red:

- Cada **jugador** es un **vértice**.
- Cada **pase** es un **arco** que va del jugador que pasa al que recibe.
- El **peso** de cada conexión es la cantidad de pases entre ambos.

Sobre esa red se analizan dos equipos, el **Equipo A** (formación 4-3-3) y el **Equipo B** (formación 4-4-2), siguiendo cinco partes:

| Parte | Tema | Qué se hace |
|-------|------|-------------|
| 1 | Investigación | Centralidad en redes y NetworkX, con fuentes citadas |
| 2 | Modelo y dibujos | Grafo dirigido y no dirigido ponderado por equipo, dibujados sobre la cancha |
| 3 | Árbol de expansión máximo | Prim (Equipo A, desde el Portero) y Kruskal (Equipo B), trabajados a mano |
| 4 | Centralidad | Grado, fuerza, cercanía e intermediación: a mano sobre el árbol y con NetworkX sobre el grafo completo |
| 5 | Conclusión | Jugador más importante por equipo y comparación entre equipos |

---

## 📊 2. Los datos

Los datos son **ficticios** y fueron diseñados para el curso. Viven en `data/`:

- `data/equipo_A_pases.csv`
- `data/equipo_B_pases.csv`

Cada archivo tiene tres columnas:

| Columna | Significado |
|---------|-------------|
| `origen` | Dorsal del jugador que pasa el balón |
| `destino` | Dorsal del jugador que lo recibe |
| `pases` | Cantidad de veces que ocurrió ese pase durante el partido |

Cada equipo tiene **11 jugadores**, identificados por dorsal y posición. Los dorsales solo sirven para nombrarlos: **no indican jerarquía**.

---

## 🧠 3. Metodología

### Grafos

Por cada equipo se construyen dos grafos ponderados:

- **Dirigido:** hay un arco de `u` a `v` si `u` le pasó el balón a `v`; el peso es el número de pases de `u` a `v`.
- **No dirigido:** hay una arista entre `u` y `v` si hubo pases en alguna dirección; el peso es la suma de los pases de `u` a `v` y de `v` a `u`.

### Árbol de expansión máximo

En clase se busca el árbol de peso **mínimo**. Aquí el peso son pases, así que interesan las conexiones **más fuertes** y se busca el de peso **máximo**. Es el mismo problema cambiando un criterio: se elige siempre la arista más pesada.

- **Kruskal:** ordenar las aristas de mayor a menor peso y agregar cada una si no forma ciclo, hasta tener `n − 1` aristas.
- **Prim:** partir de un vértice y, en cada paso, agregar la arista más pesada que conecte el árbol con un vértice que aún no esté en él.

### Medidas de centralidad

Con `U` el grafo no dirigido, `G` el dirigido y `n = 11`:

- **Grado:** número de jugadores con los que intercambió pases.
- **Fuerza:** suma de los pesos de sus aristas en `U` (total de pases en los que participó).
- **Fuerza de entrada / salida:** pases recibidos / pases hechos en `G`.
- **Cercanía:** `C(v) = (n − 1) / Σ d(v, u)`, con `d` el número mínimo de saltos (sin pesos).
- **Intermediación:** qué tan seguido un jugador está en el camino más corto entre otros dos.

---

## 🗂️ 4. Estructura del repositorio

```text
.
├── .github/
│   └── workflows/
│       └── qa-pipeline.yml     # Pipeline de CI (GitHub Actions)
├── data/                       # CSV de pases de cada equipo
├── docs/
│   ├── test-plan.md            # Plan de pruebas
│   └── test-cases.md           # Casos de prueba
├── informe/                    # Informe PDF, figuras y tablas
├── src/
│   ├── config.py               # Rutas y posiciones en la cancha
│   ├── datos.py                # Lectura y validación de los CSV
│   ├── grafos.py               # Grafos dirigido y no dirigido
│   ├── arbol.py                # Prim y Kruskal (versión máxima)
│   ├── centralidad.py          # Medidas de centralidad
│   └── dibujo.py               # Dibujo de grafos sobre la cancha
├── tests/
│   ├── unit/                   # Pruebas unitarias
│   ├── integration/            # Pruebas de integración entre módulos
│   └── conftest.py             # Fixtures compartidas de pytest
├── .pre-commit-config.yaml     # Gate de calidad antes de cada commit
├── .python-version             # Versión de Python del proyecto
├── pyproject.toml              # Dependencias y configuración de herramientas
└── README.md
```

Cada módulo de `src/` corresponde a una parte del enunciado y se puede probar de forma aislada.

---

## 🛠️ 5. Stack tecnológico

| Herramienta | Uso |
|-------------|-----|
| **Python 3.11+** | Lenguaje principal |
| **uv** | Gestor de entorno y dependencias |
| **NetworkX** | Construcción de grafos y cálculo de medidas |
| **pytest** + **pytest-cov** | Pruebas y cobertura |
| **Hypothesis** | Pruebas basadas en propiedades |
| **Ruff** | Linter y formateador |
| **pre-commit** | Revisión automática antes de cada commit |
| **GitHub Actions** | Integración continua |

---

## 🚀 6. Instalación

Requisito previo: tener [`uv`](https://docs.astral.sh/uv/) instalado.

```bash
# 1. Clonar el repositorio
git clone https://github.com/<USUARIO>/<REPO>.git
cd <REPO>

# 2. Crear el entorno e instalar dependencias (incluye las de desarrollo)
uv sync --group dev

# 3. Activar los hooks de pre-commit
uv run pre-commit install
```

---

## ▶️ 7. Uso

```bash
# Ejecutar todas las pruebas
uv run pytest

# Pruebas con reporte de cobertura
uv run pytest --cov=src --cov-report=term-missing --cov-report=html

# Análisis estático
uv run ruff check .

# Formatear el código
uv run ruff format .
```

El reporte HTML de cobertura queda en `htmlcov/index.html`.

---

## ✅ 8. Estrategia de QA

- **Shift-Left:** los errores se detectan lo antes posible, primero en local con `pre-commit` y luego en cada push con el pipeline.
- **Pruebas unitarias:** validan cada función de forma aislada (lectura de datos, construcción de grafos, algoritmos, medidas).
- **Pruebas de integración:** verifican que los módulos funcionen juntos, de los CSV hasta las tablas finales.
- **Pruebas basadas en propiedades:** con Hypothesis se comprueban invariantes, por ejemplo que un árbol de expansión de `n` vértices tenga exactamente `n − 1` aristas y que no tenga ciclos.
- **Validación cruzada:** los resultados de los algoritmos hechos a mano se contrastan con NetworkX.
- **Quality gates:** el código no se acepta si falla el lint o si la cobertura baja del **80 %**.

La planificación detallada está en `docs/test-plan.md` y `docs/test-cases.md`.

---

## 🔄 9. Pipeline de CI

El workflow `qa-pipeline.yml` se ejecuta en cada *push* a `main` y `dev`, y en cada *pull request* hacia `main`.

| Paso | Qué hace |
|------|----------|
| Checkout | Descarga el código |
| Instalar `uv` | Prepara el gestor de entorno |
| Instalar dependencias | `uv sync --group dev` |
| **Gate estático** | `ruff check .` |
| **Gate dinámico** | `pytest` con cobertura mínima de 80 % |
| Artefacto | Sube el reporte HTML de cobertura |

Si cualquiera de los gates falla, el pipeline se marca en rojo y el cambio no debe fusionarse.

---

## 👥 10. Flujo de trabajo del equipo

1. Trabajar en una rama a partir de `dev`.
2. Hacer commits pequeños; `pre-commit` revisa el código antes de cada uno.
3. Abrir un *pull request* hacia `main` y esperar a que el pipeline pase en verde.
4. Fusionar solo con el pipeline en verde.

---

## 🎓 11. Nota académica

Este repositorio acompaña un proyecto con **informe en PDF** y **evaluación oral individual**. El código está en el Apéndice B del informe. Cada integrante debe poder explicar cualquier parte de lo que se entrega.

---

## 📝 12. Integrantes y licencia

**Integrantes:**

- Hugo Jonathan Daniel Galina Puac

**Curso:** Matemática Discreta Aplicada, Universidad Francisco Marroquín.

Distribuido bajo la licencia incluida en el archivo [`LICENSE`](LICENSE).