# Guion de exposición — EfiRuta

**Curso:** Diseño y Análisis de Algoritmos (DDYA) · Escuela Colombiana de Ingeniería · grupo 05
**Formato:** 13 diapositivas · 12 minutos de exposición + preguntas
**Exponen:** Santiago Torres · Thomas Venegas · Diego Prado

Este documento no repite las diapositivas. Dice qué decir en cada una, en qué orden,
cuánto dura, quién habla, y qué preguntas van a hacer después.

---

## 0. Los números que hay que saber de memoria

Si se aprende una sola cosa de este documento, es esta tabla. Todo lo demás se puede
improvisar; estos diez datos no.

| # | Dato | Valor | De dónde sale |
|---|---|---|---|
| 1 | Mapa | 36 esquinas, 54 tramos | Calle 100–134 × Autopista–Carrera 7 |
| 2 | Demanda | 20 estudiantes en 18 paradas | Hermanos comparten esquina |
| 3 | Flota | 3 buses de 8, 7 y 7 puestos | Caso del colegio |
| 4 | Ejecuciones de Dijkstra | 19 | Colegio + 18 paradas |
| 5 | Rutas de inscripción | 70.3 km · 155.4 min · costo 120.86 | Línea base |
| 6 | Rutas EfiRuta | **22.2 km · 64.0 min · costo 38.68** | MVP |
| 7 | Ahorro | **68 % en distancia, 59 % en tiempo** | (base − EfiRuta) / base |
| 8 | Cota de Kruskal | 23.73 | Árbol de expansión mínimo |
| 9 | Brecha | 38.68 / 23.73 = **1.63×** | Nunca estamos más de 63 % sobre el óptimo |
| 10 | Pruebas | **19 de 19** | Celda `10. Plan de pruebas` |

Dos precisiones que evitan que los corrijan en público:

- **"64 minutos" es la suma de los tres recorridos**, no el reloj de pared. El último bus
  entra al colegio a las **6:24 a. m.** (el más largo dura 23.8 min desde las 6:00).
- **"22.2 km" es la suma de los tres buses.** El bus 1 hace 8.6 km, el bus 2 hace 5.4 km
  y el bus 3 hace 8.2 km.

---

## 1. Reparto y tiempos

| # | Diapositiva | Inicio | Duración | Habla | Idea que debe quedar |
|---|---|---|---|---|---|
| 1 | Portada | 0:00 | 0:30 | Santiago | Somos un equipo, hay un caso real |
| 2 | El caso | 0:30 | 0:50 | Santiago | Colegio, 20 estudiantes, 3 buses |
| 3 | El problema | 1:20 | 1:00 | Santiago | Hoy es a mano y cuesta 70.3 km |
| 4 | Lo que proponemos | 2:20 | 1:10 | Thomas | Cuatro decisiones del producto |
| 5 | Qué hace el MVP | 3:30 | 0:50 | Thomas | Carga, calcula, recalcula |
| 6 | Estructuras y algoritmos | 4:20 | 1:20 | Diego | Cada estructura tiene un uso |
| 7 | Caminos mínimos | 5:40 | 1:10 | Santiago | El bus anda por calles, no en línea recta |
| 8 | Árbol mínimo | 6:50 | 1:00 | Diego | Tenemos una cota, no una opinión |
| 9 | Cómo decide | 7:50 | 1:10 | Diego | Tres pasos concretos con números |
| 10 | Demo | 9:00 | 2:30 | Thomas | El programa funciona en vivo |
| 11 | Casos prácticos | 11:30 | 1:00 | Thomas | Un cambio, y las rutas se rehacen solas |
| 12 | Resultados | 12:30 | 1:10 | Santiago | 68 % y 59 %, 19/19 pruebas |
| 13 | Límites y lo que sigue | 13:40 | 0:40 | Diego | Sabemos qué no resolvimos |

> Si el tiempo se recorta a 8 minutos: se saltan las diapositivas 2 y 9, y la demo baja a
> 1:30. Nunca se salta la 8 ni la 13 — son las que dan credibilidad.

---

## 2. Libreto, diapositiva por diapositiva

### 1 · Portada (0:30) — Santiago

**Objetivo:** que sepan quiénes son y de qué va la cosa, en una frase.

> "Buenos días. Somos Santiago Torres, Thomas Venegas y Diego Prado, del grupo 05.
> Presentamos EfiRuta: un programa que arma las rutas de los buses escolares de un colegio
> de Bogotá. Hoy esas rutas se arman a mano; nosotros las calculamos, las explicamos y las
> recalculamos cuando algo cambia."

**No digas:** "somos estudiantes y esto es un proyecto de clase". Empieza como si fuera un
producto. El contexto académico se sobreentiende por la materia.

---

### 2 · El caso (0:50) — Santiago

**Objetivo:** que el jurado pueda dibujar la escena mentalmente.

> "El cliente es un colegio de Bogotá con servicio de buses. Los usuarios son dos: el
> coordinador de transporte, que arma las rutas, y los padres, que quieren saber por dónde
> va su hijo. Los beneficiarios son los estudiantes.
>
> El caso concreto: 20 estudiantes, 3 buses de 8, 7 y 7 puestos, y una zona de la ciudad
> entre la Calle 100 y la Calle 134. El colegio está en la Calle 116 con Carrera 11."

**Señala:** el mapa de la diapositiva. Que vean que es una zona real, no un grafo abstracto.

---

### 3 · El problema (1:00) — Santiago

**Objetivo:** que el 70.3 km duela.

> "Hoy el coordinador arma las rutas con la experiencia del conductor. Eso tiene tres
> consecuencias.
>
> Uno: se recorre más de lo necesario. Si se recogen los 20 estudiantes en el orden en que
> se inscribieron, el bus hace 70.3 kilómetros y los estudiantes pasan 155 minutos arriba
> del bus, sumando los tres recorridos.
>
> Dos: cualquier cambio obliga a rehacer todo a mano. Entra un estudiante, cierran una
> calle, y el coordinador vuelve a empezar, con el riesgo de dejar un bus con más
> estudiantes que puestos.
>
> Tres: los padres no saben nada. Llaman al colegio para preguntar dónde va el bus."

**Transición:** "Esos tres problemas son los tres frentes del MVP."

---

### 4 · Lo que proponemos (1:10) — Thomas

**Objetivo:** cuatro decisiones, no una lista de features.

> "Nuestra propuesta tiene cuatro decisiones.
>
> Primero, repartir: asignamos estudiantes a buses sin pasarnos nunca del cupo. Es una
> restricción dura, no un deseo.
>
> Segundo, ordenar: calculamos la ruta de la mañana y la de la tarde para cada bus.
>
> Tercero, ponderar: cuando dos rutas empatan en kilómetros pero una gasta más tiempo,
> preferimos la rápida. Usamos 0.8 de distancia y 0.2 de tiempo. Es una decisión de
> negocio, no un número mágico: al colegio le importa más el kilómetro, que es combustible
> y desgaste, que el minuto.
>
> Cuarto, explicar: el programa muestra cada decisión que tomó y permite buscar a un
> estudiante por su id. Un resultado que no se puede explicar no sirve para operar."

---

### 5 · Qué hace el MVP (0:50) — Thomas

> "El MVP hace tres cosas y solo tres. Carga y valida los datos: si un estudiante vive en
> una esquina sin camino al colegio, lo dice antes de calcular. Calcula las rutas y mide qué
> tan buenas son. Y recalcula cuando entra o sale un estudiante o se cierra una calle.
>
> No tiene GPS. Lo digo de una vez para que nadie se lleve una sorpresa: la posición del bus
> es una simulación sobre un reloj. Lo que sí es real es la geometría, las distancias y el
> orden de las paradas."

Decir en voz alta lo que **no** hace, temprano, desarma la mitad de las preguntas duras.

---

### 6 · Estructuras y algoritmos (1:20) — Diego

**Objetivo:** que quede claro que ninguna estructura está ahí de adorno.

> "Elegimos seis estructuras y cada una responde una pregunta distinta.
>
> El grafo responde dónde se puede andar: 36 esquinas, 54 tramos, cada tramo con un costo.
> Dijkstra responde cuál es el camino de menor costo entre dos paradas, y usa un montón
> mínimo. Clarke-Wright responde cómo repartir y en qué orden, y usa un montón máximo y
> conjuntos disjuntos. Kruskal responde qué tan buena es nuestra ruta, y usa conjuntos
> disjuntos también. La tabla hash responde quién es el estudiante 1003, en tiempo
> constante. La pila arma el recorrido calle por calle a partir de los padres de Dijkstra.
> Y la cola simula el bus avanzando por las paradas."

**Truco de memoria:** grafo → dónde; Dijkstra → cuánto; Clarke-Wright → cómo reparto;
Kruskal → qué tan bueno; hash → quién; pila y cola → cómo lo muestro.

---

### 7 · Caminos mínimos (1:10) — Santiago

**Objetivo:** justificar Dijkstra con un argumento que no sea "porque es el que vimos".

> "Un bus no va en línea recta: va por calles. Por eso la distancia entre dos paradas no es
> la euclidiana, es el camino de menor costo en el grafo.
>
> El costo de un tramo combina distancia y tiempo: 0.8 por los kilómetros normalizados, más
> 0.2 por los minutos normalizados. Normalizamos porque no se pueden sumar kilómetros con
> minutos; se divide cada uno por el promedio del mapa, que es 0.57 km y 1.24 min por tramo.
>
> Con eso, dos tramos de medio kilómetro pueden costar distinto. Ir por la Autopista cuesta
> 0.83; ir por la Carrera 11 cuesta 0.95, porque la Carrera 11 es más lenta. El programa
> prefiere la Autopista, y eso es exactamente lo que haría un coordinador con experiencia.
>
> Dijkstra funciona porque todos los costos son positivos, y el montón mínimo siempre
> entrega la esquina más barata. Cuando una esquina sale del montón por primera vez, su
> costo ya es el mínimo. Corre en O((V+E) log V) por origen y lo ejecutamos 19 veces: una
> desde el colegio y una desde cada una de las 18 paradas."

**Si preguntan por qué no Floyd-Warshall:** estamos en la diapositiva 7 y la respuesta es la
de la sección 4 de este documento, pregunta 1.

---

### 8 · Árbol mínimo (1:00) — Diego

**Objetivo:** esta es la diapositiva que separa un proyecto de una demo. No la improvises.

> "Aquí viene la parte que casi nadie hace: no solo calculamos una ruta, sabemos qué tan
> lejos está del óptimo.
>
> Cada bus hace un ciclo que sale del colegio, pasa por sus paradas y vuelve. Los tres
> ciclos juntos conectan el colegio con las 18 paradas. Cualquier árbol que conecte esos 19
> puntos pesa, como mínimo, lo que pesa el árbol de expansión mínimo. Y el árbol de
> expansión mínimo pesa 23.73.
>
> Entonces el óptimo verdadero está entre 23.73 y nuestros 38.68. Nuestra ruta no puede
> estar más de un 63 % por encima del óptimo. No es una estimación: es una cota.
>
> Kruskal la calcula sacando las aristas de un montón mínimo y usando conjuntos disjuntos
> para no formar ciclos. Con unión por rango y compresión de caminos, cada operación cuesta
> O(α(n)) amortizado, prácticamente constante."

**No digas:** "nuestra ruta es óptima". No lo es, y con esta misma diapositiva te lo
pueden demostrar.

---

### 9 · Cómo decide el programa (1:10) — Diego

**Objetivo:** bajar de la teoría a tres decisiones concretas y verificables.

> "Tres ejemplos de decisiones que tomó el programa en este caso.
>
> Uno, el costo por tramo: entre dos esquinas a la misma distancia, eligió la vía rápida.
>
> Dos, Clarke-Wright: empieza con una ruta por parada y va uniendo los pares que más
> ahorran. Si al unir dos rutas el bus pasaría el cupo, no las une y lo registra. Eso queda
> escrito en la pestaña Decisiones: cuántas uniones descartó y por qué.
>
> Tres, 2-opt: después de unir, revisa si invertir un tramo de la ruta la acorta. Si sí, lo
> invierte, y repite hasta que ninguna inversión mejore.
>
> Y al final, para cada bus elige el sentido del recorrido comparando en cuál los
> estudiantes pasan menos minutos a bordo."

---

### 10 · Demo (2:30) — Thomas

Ver la sección 3. **No improvises el orden de los clics.**

---

### 11 · Casos prácticos (1:00) — Thomas

> "Tres cosas que puede hacer el coordinador sin tocar el código.
>
> Un padre busca a Sofía. Le dice: va en el bus 2, el bus va a 2.0 km del colegio y llega
> en 7 minutos. Eso sale de la simulación, no de un GPS.
>
> Entra Emilia al colegio. El coordinador la agrega con su esquina y las rutas se rehacen
> solas: pasa de 22.2 a 22.4 km, y Emilia queda en el bus 3.
>
> Cierran la Calle 116 entre Carrera 15 y Carrera 11. Las rutas se recalculan sin pasar por
> ahí: 23.1 km y 69 minutos. Si con el cierre algún estudiante quedara sin camino al
> colegio, el programa lo dice con nombre y esquina en vez de entregar una ruta inválida."

---

### 12 · Resultados (1:10) — Santiago

> "Los resultados del caso principal.
>
> Contra el orden de inscripción: 68 % menos distancia y 59 % menos tiempo. En costo
> ponderado, de 120.86 a 38.68.
>
> Contra el óptimo: como máximo 63 % por encima, y eso está medido, no estimado.
>
> Un caso donde sí podemos probar optimalidad: con un solo bus el problema es un TSP
> pequeño, y comparamos nuestra ruta contra todas las permutaciones. Da la misma. Está en
> la prueba P9.
>
> Y 19 de 19 pruebas pasan. Incluyen comparar Dijkstra contra la relajación completa, que
> es la definición de camino mínimo, no una implementación parecida."

**Si preguntan cómo se calculó el 68 %:** (70.3 − 22.2) / 70.3 = 68.4 %. Tenlo listo.

---

### 13 · Límites y lo que sigue (0:40) — Diego

**Objetivo:** cerrar con honestidad. Esta diapositiva sube la nota; no la escondas.

> "Tres límites, y los decimos nosotros antes de que los pregunten.
>
> Con varios buses no garantizamos el óptimo. Es una heurística, y la cota del 63 % es lo
> mejor que podemos afirmar.
>
> La posición del bus es simulada. No hay GPS, ni tráfico en tiempo real, ni calles de un
> solo sentido: todas las vías son de doble sentido y con velocidad fija.
>
> Lo que sigue: modelar el tráfico por franja horaria, permitir vías de un solo sentido, y
> reemplazar la búsqueda sobre 8 pesos de ahorro por un solver de ruteo con ventanas de
> tiempo, que es el paso natural cuando el colegio crezca."

---

## 3. Demo en vivo, paso a paso

Abre la ventana **antes** de empezar a hablar. Cinco clics, en este orden exacto.

| Paso | Acción | Qué decir mientras lo haces | Resultado esperado |
|---|---|---|---|
| 1 | Ventana abierta, turno **Mañana**, reloj en 0 | "Este es el mapa: 36 esquinas, 54 tramos, el colegio marcado en negro y tres rutas de colores." | Tres polilíneas y el colegio |
| 2 | Pestaña **Rutas** | "22.2 km y 64 minutos contra 70.3 y 155 del orden de inscripción. Y aquí abajo: las rutas cuestan 1.63 veces la cota." | Totales en el panel |
| 3 | Pestaña **Decisiones**, clic en el paso 1, luego en uno de Clarke-Wright, luego en uno descartado por cupo | "No solo da la ruta: dice por qué. Aquí se ve una unión que se descartó porque el bus pasaba el cupo." | Esquinas resaltadas en amarillo |
| 4 | Marca **Ver árbol mínimo (Kruskal)** | "Este es el árbol que nos da la cota: 23.73." | Líneas azules punteadas |
| 5 | **Iniciar recorrido**, sube velocidad a 3×, **Pausar** cerca del minuto 10 (o arrastra el reloj a **6:10**) | "Los buses arrancan a las 6:00 y el reloj avanza." | Buses moviéndose entre paradas |
| 6 | Pestaña **Padres** → elige **1003 - Sofia** | "El padre de Sofía: está en el bus 2, el bus va a 2.0 km del colegio y llega en 7 minutos." | En el bus · 2.0 km · 7 min |
| 7 | Pestaña **Coordinador** → Id `1021`, Nombre `Emilia`, Esquina **Cl 122 con Kr 11** → **Agregar** | "Entra una estudiante nueva. Las rutas se rehacen solas." | 22.4 km, Emilia en el bus 3 |
| 8 | **Cerrar una calle** → Desde **Cl 116 con Kr 15**, Hasta **Cl 116 con Kr 11** → **Cerrar** | "Cierran la Calle 116. Rutas nuevas: 23.1 km." | 23.1 km · 68.8 min |
| 9 | **Volver al caso inicial** | "Y volvemos al caso base." | 22.2 km |

**Los números exactos que va a mostrar la ventana** (para que nadie te corrija):

- Base: 22.2 km · 63.95 min · costo 38.68 · árbol 23.73 · 1.63×
- Con Emilia (Cl 122 con Kr 11): 22.4 km · 64.9 min · bus 3
- Con la Calle 116 cerrada: 23.1 km · 68.8 min
- Sofía a las 6:10: bus 2 · "En el bus" · 2.0 km al colegio · 7 min para llegar

**Si algo falla en vivo:**

1. No lo arregles frente al jurado. Di "el recálculo lo tengo en el cuaderno" y abre la celda
   `11. Plan de demo`, que ya tiene las salidas guardadas.
2. Si la ventana no abre, sigue con las diapositivas 11 y 12. La demo es el 15 % de la nota;
   el argumento es el 85 %.
3. Ten el PDF de las diapositivas abierto en otra pestaña, siempre.

---

## 4. Preguntas del jurado

Las quince más probables, con la respuesta corta. La respuesta corta primero, el detalle
después: si te extiendes, se pierde.

**1. ¿Por qué Dijkstra y no Floyd-Warshall?**
Porque no necesitamos todos los pares de las 36 esquinas: necesitamos los caminos entre 19
puntos. Además necesitamos el árbol de padres para reconstruir el recorrido calle por calle,
y eso Dijkstra lo da gratis. Floyd-Warshall es O(V³) y no devuelve el camino sin trabajo
adicional.

**2. ¿El resultado es óptimo?**
Con un bus sí, y lo probamos contra todas las permutaciones (P9). Con tres buses no: es una
heurística. Lo máximo que afirmamos es que no estamos más del 63 % sobre el óptimo, y eso
está demostrado con la cota de Kruskal.

**3. ¿Cómo funciona esa cota, exactamente?**
Cada ruta es un ciclo que sale del colegio y vuelve. La unión de los tres ciclos es un grafo
conexo que cubre el colegio y las 18 paradas. Todo grafo conexo contiene un árbol de
expansión que pesa menos o igual que la suma de sus aristas. El árbol mínimo es el menor de
todos esos árboles. Entonces: peso del árbol ≤ óptimo ≤ nuestra ruta. 23.73 ≤ óptimo ≤ 38.68.

**4. ¿De dónde salen 0.8 y 0.2?**
Es una decisión de negocio, no un resultado. Al colegio le pesa más el kilómetro porque es
combustible y mantenimiento. Normalizamos cada término por el promedio del mapa para poder
sumarlos. Si el colegio priorizara el tiempo del estudiante, se cambia a 0.5/0.5 y se
recalcula: son dos constantes.

**5. ¿Por qué no resuelven el problema exacto?**
Porque con flota y capacidad el problema es un ruteo de vehículos con capacidad, que es
NP-difícil. Exacto requiere programación entera o programación dinámica sobre subconjuntos.
Con 18 paradas es alcanzable en teoría, pero con varios vehículos deja de ser un TSP y pasa
a ser un CVRP. Preferimos una heurística que corre en 9 milisegundos y explicar su brecha.

**6. ¿Por qué Clarke-Wright y no vecino más cercano?**
Porque el vecino más cercano construye una ruta desde cero y no sabe de cupos. Clarke-Wright
parte de rutas individuales y solo las une si el ahorro es positivo y el cupo lo permite, así
que la restricción de capacidad entra en la construcción, no como parche posterior.

**7. ¿Por qué implementaron su propio montón y su propio Union-Find?**
Porque es el objeto de la materia: implementar las estructuras, no importarlas. Y sobre eso
corregimos: el `insert` original reconstruía el montón completo, lo pasamos a O(log n); y los
conjuntos disjuntos pasaron de búsqueda lineal a unión por rango con compresión de caminos,
O(α(n)) amortizado.

**8. ¿Qué pasa si los puestos no alcanzan?**
Se detecta antes de calcular: total de estudiantes contra suma de cupos, y también el caso de
una sola parada con más estudiantes que el bus más grande. La ventana no entrega una ruta
inválida: muestra el error en rojo y deja el plan anterior.

**9. ¿Y si al cerrar una calle alguien queda incomunicado?**
Los conjuntos disjuntos de la validación dicen si la esquina del estudiante sigue en el mismo
componente que el colegio. Si no, el mensaje nombra al estudiante y su esquina. Está en las
pruebas P15 y P16.

**10. ¿Los datos son reales?**
Los nombres de las vías son reales y la geometría es coherente con la zona. Las distancias
salen de las coordenadas del mapa simplificado, no de un GPS, y las velocidades son
aproximadas: 40 km/h en la Autopista, 30 en avenidas, 20 en calles de barrio.

**11. ¿Cómo escala a 300 estudiantes y 15 buses?**
El cuello de botella es la matriz de costos entre paradas: hoy son 19 Dijkstra. Con 250
paradas son 250 Dijkstra sobre el mismo grafo, y Clarke-Wright pasa a O(k² log k) con k=250,
que sigue siendo milisegundos. Lo que habría que cambiar es el solver: a ese tamaño conviene
OR-Tools con ventanas de tiempo. La interfaz también necesitaría paginación.

**12. ¿La ruta de la tarde es simplemente la inversa?**
Sí. Con costos simétricos y sin ventanas de tiempo, el espejo es razonable. Con tráfico
asimétrico habría que recalcularla por separado: es una de las cosas que dejamos como
trabajo futuro.

**13. ¿Por qué el bus 2 va con 5 de 7 puestos?**
Porque las rutas se construyen apuntando al bus más grande, que tiene 8, y después se
asignan por carga: la ruta más llena al bus más grande. De los ocho pesos de ahorro que
probamos, el reparto más barato en kilómetros fue ese. Es una consecuencia de optimizar
distancia total, no de repartir parejo. Si el colegio prefiere equilibrio, se cambia la
función objetivo.

**14. ¿Cómo se que el programa no se equivoca?**
Tres pruebas hacen el trabajo pesado: P3 compara Dijkstra contra la relajación completa, que
es la definición; P4 verifica que ninguna ruta cueste menos que el árbol mínimo; y P9
compara el caso de un bus contra fuerza bruta. Además P1 verifica los invariantes de negocio:
cada estudiante una sola vez, ningún bus pasado de cupo, toda ruta sale y vuelve del colegio.

**15. ¿Qué no resolvieron?**
Tráfico por franja horaria, vías de un solo sentido, ventanas de tiempo ("el bus debe pasar
por esta casa antes de las 6:20"), y optimalidad con varios buses. Las cuatro están en la
última diapositiva a propósito.

---

## 5. Frases que no se dicen

| No digas | Di |
|---|---|
| "La ruta es óptima" | "Con un bus es óptima; con tres, es una heurística con brecha máxima del 63 %" |
| "Es la ruta más corta" | "Es la ruta de menor costo ponderado" |
| "GPS en tiempo real" | "Simulación sobre un reloj, sin GPS" |
| "Usamos IA" | "Usamos Dijkstra, Clarke-Wright, 2-opt y Kruskal" |
| "Es como Google Maps" | "Es un planificador de rutas con restricción de cupo" |
| "Ahorra X minutos por estudiante" | No se midió. Di minutos totales de bus, que sí están medidos |
| "Obviamente" / "como todos saben" | Nada. Si es obvio, no lo expliques |

Y la regla de oro: **no leas las diapositivas.** Nadie califica a quien lee.

---

## 6. Checklist, diez minutos antes

- [ ] La ventana de escritorio abre y muestra 22.2 km.
- [ ] El cuaderno está **ejecutado** (con salidas guardadas), no en blanco.
- [ ] El PDF del pitch está abierto en otra pestaña.
- [ ] Cada uno sabe qué diapositivas le tocan y quién hace la demo.
- [ ] El reloj de la demo está en 3×, no en 1× (si no, no alcanza).
- [ ] Nadie dice "óptimo" sin la palabra "con un bus".
- [ ] Se sabe de memoria: 36, 54, 20, 3, 19, 22.2, 70.3, 38.68, 23.73, 1.63, 19/19.
