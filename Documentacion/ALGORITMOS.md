# Los algoritmos de EfiRuta

Guion de exposición. Para cada algoritmo: qué problema resuelve, cómo está escrito,
dónde vive en el código y qué se puede mostrar en vivo. Al final, el que no está en
el programa del curso y por qué se metió.

Todo lo que sigue se puede comprobar con el archivo abierto: las líneas citadas son
de `3_Ventana_de_escritorio/efiruta_escritorio/logica.py`, que es el mismo código de
la celda 21 del cuaderno final (63 de 63 funciones y clases idénticas).

---

## 1. El problema, en términos de algoritmos

Veinte estudiantes, dieciocho paradas (dos pares son hermanos y comparten esquina),
tres buses de 8, 7 y 7 puestos, un colegio en la Calle 116 con Carrera 11.

Lo que hay que decidir es a qué bus va cada parada y en qué orden las visita. Eso es
el **problema de ruteo de vehículos con capacidad** (CVRP, por *Capacitated Vehicle
Routing Problem*), que es NP-difícil: con 18 paradas, probar todos los repartos y
todos los órdenes pasa de los billones de casos. No se resuelve por fuerza bruta; se
resuelve con una heurística buena y con una cota que diga qué tan lejos está del óptimo.

El costo de cada calle no es solo distancia. Se pondera:

```
costo = 0.8 * (km / km promedio) + 0.2 * (minutos / minutos promedio)
```

Es la línea 368. Así el algoritmo prefiere calles cortas sin castigar demasiado las
lentas, y las dos unidades quedan en la misma escala (sin ponderar, comparar 2 km con
1 minuto no significa nada).

---

## 2. Las piezas que se escribieron a mano

El proyecto no usa `networkx`, `scipy` ni `heapq`. Las estructuras son propias, porque
el curso las pide y porque así el comportamiento es auditable:

| Estructura | Dónde | Para qué se usa aquí |
|---|---|---|
| `Heap` (máximo y mínimo, según un flag) | `logica.py:11-91` | Es la base de la cola de prioridad |
| `PriorityQueue` | `logica.py:94-107` | Dijkstra, Clarke-Wright, Kruskal y la asignación de buses |
| `HashTable` (101 cubetas, encadenamiento) | `logica.py:110-142` | Buscar un estudiante por cédula en O(1); guarda su bus y su parada |
| `DisjointSets` (unión por rango + compresión de caminos) | `logica.py:145-197` | Clarke-Wright (no unir rutas ya unidas) y Kruskal (no formar ciclos) |
| `Graph` (lista de adyacencia, dirigido o no) | `logica.py:200-275` | El mapa de calles y el Dijkstra |

---

## 3. Los seis algoritmos, uno por uno

### 3.1 Dijkstra con montón mínimo — por dónde va el bus

**Qué resuelve.** El camino de menor costo entre dos esquinas, sobre el grafo de
calles ponderado.

**Cómo está escrito** (`logica.py:256-275`). Cola de prioridad de mínimos con pares
`(costo, vértice)`. Un vértice se cierra la primera vez que sale de la cola, y en ese
momento su costo ya es el mínimo. Se relaja cada vecino y se vuelve a encolar.
`self.order` guarda el orden de cierre, que es la evidencia de que el algoritmo avanzó
en orden de costo creciente (lo verifica la prueba P3).

**Cómo se usa.** `calcularCostos` (`logica.py:422`) corre un Dijkstra desde el colegio
y desde cada una de las 18 paradas: **19 ejecuciones**. Con los árboles de padres se
arman las 361 distancias entre esos 19 puntos y se reconstruye cualquier camino con
una **pila** (`caminoCalles`, `logica.py:435`): se sube del destino al origen por los
padres y, al sacar, queda en el orden correcto.

**Costo.** O(E log V) por origen; con 54 tramos y 36 esquinas, milisegundos.

**Lo que se muestra.** Subir de la Calle 116 a la 122 son 0.5 km por la Autopista y
0.5 km por la Carrera 11. La Autopista cuesta 0.825 y la Carrera 11 cuesta 0.946: el
bus prefiere la primera porque va a 40 km/h y la segunda a 20, no porque sea más corta.
Y si se cierra una calle, `cerrarCalle` quita la arista y el siguiente Dijkstra ya trae
otro camino, sin tocar el resto del código.

### 3.2 Clarke-Wright (ahorros) — el reparto entre buses

**Qué resuelve.** Agrupar las paradas en rutas por bus y ordenarlas dentro de cada ruta.

**La idea.** Al principio cada parada es su propia ruta: colegio → parada → colegio.
Unir dos rutas por sus extremos ahorra

```
ahorro(i, j) = c(colegio, i) + c(colegio, j) - peso * c(i, j)
```

Si el ahorro es grande, esas dos paradas están cerca entre sí y lejos del colegio:
conviene que el mismo bus las recoja. Se procesan los ahorros de mayor a menor y se
unen mientras quepan.

**Cómo está escrito** (`logica.py:474-517`). Los pares se meten en un **montón máximo**
y salen en orden de ahorro. Los **conjuntos disjuntos** dicen en O(α(n)) si dos paradas
ya están en la misma ruta, y la unión solo se acepta si las dos están en un extremo
(no se puede pegar una parada del medio) y si la carga sumada no pasa el cupo del bus
más grande. En el caso del proyecto se descartan **13 uniones** por capacidad, y el
programa lo reporta.

**El detalle que no es obvio: se prueban ocho pesos.** El factor `peso` decide cuánto
pesa la cercanía entre paradas frente a la cercanía al colegio. Con un solo valor se
está apostando; con `PESOS_AHORRO = [1.0, 0.6, 0.8, 1.2, 1.4, 1.6, 1.8, 2.0]`
(`logica.py:314`) se corren ocho repartos completos y se queda el de menor costo total.
En el caso del proyecto gana **1.8**, con costo 38.68. Son ocho pasadas de milisegundos:
más barato que equivocarse.

**Costo.** O(n² log n) para armar la cola de ahorros, con n = 18 paradas.

### 3.3 2-opt — el que se agregó por fuera (sección 4)

### 3.4 Kruskal con conjuntos disjuntos — la cota de calidad

**Qué resuelve.** Dar un número que responda: "¿qué tan buena es esta ruta?". Sin el
óptimo no se puede comparar contra el óptimo. Pero sí se puede calcular el **árbol de
expansión mínimo**: la forma más barata de conectar el colegio con todas las paradas.

**Cómo está escrito** (`logica.py:560-580`). Todas las aristas entre los 19 puntos van
a un **montón mínimo** y salen de menor a mayor. Se acepta la arista solo si une dos
conjuntos distintos, y eso lo dice `findSet` de los conjuntos disjuntos. Se detiene con
18 aristas (19 puntos menos uno).

**Cómo se usa.** Es una cota inferior: **ninguna ruta puede costar menos que el árbol**,
porque cualquier recorrido que visite todas las paradas contiene, como subconjunto, un
árbol que las conecta. Aquí el árbol pesa **23.73** y las rutas cuestan **38.68**: el
colegio sabe que está a **1.63 veces o menos** de la mejor ruta posible. Es una frase
defendible frente a un rector, y es un número, no una promesa.

### 3.5 Asignación de buses con dos montones máximos — quién va en qué bus

**Qué resuelve.** Repartir las rutas ya armadas entre buses de distinta capacidad.

**Cómo está escrito** (`logica.py:540-557`). Dos montones máximos: uno con las rutas
ordenadas por número de estudiantes, otro con los buses ordenados por puestos. Se saca
la ruta más llena y el bus más grande. Si en algún momento la ruta no cabe, no hay
reparto posible y se devuelve `None` para que el programa explique el problema.

Este emparejamiento por orden es **exacto**, no aproximado: si existe un reparto
válido, el voraz lo encuentra (es el mismo argumento del problema de las tareas con
plazo). Y de paso resuelve el orden de los buses: el más grande se lleva la ruta más
pesada.

### 3.6 Pila y cola — reconstruir el camino y simular el bus

Dos usos chicos pero visibles:

- **Pila** (`caminoCalles`, `logica.py:435`): reconstruye el camino de Dijkstra de
  atrás hacia adelante. Se apila desde el destino y al desapilar sale ordenado.
- **Cola** (`consultarEstudiante`, `logica.py:753-809`): la vista de los padres. Los
  puntos del recorrido se atienden en orden de llegada, como una cola, y según la hora
  se responde "Sofía va en el bus 2, a 2.5 km, llega en 9 minutos" (a las 6:08) o "ya
  está en el colegio" (desde las 6:20). Además se elige el **sentido** de la ruta
  comparando los minutos a bordo (sección 5, paso 5), para que los niños del final del
  recorrido no sean los que más tiempo pasan sentados.

### 3.7 Fuerza bruta — solo para verificar, no para producir

En la prueba P9 (celda 26 del cuaderno) se generan las **5040 permutaciones** de las
7 paradas de un solo bus (`7! = 5040`) y se calcula el costo de cada una. El programa
tiene que dar exactamente el mismo costo que la mejor. Es la única prueba donde se
conoce el óptimo, y sirve para responder la pregunta obvia: "¿y cómo saben que su
heurística funciona si no conocen la respuesta?". En un bus, la conocen.

---

## 4. El algoritmo especial: 2-opt

### Qué es

Es una **mejora local** tomada del problema del viajante (Croes, 1958), no del temario
de la materia. Toma una ruta y prueba invertir un tramo: si el tramo `... a → b ...`
se reemplaza por `... a → c ... b → d ...` y cuesta menos, se invierte y se vuelve a
intentar. Termina cuando ninguna inversión mejora.

### Por qué hizo falta

Clarke-Wright une paradas por **ahorro**, no por geografía. El resultado es una ruta
que pasa cerca de cada parada pero con frecuencia **cruza sobre sí misma**: va al norte,
vuelve al sur y sube otra vez. El ahorro mide cuánto se economiza al unir dos tramos,
no si el recorrido queda ordenado en el mapa. Sobre el papel la distancia es buena; en
la calle el bus da vueltas.

2-opt quita exactamente eso: los cruces. No cambia el reparto entre buses (eso ya lo
decidió Clarke-Wright), solo el orden dentro de cada ruta.

### Qué aporta, medido

Se puede correr el mismo caso con y sin la mejora (comando abajo). En el caso del
proyecto, con el peso ganador:

| | Sin 2-opt | Con 2-opt | Diferencia |
|---|---|---|---|
| Costo total | 40.09 | **38.68** | −1.41 |
| Kilómetros | 23.10 km | **22.20 km** | −0.90 km |
| Minutos | 64.8 min | **63.9 min** | −0.85 min |
| Inversiones aplicadas | — | 2 | — |
| Tiempo de cálculo | 15.1 ms | 15.5 ms | +0.4 ms |

Medio kilómetro no suena a mucho hasta que se multiplica por 200 días de clase y tres
buses. Y el costo de tenerlo es un cuarto de milisegundo.

### Por qué se defiende como "el especial"

1. **No viene en el temario.** El curso cubre grafos, montones, tablas hash y conjuntos
   disjuntos. 2-opt es de investigación de operaciones y hay que justificarlo con
   literatura, no con la guía de clase.
2. **Tiene un problema concreto que resuelve.** No se agregó "porque sí": sin él,
   Clarke-Wright produce rutas que se cruzan, y el registro del programa lo muestra
   línea por línea ("2-opt: se invierte el tramo ... ahorra X").
3. **Es barato y acotado.** Trabaja sobre una ruta de 7 paradas, con dos ciclos
   anidados; no toca la complejidad del sistema.
4. **Se puede auditar.** El registro de decisiones explica cada inversión con su ahorro,
   así que no hay que creerle al resultado: se lee el porqué.

### Su límite, dicho sin adornos

2-opt llega a un **óptimo local**: ninguna inversión simple mejora, pero puede existir
un orden mejor que requiera dos cambios a la vez (3-opt lo encontraría). Por eso la
prueba P9 importa: en el caso de un solo bus, donde sí se conoce el óptimo por fuerza
bruta, el resultado coincide. No se afirma que las rutas de tres buses sean óptimas; se
afirma que están a 1.63 del árbol mínimo y que la heurística es la misma que en el caso
verificado.

---

## 5. Cómo encajan: el flujo de una corrida

`calcularRutas` (`logica.py:619-725`) es el director de orquesta. Ocho pasos:

1. **Validar** (`validarDatos`, 381). Los conjuntos disjuntos unen cada calle y cuentan
   zonas; si la esquina de un estudiante no está en la zona del colegio, se reporta
   antes de calcular nada.
2. **Agrupar paradas** (409). Hermanos en la misma esquina comparten parada: 20
   estudiantes quedan en 18 paradas.
3. **Dijkstra** (422). 19 orígenes, 361 pares, caminos reconstruidos con pila.
4. **Clarke-Wright** con los 8 pesos (474) → **2-opt** en cada ruta (520) → **asignación
   voraz** (540). Se queda el reparto válido más barato.
5. **Sentido del recorrido** (`minutosABordo`, 583). Se prueba la ruta y su inversa y
   se elige la que deja menos tiempo total a bordo.
6. **Horarios** (`construirHorario`, 596). Mañana y tarde, con km y minutos acumulados
   desde la salida y quién sube o baja en cada parada.
7. **Kruskal** (560). La cota de calidad.
8. **Tabla hash** (110). Se escribe en cada estudiante su bus y su posición, para que
   la vista de los padres responda en O(1).

Todo el cálculo tarda **entre 16 y 28 ms** (mediana 19.6 sobre 20 corridas). Es lo que
permite que, al cerrar una calle, la ruta nueva aparezca sin espera visible.

---

## 6. Qué se puede mostrar en vivo

**El caso completo.** Los números que hay que decir de memoria:

```
22.2 km | 38.68 de costo | 63.9 min | árbol 23.73 | 1.63 veces
contra el orden de inscripción: 70.3 km y 155 min → 68 % menos distancia, 59 % menos tiempo
```

**El efecto de 2-opt**, sin tocar ningún archivo (se apaga la función en memoria):

```bash
cd 3_Ventana_de_escritorio/efiruta_escritorio
python3 - <<'PY'
import logica as L
n, c, t = L.construirMapa()
def caso(): return L.construirCaso(n, c, t, L.COLEGIO, L.ESTUDIANTES, L.BUSES)
print('con 2-opt: %.2f km' % L.calcularRutas(caso())['totalKm'])
L.mejorar2opt = lambda orden, *a: list(orden)
print('sin 2-opt: %.2f km' % L.calcularRutas(caso())['totalKm'])
PY
```

Sale `22.20` y luego `23.10`. La diferencia es la mejora, y se ve en la misma sesión.

**La traza de decisiones.** En la ventana, el panel de decisiones muestra, línea por
línea, cada unión de Clarke-Wright con su ahorro, las 13 descartadas por cupo, cada
inversión de 2-opt y el peso ganador. En el cuaderno, la parte 4 de `ejecutar_demo()`
imprime lo mismo. Es la mejor respuesta a "¿y cómo sé que hizo lo que dice?".

**El cierre de calle.** Cerrar Calle 116 y recalcular: la ruta cambia, los km suben un
poco, y todo el razonamiento se repite en el mismo panel.

---

## 7. Preguntas probables

**¿Por qué no usaron una librería?** Porque el curso pide implementar las estructuras, y
porque con 36 esquinas y 54 tramos una dependencia externa no compra nada: el cálculo
completo son 20 ms. Una librería habría escondido justo lo que hay que explicar.

**¿La ruta es óptima?** No se sabe, y no se dice. Se sabe que está a 1.63 veces del
árbol mínimo o menos, y que en el caso de un solo bus coincide con la fuerza bruta
(5040 permutaciones). CVRP es NP-difícil: afirmar el óptimo en 18 paradas sería
mentira o fuerza bruta inviable.

**¿Por qué 0.8 y 0.2?** Porque el colegio paga kilómetros y los padres sufren minutos.
Los pesos están en dos constantes al inicio del archivo; cambiarlos cambia las rutas, y
eso se puede mostrar en un minuto. La ponderación por promedio deja las dos unidades en
la misma escala.

**¿Qué pasa si un estudiante vive en una esquina aislada?** `validarDatos` lo detecta
con los conjuntos disjuntos antes de optimizar y lo reporta como error, en vez de
devolver una ruta que no existe.

**¿Qué pasa si son más estudiantes que puestos?** Clarke-Wright descarta las uniones que
pasarían el cupo y la asignación devuelve `None`; el programa explica que hay que
agregar un bus o puestos, en lugar de repartir de más.

**¿Por qué ocho pesos y no uno?** Porque el peso correcto depende de la geografía del
colegio y no hay forma de saberlo a priori. Ocho corridas cuestan menos de un segundo y
el programa reporta cuál ganó. Es fuerza bruta sobre un solo parámetro, no sobre las
rutas.

**¿Y el orden de inscripción?** Está implementado (`rutaSinOptimizar`, 728) para poder
comparar. Es la línea base: 70.3 km y 155 minutos. Toda la mejora se mide contra eso,
que es lo que el colegio hace hoy a mano.

---

## 8. Lo que se dejó fuera, y por qué

- **OR-Tools / VRP solver**: resolvería mejor y más rápido, pero convierte el proyecto en
  una llamada a una caja negra. El objetivo era entender y poder explicar.
- **Solución exacta del CVRP** (programación entera, branch and bound): correcta e
  inútil aquí; el tiempo de cómputo crece de forma exponencial y no cabe en una ventana
  que recalcula al instante.
- **Metaheurísticas** (recocido, colonia de hormigas, búsqueda tabú): dan mejores
  resultados en instancias grandes; con 18 paradas la diferencia no se nota y el código
  se vuelve mucho más difícil de defender.
- **A\***: sirve para un destino, no para visitar 18 puntos. Dijkstra desde cada origen
  es más simple y el grafo es diminuto.

---

## Referencias

- Clarke, G. y Wright, J. W. (1964). Scheduling of vehicles from a central depot to a
  number of delivery points. *Operations Research*, 12(4), 568-581.
- Croes, G. A. (1958). A method for solving traveling-salesman problems.
  *Operations Research*, 6(6), 791-812.
- Dijkstra, E. W. (1959). A note on two problems in connexion with graphs.
  *Numerische Mathematik*, 1, 269-271.
- Kruskal, J. B. (1956). On the shortest spanning subtree of a graph and the traveling
  salesman problem. *Proceedings of the American Mathematical Society*, 7(1), 48-50.
- Tarjan, R. E. (1975). Efficiency of a good but not linear set union algorithm.
  *Journal of the ACM*, 22(2), 215-225.
- Cormen, T., Leiserson, C., Rivest, R. y Stein, C. (2022). *Introduction to
  Algorithms* (4.ª ed.). MIT Press. Capítulos 6, 19, 21, 22 y 23.
