# EfiRuta

Programa en Python que arma las rutas de los buses escolares de un colegio de Bogotá:
reparte a los estudiantes entre los buses sin pasar los puestos disponibles y calcula el
recorrido de la mañana y el de la tarde, minimizando una combinación de distancia (0.8) y
tiempo (0.2).

Proyecto integrador de **Diseño y Análisis de Algoritmos (DDYA)** — Escuela Colombiana de
Ingeniería Julio Garavito, grupo 05, tercer tercio de 2026-2.

## Equipo

| Integrante | Rol | Responsabilidad principal |
|---|---|---|
| Santiago Andres Torres Alvarez | Líder / integrante | Grafo vial, caminos mínimos y optimización de rutas. |
| Thomas Steban Venegas Castañeda | Integrante | Tabla hash para estudiantes, simulación de recorridos e interfaz del MVP. |
| Diego Prado Pardo | Integrante | Árbol de expansión mínimo, conjuntos disjuntos y suite de pruebas. Responsable del control de versiones del repositorio. |

## El caso

Un colegio de Bogotá con servicio de buses. Hoy las rutas se arman a mano. Con 20
estudiantes, recogerlos en el orden de inscripción da 70.3 km y 155 minutos de bus; cuando
entra un estudiante o cierran una calle hay que rehacerlas, y los padres no saben por dónde
va el bus.

- **Cliente:** el colegio.
- **Usuarios:** el coordinador de transporte, que arma las rutas, y los padres de familia, que consultan el recorrido de sus hijos.
- **Beneficiarios:** los estudiantes.

## Resultados del caso principal

| Métrica | Orden de inscripción | EfiRuta |
|---|---|---|
| Distancia total | 70.3 km | **22.2 km** |
| Tiempo total | 155.4 min | **64.0 min** |
| Costo ponderado | 120.86 | **38.68** |

- 20 estudiantes, 3 buses (8 / 7 / 7 puestos), 36 esquinas y 54 tramos.
- Árbol de expansión mínimo: 23.73. Las rutas cuestan 1.63 veces esa cota, así que no pueden
  estar más lejos del óptimo por ese factor.
- Con un solo bus, la ruta del programa coincide con la de fuerza bruta.

## Algoritmos

| Decisión | Estructura o algoritmo | Complejidad |
|---|---|---|
| Caminos entre paradas | Dijkstra con montón mínimo | O((V + E) log V) por origen |
| Reparto de estudiantes y orden de paradas | Ahorros de Clarke-Wright + 2-opt | O(k² log k) |
| Cota de calidad de la ruta | Kruskal con conjuntos disjuntos (Union-Find) | O(k² log k) |
| Consulta de un estudiante | Tabla hash con encadenamiento | O(1) promedio |
| Armar el recorrido | Pila | O(largo del camino) |
| Simular el bus | Cola | O(n) |

Los conjuntos disjuntos usan **unión por rango y compresión de caminos**, así que `findSet`
y `union` son O(α(n)) amortizado en vez de O(n).

## Contenido del repositorio

```
1_Cuaderno_segunda_entrega/   Cuaderno del Momento 2 (estructuras, algoritmos y pruebas)
2_Cuaderno_entrega_final/     Cuaderno de entrega final (incluye el pitch)
3_Ventana_de_escritorio/      MVP de escritorio en Tkinter
4_Diapositivas/               Pitch en PDF y PPTX
```

## Cómo ejecutar

El MVP de escritorio solo usa la biblioteca estándar de Python (Tkinter incluido).

```bash
cd 3_Ventana_de_escritorio/efiruta_escritorio
python3 app.py
```

> En algunas distribuciones de Linux, Tkinter viene en un paquete aparte
> (`sudo pacman -S tk`, `sudo apt install python3-tk`).

Los cuadernos están pensados para ejecutarse en Google Colab. Solo necesitan `matplotlib`:

```bash
pip install -r requirements.txt
```

## Pruebas

El cuaderno del Momento 2 incluye 19 pruebas que se ejecutan en la celda `10. Plan de
pruebas` y terminan con el mensaje `19 de 19 pruebas pasaron`. Cubren ocupación de los
buses, simetría de las calles, caminos mínimos, árbol de expansión mínimo, consulta por id,
entrada y salida de estudiantes y cierre de calles.

## Cómo se construyó este repositorio

El historial refleja el trabajo real, en orden:

1. Versión original entregada por el equipo.
2. Optimización del motor: conjuntos disjuntos con Union-Find y actualización de los cuadernos.
3. Actualización de roles del equipo, caso de negocio y redacción.
4. Pitch: Diego en la portada y nueva diapositiva del caso.
5. Documentación del repositorio.
