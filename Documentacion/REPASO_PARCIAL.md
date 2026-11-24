# Repaso para el parcial — DDYA

Material de estudio armado sobre **tu propio proyecto**. La idea es que no memorices
teoría suelta sino que reconozcas la misma estructura que ya escribiste: si en el parcial
te piden "implemente una cola de prioridad", tú ya la tienes en `logica.py:94`.

Convenciones:

- `[EN TU CÓDIGO]` = existe en `logica.py` y puedes abrirlo para comparar.
- `[NO ESTÁ]` = no está en tu proyecto, pero sí en el código base de la clase o en el
  programa. Es lo que más riesgo tiene de salir y no haber practicado.
- Los números de línea son de `3_Ventana_de_escritorio/efiruta_escritorio/logica.py`.
- Toda traza de este documento la ejecuté con tu código antes de escribirla. Si un
  resultado no te cuadra, corre el fragmento y compara.

---

## 0. Cómo usar esto según el tiempo que tengas

| Tiempo | Qué leer | Qué escribir a mano |
|---|---|---|
| 3 horas | §1, §2.5, §2.7, §3.3, §3.5, §7 | `build` del heap, Dijkstra en papel |
| 1 día | todo menos §6 | además `findSet`, Kruskal, BFS |
| 2 días | todo | reescribir de memoria Heap, DisjointSets y Dijkstra sin mirar |

Regla de estudio que sirve para este tipo de parcial: **por cada estructura, escribe de
memoria las tres cosas** — el invariante (qué se cumple siempre), las complejidades por
operación, y el error clásico. Si puedes hacer eso sin ayuda, ya la sabes.

Tu proyecto cubre aproximadamente el 70 % del programa: montón, cola de prioridad, tabla
hash, conjuntos disjuntos, grafo, Dijkstra, Kruskal. El 30 % que falta y sí puede salir:
**BFS, DFS, orden topológico, ordenamientos, búsqueda binaria, Prim, Bellman-Ford,
recurrencias**.

---

## 1. Complejidad: lo mínimo que hay que saber hacer rápido

### 1.1 Contar en 30 segundos

| Lo que ves | Costo |
|---|---|
| asignación, comparación, `a[i]`, `len()` | O(1) |
| un `for` sobre `range(n)` | O(n) |
| dos `for` anidados sobre `n` | O(n²) |
| `for` donde la variable se divide (`i //= 2`, `i //= 3`) | O(log n) |
| `x in lista` | O(n) |
| `x in conjunto` / `x in dict` | O(1) promedio, O(n) peor |
| `lista[i:j]`, `lista.pop(0)`, `lista.insert(0, x)` | O(n) |
| `sorted(a)` | O(n log n) |
| `lista.append(x)` | O(1) amortizado |
| recursión | escribe la recurrencia primero |

Tres trampas que valen puntos:

1. **`pop(0)` no es O(1).** En tu propio código, `consultarEstudiante` (`logica.py:753`)
   llena una `cola` y luego hace `cola.pop(0)` dentro de un `while`. Eso es O(p²) para p
   puntos del recorrido. Con `collections.deque` y `popleft()` es O(p). La pregunta de
   parcial es exactamente esa: *"¿cuál es la complejidad de este fragmento y cómo la
   bajas?"*.
2. **`x in lista` dentro de un `for`** convierte tu O(n) en O(n²) sin que se note.
3. **`for i in range(n): for j in range(i)`** es n(n-1)/2 = **O(n²)**, no O(n²/2) —
   la constante se tira.

### 1.2 Tabla que hay que saber de memoria

| Estructura | Operación | Costo |
|---|---|---|
| Pila | push / pop | O(1) |
| Cola | enqueue / dequeue (bien hecha) | O(1) |
| Tabla hash | insert / search / delete | O(1) promedio, O(n) peor |
| Montón | peek | O(1) |
| Montón | insert / extract | O(log n) |
| Montón | build desde arreglo | O(n) |
| Conjuntos disjuntos | findSet / union | O(α(n)) ≈ O(1) |
| Grafo (lista adyacencia) | recorrer vecinos de u | O(grado(u)) |
| Grafo (matriz) | saber si hay arista | O(1), pero O(V²) de memoria |
| BST | search / insert / delete | O(h), peor O(n) |
| BFS / DFS | recorrido completo | O(V + E) |
| Dijkstra (montón) | caminos desde un origen | O(E log V) u O(E log E) |
| Kruskal | árbol de expansión mínimo | O(E log E) |
| Prim (montón) | árbol de expansión mínimo | O(E log V) |
| Merge sort | ordenar | O(n log n), estable |
| Quick sort | ordenar | O(n log n) promedio, O(n²) peor |
| Búsqueda binaria | buscar en arreglo ordenado | O(log n) |

### 1.3 Recurrencias (teorema maestro, versión corta)

Para `T(n) = a·T(n/b) + f(n)`, compara `f(n)` con `n^(log_b a)`:

- si `f(n)` es **menor** → `T(n) = Θ(n^(log_b a))`
- si son **del mismo orden** → `T(n) = Θ(n^(log_b a) · log n)`
- si `f(n)` es **mayor** (y cumple la condición de regularidad) → `T(n) = Θ(f(n))`

Los tres casos que salen siempre:

| Recurrencia | Algoritmo | Resultado |
|---|---|---|
| `T(n) = 2T(n/2) + Θ(n)` | merge sort | Θ(n log n) |
| `T(n) = T(n/2) + Θ(1)` | búsqueda binaria | Θ(log n) |
| `T(n) = 2T(n/2) + Θ(n²)` | ejemplo de clase | Θ(n²) |

---

## 2. Las estructuras, una por una

### 2.1 Pila (LIFO) `[EN TU CÓDIGO]`

`caminoCalles` (`logica.py:435`) la usa así: sube desde el destino siguiendo el arreglo de
padres que dejó Dijkstra, y al sacar de la pila el camino queda en orden origen → destino.

```python
pila = []
actual = destino
while actual is not None:
    pila.append(actual)
    actual = padres[origen][actual]
camino = []
while len(pila) > 0:
    camino.append(pila.pop())
return camino
```

Lo que hay que poder explicar: **por qué la pila y no una cola**. Porque se descubre el
camino al revés (del destino hacia atrás) y la pila invierte. Con una cola saldría al revés.

Complejidad: O(L) con L la longitud del camino. La lista de Python como pila es O(1)
amortizado en `append`/`pop` del final.

### 2.2 Cola (FIFO)

Es la estructura de BFS y de cualquier simulación por turnos. Tu `consultarEstudiante`
modela el avance del bus con una cola de puntos.

**La implementación correcta** es `collections.deque`. Si usas `list`, `append` es O(1) pero
`pop(0)` es O(n), y en un bucle se vuelve O(n²) — que es lo que hace tu código hoy.

```python
from collections import deque
cola = deque([inicio])
while cola:
    u = cola.popleft()      # O(1)
```

### 2.3 Tabla hash `[EN TU CÓDIGO]` — `logica.py:110`

Encadenamiento: un arreglo de listas. `hash(key) % size` elige el cajón; dentro del cajón
se busca lineal.

```python
def hash(self, key):
    return hash(key) % len(self.elements)
```

Lo que hay que saber:

| Concepto | Qué responder |
|---|---|
| Factor de carga | `n / tamaño`. Si crece, las cadenas se alargan y el O(1) se pierde. |
| Colisión | Dos claves en el mismo cajón. Se resuelve por encadenamiento (tu caso) o por direccionamiento abierto. |
| Peor caso | Todas las claves al mismo cajón → O(n) por operación. |
| ¿Por qué O(1) promedio? | Con buen hash y factor de carga acotado, la cadena esperada es constante. |

Tres detalles de tu implementación que son oro para un parcial:

1. **`insert` no verifica duplicados** (`logica.py:117`). Si insertas `('a', 1)` y luego
   `('a', 99)`, el cajón queda con dos pares y `search('a')` devuelve **1**, el primero.
   Verificado. Por eso `construirCaso` consulta antes de insertar.
2. **`update` reemplaza la tupla completa** porque las tuplas son inmutables:
   `self.elements[index][pos] = (key, value2)`.
3. **`delete` borra mientras itera** (`logica.py:136`):

```python
for e in self.elements[index]:
    if e[0] == key:
        self.elements[index].remove(e)   # muta la lista que se está recorriendo
        return
```

Si el cajón tiene dos claves y borras la primera, el iterador se salta la siguiente. Es un
bug real y es el ejemplo perfecto de "no modifiques una colección mientras la recorres".

Dato para el parcial: `hash()` de un `str` en Python **cambia entre ejecuciones** (Python
aleatoriza el hash por proceso). Puedes usarlo en memoria, nunca para guardar en disco ni
para esperar un orden reproducible.

### 2.4 Montón (heap) `[EN TU CÓDIGO]` — `logica.py:11`

Un arreglo que se lee como árbol binario completo. Para el índice `i`:

| Pariente | Índice |
|---|---|
| padre | `(i - 1) // 2` |
| hijo izquierdo | `2i + 1` |
| hijo derecho | `2i + 2` |

En tu código `left = 2*index + 1`, `right = 2*(index+1)` — la segunda forma es equivalente a
`2i + 2`, pero si te la preguntan, la estándar es `2i + 2`.

**Invariante (max-heap):** `data[padre] >= data[hijo]` para todo par. En tu código lo
resume `goesAbove(child, parent)`, que además sirve para el min-heap cuando `config=False`.

**Las tres operaciones y por qué cada una cuesta lo que cuesta:**

- `insert` (línea 37): agrega al final y **sube** mientras supere al padre. Altura del
  árbol = log n → **O(log n)**.
- `extract` (línea 46): guarda la raíz, mueve el último a la raíz y **baja**. → **O(log n)**.
- `build` (línea 57): llama `heapify` desde `len//2` hasta 0. → **O(n)**, no O(n log n).

**Por qué `build` es O(n)** — esta es la pregunta clásica y casi nadie la responde bien.
La mitad de los nodos son hojas y cuestan 0. Un cuarto está a altura 1 y cuesta 1 paso. Un
octavo cuesta 2. La suma es

```
n/4 · 1 + n/8 · 2 + n/16 · 3 + ... ≈ 2n
```

porque la serie `Σ k/2^k` converge a 2. Entonces es lineal. La intuición: **la mayoría de
los nodos están abajo y bajan poquísimo**. Construir insertando uno por uno sí sería
O(n log n), y eso es lo que hacía tu versión original antes de la corrección (por eso la
nota "Corregido" en el comentario).

Detalle: `range(len(self) // 2, -1, -1)` empieza un índice antes de lo necesario (el índice
`len//2` es hoja), pero como `heapify` sobre una hoja no hace nada, no rompe nada.

**Trampa:** `def __init__(self, data=[], config=True)`. El `[]` se evalúa **una sola vez** y
se comparte entre instancias. Es el ejemplo canónico de argumento mutable por defecto y está
en tu propio código. El arreglo es `data=None` y `if data is None: data = []`.

### 2.5 Cola de prioridad `[EN TU CÓDIGO]` — `logica.py:94`

Es un envoltorio: `enqueue` = insertar en el montón, `dequeue` = extraer la raíz. Su gracia
es el **contrato**: "saca siempre el de menor prioridad", sin que el usuario sepa que hay un
montón debajo.

```python
class PriorityQueue:
    def __init__(self, data=[], config=True):
        self.data = Heap(data, config)       # config=False → min-heap
    def enqueue(self, new):
        self.data.insert(new)
    def dequeue(self):
        if len(self) == 0:
            raise Exception("Underflow")
        return self.data.extract()
```

Dos cosas que se califican aquí: la guarda de `Underflow` (extraer de una cola vacía debe
fallar ruidosamente, no devolver `None`), y que el sentido del montón se decide en un solo
lugar (`config`), no repartido por el código.

En Dijkstra y en Kruskal se usa con `config=False` (min-heap): quieres el costo menor
primero. Si te equivocas de sentido, Dijkstra devuelve basura sin lanzar ningún error —
vale la pena probarlo mentalmente.

**Ojo:** en tu `Heap`, `config=True` significa **max-heap** (`goesAbove` compara
`padre < hijo`, así que el mayor sube). Verificado extrayendo: `[10, 8, 5, 4, 3, 1]`.

### 2.6 Conjuntos disjuntos (Union-Find) `[EN TU CÓDIGO]` — `logica.py:145`

Dos arreglos: `padre` (quién es el representante) y `rango` (altura aproximada del árbol).
Dos optimizaciones:

- **unión por rango:** el árbol más bajo cuelga del más alto → evita cadenas.
- **compresión de caminos:** al buscar la raíz, todos los nodos del camino apuntan directo
  a ella → aplana.

Con las dos, el costo amortizado es **O(α(n))**, donde α es la inversa de Ackermann y vale
≤ 4 para cualquier n que quepa en un computador. En la práctica: **O(1)**.

Sin ninguna de las dos, una secuencia de uniones puede crear una lista enlazada y `findSet`
cuesta **O(n)**. Esa es la comparación que suelen pedir.

Tu `findSet` (línea 156) es iterativo y comprime en dos pasadas: sube hasta la raíz y luego
vuelve reasignando. Tu `union` (línea 182) compara rangos.

**Detalle fino que puede valer un punto:** `cuentaConjuntos()` (línea 175) llama
`findSet` sobre todos los elementos, así que **comprime caminos y muta la estructura**.
Una función con nombre de consulta que modifica el estado. Verificado: después de llamarla,
la profundidad de los nodos baja. Si te preguntan "¿`cuentaConjuntos` es una operación de
lectura?", la respuesta es no.

### 2.7 Grafo `[EN TU CÓDIGO]` — `logica.py:200`

Lista de adyacencia + diccionario de pesos. La decisión importante es la representación:

| | Lista de adyacencia | Matriz |
|---|---|---|
| Memoria | O(V + E) | O(V²) |
| ¿Hay arista u-v? | O(grado(u)) | O(1) |
| Recorrer vecinos | O(grado(u)) | O(V) |
| Cuándo | grafo disperso | grafo denso |

Tu caso: 36 vértices y 54 aristas. Una matriz sería 36² = 1296 celdas para guardar 108
aristas (cada tramo en los dos sentidos). **Disperso → lista de adyacencia**. Ese es el
argumento que hay que saber dar.

Tres cosas de tu implementación:

1. **No dirigido se logra duplicando.** `_buildRelation` agrega `(u, v, w)` y `(v, u, w)`.
   Por eso `weights[(u, v)]` funciona en los dos sentidos.
2. **Los pesos van en un dict aparte** del `adjList`. En `adjList` solo están los vecinos.
   Consecuencia: si hubiera dos tramos distintos entre el mismo par de nodos, el dict
   guardaría solo uno y perderías información (grafo simple implícito).
3. **`relations` es un `set`**, así que el orden de `adjList` es arbitrario. No afecta a
   Dijkstra ni a Kruskal (el resultado es único), pero **sí afectaría el orden de salida de
   un BFS**. Si te piden "el orden de visita", tienes que ordenar los vecinos primero.

### 2.8 Árboles binarios y BST `[NO ESTÁ]`

Lo mínimo: un BST cumple `izq < raíz < der`. `search`, `insert` y `delete` cuestan O(h),
donde h es la altura. Si insertas en orden creciente, h = n y todo degenera a O(n). De ahí
salen los árboles balanceados (AVL, rojo-negro) con O(log n) garantizado.

Diferencia que preguntan: **un montón no es un BST**. El montón solo garantiza
`padre ≥ hijos`, no un orden entre hermanos; por eso no sirve para buscar un valor
arbitrario, solo para sacar el máximo.

---

## 3. Los algoritmos

### 3.1 BFS y DFS `[NO ESTÁ en tu proyecto]`

Tu `Graph` ya trae los colores `WHITE`/`GRAY`/`BLACK` y `_buildVProps` (`logica.py:249`)
los inicializa. Eso viene del código base de la clase, que sí implementa BFS y DFS. Es lo
más probable que falte en tu práctica y salga en el parcial.

**BFS** — cola, explora por niveles. En un grafo **sin pesos**, la distancia en número de
aristas es la mínima. En un grafo con pesos **no sirve**: para eso es Dijkstra.

```python
from collections import deque

def bfs(g, s):
    g._buildVProps(s)                      # todos WHITE, s en GRAY
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for v in g.getNeighbors(u):
            if g.v_props[v]['color'] == WHITE:
                g.v_props[v]['color'] = GRAY
                g.v_props[v]['distance'] = g.v_props[u]['distance'] + 1
                g.v_props[v]['parent'] = u
                cola.append(v)
        g.v_props[u]['color'] = BLACK
    return g.v_props
```

**DFS** — pila (o recursión), se hunde por una rama antes de devolverse.

```python
def dfs(g, s):
    g._buildVProps(s)
    pila, orden = [s], []
    while pila:
        u = pila.pop()
        if g.v_props[u]['color'] != WHITE:
            continue
        g.v_props[u]['color'] = BLACK
        orden.append(u)
        for v in g.getNeighbors(u):
            if g.v_props[v]['color'] == WHITE:
                pila.append(v)
    return orden
```

Ambos son **O(V + E)**: cada vértice entra y sale una vez y cada arista se revisa una vez
(dos si el grafo es no dirigido).

Para qué sirve cada uno, en una línea:

| BFS | DFS |
|---|---|
| Camino con menos aristas | Detectar ciclos |
| Componentes conexas | Orden topológico |
| Distancia en saltos | Componentes fuertemente conexas |
| Nivel / capas | Puentes y puntos de articulación |

Para qué usa tu proyecto el equivalente: `validarDatos` (`logica.py:381`) cuenta
**componentes conexas con `DisjointSets`** en vez de con DFS. Es la misma pregunta
("¿está todo conectado?") resuelta con otra estructura. Saber decir "esto también se hace
con un DFS en O(V+E)" demuestra que entiendes, no que memorizaste.

### 3.2 Orden topológico `[NO ESTÁ]`

Solo para **DAG** (dirigido sin ciclos). Dos formas:

- **Kahn (BFS):** repetir "toma un nodo con grado de entrada 0, bórralo y actualiza". Si al
  final no salieron todos, hay ciclo.
- **DFS:** el orden topológico es el orden de finalización **invertido**.

```python
def ordenTopologico(g):
    grado = {v: 0 for v in g.vertexes}
    for u in g.vertexes:
        for v in g.getNeighbors(u):
            grado[v] += 1
    cola = [v for v in g.vertexes if grado[v] == 0]
    orden = []
    while cola:
        u = cola.pop(0)
        orden.append(u)
        for v in g.getNeighbors(u):
            grado[v] -= 1
            if grado[v] == 0:
                cola.append(v)
    return orden if len(orden) == len(g.vertexes) else None
```

Complejidad O(V + E). Si devuelve `None`, había un ciclo.

### 3.3 Dijkstra `[EN TU CÓDIGO]` — `logica.py:256`

**Invariante:** cuando un vértice sale de la cola de prioridad, su distancia ya es la
mínima y no vuelve a cambiar. Por eso se pinta `BLACK` y no se toca más.

```python
pq = PriorityQueue([], False)      # min-heap
pq.enqueue((0, source))
while len(pq) > 0:
    d, u = pq.dequeue()
    if self.v_props[u]['color'] != BLACK:      # lazy deletion
        self.v_props[u]['color'] = BLACK
        self.order.append(u)
        for neighbor in self.getNeighbors(u):
            newDistance = d + self.weights[(u, neighbor)]
            if newDistance < self.v_props[neighbor]['distance']:
                self.v_props[neighbor]['distance'] = newDistance
                self.v_props[neighbor]['parent'] = u
                pq.enqueue((newDistance, neighbor))
```

Cuatro preguntas que caen siempre sobre este bloque:

1. **¿Qué es la "lazy deletion" y por qué no hace falta `decrease-key`?**
   Cuando mejoras la distancia de `v`, en vez de modificar su entrada en el montón
   metes una nueva. El montón queda con entradas viejas, pero **la buena sale primero**
   (tiene menor costo), cierra `v`, y las viejas se descartan con el `if color != BLACK`.
   El costo es más memoria en la cola, no más tiempo.
2. **¿Por qué funciona si hay entradas repetidas?** Porque el montón siempre entrega el
   menor. La entrada con la distancia correcta tiene el costo más bajo, así que sale antes
   que cualquier versión peor del mismo vértice.
3. **¿Por qué no admite pesos negativos?** Porque el invariante asume que al cerrar `u` no
   va a aparecer después un camino más corto pasando por otro nodo todavía abierto. Con
   pesos negativos eso sí puede pasar, y el algoritmo cierra un valor incorrecto **sin
   avisar**. Para eso existe Bellman-Ford.
4. **¿Complejidad?** Cada relajación exitosa mete una entrada: a lo sumo E. Cada
   `enqueue`/`dequeue` es O(log E). Total **O(E log E)**, equivalente a O(E log V). Con
   `decrease-key` sería O(E + V log V).

### 3.4 Bellman-Ford `[NO ESTÁ]` — el que sí admite negativos

Relaja **todas** las aristas V-1 veces. O(V·E). Si al hacer la pasada V-ésima todavía se
mejora algo, hay un ciclo negativo (el problema no tiene solución).

```python
def bellmanFord(vertices, aristas, s):
    d = {v: float('inf') for v in vertices}
    d[s] = 0
    for _ in range(len(vertices) - 1):
        for u, v, w in aristas:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    for u, v, w in aristas:              # detección de ciclo negativo
        if d[u] + w < d[v]:
            return None
    return d
```

La comparación de una línea: **Dijkstra es más rápido pero exige pesos ≥ 0;
Bellman-Ford es más lento y tolera negativos**.

### 3.5 Kruskal `[EN TU CÓDIGO]` — `logica.py:560`

1. Ordena las aristas de menor a mayor (aquí con una `PriorityQueue` en min).
2. Para cada arista, si une **dos conjuntos distintos**, la acepta.
3. Para cuando tiene V-1 aristas.

Es greedy, y funciona por el **corte**: la arista más barata que cruza un corte siempre
pertenece a algún árbol mínimo.

```python
while len(pq) > 0 and len(aristas) < len(puntos) - 1:
    c, a, b = pq.dequeue()
    if dj.findSet(a) != dj.findSet(b):
        dj.union(a, b)
        aristas.append((a, b, c))
        peso = peso + c
```

Complejidad: ordenar E aristas es O(E log E); cada `findSet`/`union` es casi O(1). Total
**O(E log E)**, dominado por el ordenamiento.

En tu proyecto se construye el grafo completo sobre los puntos (colegio + paradas): con
k = 19 puntos son k(k-1)/2 = 171 aristas. Trivial, pero **saber decir por qué** (se quiere
el MST sobre las paradas usando la distancia real por calles entre ellas, no sobre las
esquinas) es lo que diferencia una respuesta buena.

### 3.6 Kruskal vs Prim `[Prim NO ESTÁ]`

| | Kruskal | Prim |
|---|---|---|
| Estrategia | Global: ordena todas las aristas | Local: crece desde un vértice |
| Estructura clave | Conjuntos disjuntos | Cola de prioridad |
| Costo | O(E log E) | O(E log V) |
| Brilla en | Grafo disperso | Grafo denso |
| Con aristas ya ordenadas | Casi lineal | No aplica |

En un grafo disperso (tu caso: 54 aristas para 36 nodos) los dos dan lo mismo; Kruskal suele
ser más simple de escribir. Si el grafo fuera denso (E ≈ V²), ordenar E aristas duele y Prim
con montón gana.

**Dato de tu proyecto que sirve como pregunta de examen:** el MST pesa 23.73 y la ruta de
los buses cuesta 38.68. El MST **sí** es menor, como debe ser (quitando una arista a
cualquier recorrido cerrado queda un árbol de expansión). Pero el MST (23.73) es mayor que
los **22.20 km** del recorrido… porque son **unidades distintas**: 22.20 son km y 23.73 es
costo (la unidad interna que combina km y minutos). Comparar magnitudes en unidades
distintas es el error que más puntos cuesta en estos parciales.

### 3.7 Ordenamientos `[NO ESTÁ]`

| Algoritmo | Mejor | Promedio | Peor | Memoria | Estable |
|---|---|---|---|---|---|
| Burbuja | O(n) | O(n²) | O(n²) | O(1) | sí |
| Inserción | O(n) | O(n²) | O(n²) | O(1) | sí |
| Selección | O(n²) | O(n²) | O(n²) | O(1) | no |
| Merge sort | O(n log n) | O(n log n) | O(n log n) | O(n) | sí |
| Quick sort | O(n log n) | O(n log n) | O(n²) | O(log n) | no |

**Estable** = los elementos iguales conservan su orden relativo. Merge lo es, quick no.

Por qué quick es O(n²) en el peor caso: si el pivote siempre es el menor o el mayor, la
partición deja un lado vacío y la recursión baja de a uno. Pasa con un arreglo ya ordenado
si eliges el primer elemento como pivote.

En Python, `sorted()` y `list.sort()` usan Timsort: O(n log n) garantizado y estable. Puedes
decirlo.

### 3.8 Búsqueda binaria `[NO ESTÁ]`

Requiere arreglo **ordenado**. O(log n).

```python
def busquedaBinaria(a, x):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

Los dos errores clásicos: `while lo < hi` (no revisa el último) y `lo = mid` en vez de
`lo = mid + 1` (ciclo infinito cuando faltan dos elementos). En Python `(lo+hi)//2` no
desborda; en C/Java sí, y ahí se usa `lo + (hi-lo)//2`.

### 3.9 Greedy vs programación dinámica

Cómo reconocerlo en el enunciado:

| Señal | Greedy | DP |
|---|---|---|
| "Toma siempre lo mejor ahora" | sí | no |
| Subproblemas **independientes** | sí | no, se repiten |
| Necesitas el óptimo global garantizado | solo con prueba de intercambio | sí |
| Ejemplos | Kruskal, Prim, Dijkstra, Huffman | mochila 0/1, cambio de monedas, LCS |

**Tu proyecto tiene el ejemplo perfecto de greedy que no es óptimo:** Clarke-Wright decide
fusionar rutas por ahorro, y da 38.68 de costo cuando el óptimo para un bus solo (con 8
estudiantes) es menor. `mejorar2opt` lo acerca, pero no lo garantiza. Saber decir "es
greedy, es rápido, aproxima, y la brecha se mide contra una cota inferior que es el MST"
es exactamente el tipo de respuesta que sube nota.

---

## 4. Trazas resueltas (para hacer con lápiz, no solo leer)

### 4.1 Build de un max-heap

Arreglo inicial: `[4, 10, 3, 5, 1, 8]`, n = 6. Se recorre desde `i = 3` hasta `0`.

| i | Hijos de i | Antes | Qué pasa | Después |
|---|---|---|---|---|
| 3 | 7, 8 (no existen) | `[4,10,3,5,1,8]` | hoja, nada | `[4,10,3,5,1,8]` |
| 2 | 5, 6 → `8` | `[4,10,3,5,1,8]` | `8 > 3`, baja el 3 | `[4,10,8,5,1,3]` |
| 1 | 3, 4 → `5, 1` | `[4,10,8,5,1,3]` | `10` ya es mayor | `[4,10,8,5,1,3]` |
| 0 | 1, 2 → `10, 8` | `[4,10,8,5,1,3]` | sube el `10`, y el `4` sigue bajando | `[10,5,8,4,1,3]` |

Resultado: `[10, 5, 8, 4, 1, 3]`. Verificado con tu `Heap`.

Al extraer todo sale `[10, 8, 5, 4, 3, 1]`, descendente. Si sale ascendente, tu montón es
min-heap.

### 4.2 Dijkstra con tabla

Grafo no dirigido de 6 nodos:

```
A-B 4   A-C 2   B-C 1   B-D 5   C-D 8   C-E 10   D-E 2   D-F 6   E-F 3
```

Desde `A`. En cada fila se cierra el nodo con menor distancia pendiente.

| Paso | Cerrado | d(A) | d(B) | d(C) | d(D) | d(E) | d(F) |
|---|---|---|---|---|---|---|---|
| 0 | — | **0** | ∞ | ∞ | ∞ | ∞ | ∞ |
| 1 | A | 0 | 4 | **2** | ∞ | ∞ | ∞ |
| 2 | C | 0 | **3** | 2 | 10 | 12 | ∞ |
| 3 | B | 0 | 3 | 2 | **8** | 12 | ∞ |
| 4 | D | 0 | 3 | 2 | 8 | **10** | 14 |
| 5 | E | 0 | 3 | 2 | 8 | 10 | **13** |
| 6 | F | 0 | 3 | 2 | 8 | 10 | 13 |

Padres: `B←C`, `C←A`, `D←B`, `E←D`, `F←E`. Orden de cierre: `A, C, B, D, E, F`.
Verificado: `distancias {A:0, B:3, C:2, D:8, E:10, F:13}`.

Fíjate en el paso 2: **B se mejora antes de cerrarse** (de 4 a 3, pasando por C) y eso es
lo que el algoritmo aprovecha. Si hubieras cerrado B al verlo desde A, el resultado sería 4
y estarías mal. Esa es la trampa concreta de Dijkstra.

### 4.3 Kruskal con el estado de los conjuntos

Mismas aristas, ordenadas: `BC 1, AC 2, DE 2, AB 3, EF 3, BD 5, CD 6, DF 6, AE 10, CE 10, AF 13`
(el orden exacto entre pesos iguales no importa).

| Arista | Peso | ¿Conjuntos distintos? | Acción | Conjuntos |
|---|---|---|---|---|
| B-C | 1 | sí | acepta | {B,C} {A} {D} {E} {F} |
| A-C | 2 | sí | acepta | {A,B,C} {D} {E} {F} |
| D-E | 2 | sí | acepta | {A,B,C} {D,E} {F} |
| A-B | 3 | **no** (mismo conjunto) | rechaza, hay ciclo | igual |
| E-F | 3 | sí | acepta | {A,B,C} {D,E,F} |
| B-D | 5 | sí | acepta | todos juntos → 5 aristas, fin |

Peso total: `1 + 2 + 2 + 3 + 5 = 13`. Verificado con tu `kruskal`.

Lo que hay que mostrar en el parcial: **el rechazo de A-B por ciclo** (y decir "mismo
`findSet`"), y **el criterio de parada** (V-1 aristas).

### 4.4 BFS sobre el mismo grafo

Desde `A`, suponiendo que los vecinos se visitan en orden alfabético:

| Paso | Cola | Se saca | Se descubre | Distancia (aristas) |
|---|---|---|---|---|
| 1 | A | A | B, C | A=0 |
| 2 | B, C | B | D | B=1 |
| 3 | C, D | C | E | C=1 |
| 4 | D, E | D | F | D=2 |
| 5 | E, F | E | — | E=2 |
| 6 | F | F | — | F=3 |

Orden: `A, B, C, D, E, F`. Distancias en **aristas**: D y E a 2 saltos, F a 3.

Compara con Dijkstra: BFS dice `D = 2 saltos`, Dijkstra dice `D = 8 km`. **Ambos son
correctos** porque miden cosas distintas. Si el parcial pregunta "¿cuál es el camino más
corto de A a D?", la primera respuesta debe ser **"¿corto en qué?"**.

Recuerda la advertencia de §2.7: con tu `Graph`, el orden real depende del `set`, así que el
orden de visita puede cambiar entre ejecuciones. La tabla anterior asume vecinos ordenados.

### 4.5 Union-Find: con y sin optimizaciones

Seis elementos `a..f`, uniones `(a,b) (c,d) (a,c) (e,f) (d,e)`.

| Unión | padre | rango | Conjuntos |
|---|---|---|---|
| inicial | todos apuntan a sí mismos | todos 0 | 6 |
| (a,b) | `b→a` | `a=1` | 5 |
| (c,d) | `d→c` | `c=1` | 4 |
| (a,c) | `c→a` | `a=2` | 3 |
| (e,f) | `f→e` | `e=1` | 2 |
| (d,e) | `e→a` (rango 1 < 2) | `a=2` | 1 |

Estado final de los padres: `a→a, b→a, c→a, d→a, e→a, f→e`.

`f` quedó a profundidad 2 (`f → e → a`). Sin unión por rango, si las uniones hubieran ido
`(a,b) (b,c) (c,d) (d,e) (e,f)` cadenas así, `findSet(f)` tendría que subir 5 veces: es la
diferencia entre O(α) y O(n).

Después de un `findSet(f)`, la compresión deja `f→a` directo y la profundidad vuelve a 1.
Verificado con tu `DisjointSets`.

**Detalle del ejercicio:** la profundidad de `f` bajó a 1 *antes* de llamar explícitamente
`findSet(f)`, porque `cuentaConjuntos()` ya había comprimido todas las rutas. Es el efecto
secundario de §2.6.

---

## 5. Preguntas tipo parcial (con respuesta)

Tapa la respuesta con la mano y contesta en voz alta. Si no la dices en 15 segundos, no la
sabes.

### Complejidad

**1. ¿Cuál es la complejidad de construir un montón insertando n elementos uno por uno, y por qué `build` es mejor?**
O(n log n) vs O(n). `build` aprovecha que la mayoría de los nodos son hojas y baja poco: la suma de alturas es 2n.

**2. ¿Por qué `x in lista` dentro de un bucle lo vuelve O(n²)?**
Cada `in` recorre hasta n elementos y se hace n veces.

**3. `T(n) = 2T(n/2) + n`. ¿Cuánto vale?**
Θ(n log n), caso 2 del teorema maestro.

**4. ¿Por qué la tabla hash es O(1) promedio y O(n) peor?**
Promedio: cadenas de largo constante con buen hash y factor de carga acotado. Peor: todas las claves al mismo cajón.

**5. ¿Un `for` que anida otro y el interno va de 0 a i, cuántas iteraciones hace?**
n(n-1)/2, que es O(n²).

**6. Ordena de menor a mayor: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ), O(n!).**
Ese mismo orden. (`2ⁿ` es peor que `n²` y mejor que `n!`.)

### Estructuras

**7. ¿Cuál es la diferencia entre un montón y un BST?**
El montón solo garantiza la relación padre-hijo (no hay orden entre hermanos), sirve para extraer el extremo. El BST garantiza orden total en el recorrido inorden, sirve para buscar cualquier valor.

**8. ¿Por qué el montón se guarda en un arreglo y no con punteros?**
Es un árbol binario completo: los índices dan los parientes sin punteros. Menos memoria y mejor localidad de caché.

**9. Un grafo tiene 1000 vértices y 2000 aristas. ¿Matriz o lista de adyacencia?**
Lista: la matriz usaría 10⁶ celdas para 2000 aristas. Es disperso.

**10. ¿Para qué sirve el color GRAY en BFS/DFS?**
Marca "descubierto pero no terminado": detecta aristas de retroceso (ciclos) y evita procesar dos veces. En blanco = no visitado, negro = terminado.

**11. En tu `dijkstra`, ¿qué rol cumple `GRAY`?**
Ninguno. `_buildVProps` deja el origen en GRAY pero el algoritmo nunca lo consulta; solo usa BLACK. Es residuo de BFS/DFS.

**12. ¿Qué pasa si dos claves caen en el mismo cajón de la tabla hash?**
Se guardan en la misma lista y la búsqueda recorre la cadena comparando claves. O(largo de la cadena).

**13. ¿Por qué `insert` en tu tabla no revisa duplicados? ¿Qué consecuencia tiene?**
Porque asume que el llamador controla. Consecuencia: dos pares con la misma clave, y `search` devuelve el primero insertado.

**14. ¿Qué estructura usarías para "el pedido más urgente" y por qué no una lista ordenada?**
Cola de prioridad (montón): insertar es O(log n) y sacar el mínimo O(log n). En una lista ordenada, insertar en el medio es O(n).

### Grafos

**15. ¿Cuándo BFS da el camino más corto y cuándo no?**
Da el mínimo en número de aristas en un grafo sin pesos. Con pesos, no: necesita Dijkstra.

**16. ¿Por qué Dijkstra falla con pesos negativos?**
Al cerrar un nodo asume que no aparecerá un camino menor después. Con negativos sí puede aparecer, y cierra un valor incorrecto sin avisar.

**17. ¿Qué es la relajación?**
`if d[u] + w < d[v]: d[v] = d[u] + w`. Intentar mejorar la distancia conocida usando una arista.

**18. ¿Por qué el MST de tu proyecto (23.73) es menor que el costo de las rutas (38.68)?**
Porque quitar una arista a un recorrido cerrado deja un árbol de expansión: todo MST es cota inferior del recorrido. El árbol conecta sin repetir; las rutas tienen que volver al colegio.

**19. ¿Por qué el MST (23.73) es mayor que los 22.20 km del recorrido?**
Unidades distintas: 22.20 son km, 23.73 es costo (km y minutos combinados). No se comparan.

**20. ¿Kruskal o Prim para un grafo denso?**
Prim: O(E log V) con montón. Kruskal ordena E aristas y en un grafo denso E ≈ V², así que el ordenamiento domina.

**21. ¿Cómo detectas un ciclo en un grafo no dirigido?**
Con conjuntos disjuntos: si al procesar la arista u-v ya están en el mismo conjunto, hay ciclo. (O con DFS y colores.)

**22. ¿Qué devuelve un orden topológico si el grafo tiene ciclo?**
Nada: no existe. En Kahn sobran nodos al final; con DFS aparece una arista de retroceso.

**23. ¿Complejidad de DFS en un grafo con lista de adyacencia?**
O(V + E). Con matriz sería O(V²).

### Código y trampas

**24. ¿Por qué `def f(data=[])` es peligroso?**
El `[]` se crea una vez al definir la función y se reutiliza en todas las llamadas: lo que agregues persiste entre llamadas.

**25. ¿Qué pasa si borras un elemento de una lista mientras la recorres con `for`?**
El iterador avanza de índice y se salta el siguiente elemento. Se copia la lista o se recorre al revés.

**26. ¿Por qué `pop(0)` en un bucle es O(n²)?**
Cada `pop(0)` desplaza todos los elementos una posición: O(n) por llamada.

**27. ¿Es estable `sorted()` en Python? ¿Y qué significa?**
Sí, Timsort es estable: los elementos iguales conservan su orden relativo original.

**28. ¿Qué diferencia hay entre `list.sort()` y `sorted(lista)`?**
`sorted` devuelve una lista nueva; `list.sort()` ordena en el sitio y devuelve `None`.

**29. ¿Por qué `hash('abc')` puede dar un valor distinto mañana?**
Python aleatoriza el hash de las cadenas por proceso (PYTHONHASHSEED). Sirve en memoria, no para persistir ni para esperar orden reproducible.

**30. `if u < v` para guardar una arista no dirigida. ¿Qué problema tiene?**
Solo funciona si los vértices son comparables y si normalizas siempre el par. Con strings se compara lexicográficamente y está bien, pero con objetos arbitrarios falla; lo robusto es `frozenset((u,v))` o guardar las dos direcciones, como hace `_buildRelation`.

---

## 6. Ejercicios de código

### 6.1 Implementar `esConexo` con conjuntos disjuntos

```python
def esConexo(g):
    dj = DisjointSets(g.vertexes)
    for u in g.vertexes:
        for v in g.getNeighbors(u):
            dj.union(u, v)
    return dj.cuentaConjuntos() == 1
```

Es exactamente lo que hace tu `validarDatos` con las esquinas. Complejidad: O(V + E·α).

### 6.2 Completar un `min_heapify` correcto

```python
def min_heapify(self, index):
    smallest = index
    l, r = self.left(index), self.right(index)
    if l < len(self.data) and self.data[l] < self.data[smallest]:
        smallest = l
    if r < len(self.data) and self.data[r] < self.data[smallest]:
        smallest = r
    if smallest != index:
        self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
        self.min_heapify(smallest)      # <- la línea que todos olvidan
```

Sin la llamada recursiva solo bajas un nivel y el arreglo deja de ser montón.

### 6.3 Encuentra el bug

**(a)**
```python
def borrarPares(lista, x):
    for e in lista:
        if e == x:
            lista.remove(e)
```
No borra duplicados consecutivos: al remover, el iterador salta el siguiente. Solución: `lista[:] = [e for e in lista if e != x]`.

**(b)**
```python
def buscar(a, x):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[mid] < x:
            lo = mid          # <- bug
        else:
            hi = mid
    return -1
```
`lo = mid` no avanza cuando `hi == lo + 1`: ciclo infinito. Debe ser `lo = mid + 1` y `hi = mid - 1`, con `while lo <= hi`.

**(c)**
```python
def delete(self, key):
    index = self.hash(key)
    for e in self.elements[index]:
        if e[0] == key:
            self.elements[index].remove(e)
            return
```
Borra mientras itera (tu `logica.py:136`). Si hay dos claves en el cajón, la segunda se salta.

### 6.4 ¿Qué imprime?

**(1)**
```python
h = Heap([3, 1, 4, 1, 5, 9, 2, 6], True)
salida = []
while len(h) > 0:
    salida.append(h.extract())
print(salida)
```
`[9, 6, 5, 4, 3, 2, 1, 1]` — max-heap, descendente. Verificado.

**(2)**
```python
t = HashTable(7)
t.insert('a', 1); t.insert('b', 2); t.insert('c', 3)
print(t.search('c'), t.search('z'))
t.insert('a', 99)
print(t.search('a'))
```
`3 None` y luego `1`. El `99` es invisible porque `search` devuelve el primer par de la cadena. Verificado.

**(3)**
```python
def f(x=[]):
    x.append(1)
    return x
a = f(); b = f()
print(a, b)
```
`[1] [1, 1]`. Si lo escribes todo en un solo `print(f(), f())` sale `[1, 1] [1, 1]`: Python evalúa los dos argumentos antes de imprimir, así que ambos apuntan a la misma lista ya mutada. Verificado.

**(4)**
```python
g = DisjointSets(['p', 'q', 'r'])
g.union('p', 'q')
print(g.cuentaConjuntos(), g.findSet('r'))
```
`2 r`. `r` está solo, su representante es él mismo. Verificado.

**(5)**
```python
kp = PriorityQueue([], False)
kp.enqueue(3); kp.enqueue(1); kp.enqueue(2)
print(kp.dequeue())
```
`1`. `config=False` es min-heap. Si hubieras puesto `True`, saldría `3`.

**(6)**
```python
w = {}
w[('a', 'b')] = 5
g = Graph(['a', 'b'], [('a', 'b', 5)], directed=False)
print(w[('b', 'a')])
```
`KeyError`. Tu `Graph` evita esto porque `_buildRelation` guarda las dos direcciones. Si escribes un grafo no dirigido a mano con un solo sentido, la primera relajación explota.

### 6.5 Escríbelo de memoria

1. `Heap.build` + `max_heapify` (8 líneas).
2. `DisjointSets.findSet` con compresión (6 líneas).
3. `dijkstra` completo (15 líneas).
4. `kruskal` completo (10 líneas).
5. BFS (12 líneas).

Si los cinco salen sin mirar, el parcial de estructuras está cubierto.

---

## 7. Los diez errores que cuestan puntos

1. **Confundir "más corto" con "menos km".** Pregunta primero en qué unidad.
2. **Comparar magnitudes en unidades distintas** (km contra costo).
3. **Dar la complejidad sin justificar.** "O(n log n) porque el bucle divide" vale más que el símbolo solo.
4. **Decir que `build` es O(n log n).** Es O(n) y hay que saber la suma de alturas.
5. **Cerrar un nodo en Dijkstra antes de tiempo.** Solo se cierra al salir de la cola.
6. **Usar BFS para caminos con peso.**
7. **Olvidar la recursión en `heapify`.**
8. **`pop(0)` en un bucle.**
9. **Argumento mutable por defecto.**
10. **Afirmar que un greedy es óptimo sin prueba.** Clarke-Wright no lo es, y decirlo sube nota.

---

## 8. Hoja de una página (imprimir y llevar)

```
ÍNDICES DEL MONTÓN      padre (i-1)//2   izq 2i+1   der 2i+2
COMPLEJIDADES           peek O(1) · insert/extract O(log n) · build O(n)
                        hash O(1) prom / O(n) peor · findSet O(α)≈O(1)
                        BFS/DFS O(V+E) · Dijkstra O(E log V)
                        Kruskal O(E log E) · Prim O(E log V)
                        merge O(n log n) estable · quick O(n log n)/O(n²) inestable
RECURRENCIA             T(n)=aT(n/b)+f(n) → compara f(n) con n^(log_b a)
DIJKSTRA                invariante: al salir de la cola, la distancia es final
                        no cerrar antes · no pesos negativos → Bellman-Ford O(VE)
KRUSKAL                 ordena aristas · acepta si findSet(u)!=findSet(v) · para en V-1
BFS vs DFS              BFS: cola, menos aristas, sin pesos
                        DFS: pila, ciclos, topológico (finalización invertida)
GRAFO DISPERSO          lista de adyacencia O(V+E) · denso: matriz O(V²)
NO DIRIGIDO             guardar las dos direcciones o frozenset
TRAMPAS                 pop(0) O(n) · def f(x=[]) · borrar iterando · hash() no persiste
```

---

### Después del parcial

Si algo de esto no coincide con lo que dictó el profesor, gana el profesor: hay cursos que
definen el montón con el índice 1 (`2i`, `2i+1`) o que exigen `decrease-key` en Dijkstra.
Ajusta las fórmulas a su convención antes de memorizarlas.
