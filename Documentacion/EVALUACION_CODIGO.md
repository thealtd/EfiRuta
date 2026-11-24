# Evaluación de código — EfiRuta

**Alcance revisado:** `3_Ventana_de_escritorio/efiruta_escritorio/` (`logica.py` 848 líneas,
`app.py` 696 líneas), el cuaderno del Momento 2 (33 celdas, 3 celdas de código con la lógica:
273 + 65 + 504 líneas), el cuaderno de entrega final, `README.md`, `requirements.txt` e
historial de git (6 commits).

**Método:** lectura completa del código, ejecución del motor, ejecución de la suite de
pruebas del cuaderno y contraste de cada número publicado en el pitch. No es una revisión de
estilo: cada hallazgo tiene archivo, línea y consecuencia.

---

## 1. Veredicto

> Código de curso, hecho con más rigor del que el curso pide: las estructuras son propias y
> correctas, los invariantes están escritos antes de implementarse, y el proyecto mide su
> propia brecha contra el óptimo en vez de afirmar que su heurística es buena. Lo que le
> falta no es algoritmo: es ingeniería de software alrededor del algoritmo (una sola fuente
> de verdad, pruebas ejecutables fuera del notebook, separación entre datos, lógica e
> interfaz).

| Dimensión | Peso | Nota | Motivo en una línea |
|---|---|---|---|
| Modelado y estructuras de datos | 15 % | **9.0** | Grafo, montón, hash y Union-Find propios, con las operaciones que el caso necesita |
| Algoritmos y justificación | 20 % | **8.5** | Dijkstra + Clarke-Wright + 2-opt + Kruskal, cada uno con un uso declarado |
| Correctitud e invariantes | 15 % | **8.0** | Números reproducidos exactos; invariantes verificados; heurística declarada como tal |
| Pruebas | 15 % | **7.0** | 19 pruebas fuertes en contenido, débiles en infraestructura (viven en una celda) |
| Documentación y trazabilidad | 10 % | **9.0** | Cuadernos, README y mensajes de decisión en tiempo de ejecución |
| Interfaz y usabilidad | 10 % | **8.0** | Funcional y clara; una clase de 696 líneas mezcla vista, estado y simulación |
| Mantenibilidad y arquitectura | 10 % | **5.5** | Lógica duplicada, `import *`, datos del caso incrustados en el módulo de lógica |
| Rendimiento | 5 % | **8.0** | 9 ms para el caso completo; hay trabajo redundante que no duele a este tamaño |
| **Total ponderado** | **100 %** | **8.0 / 10** | |

**Cómo leer el 8.0.** Como proyecto de DDYA es un 8 sólido, con partes de 9. Como base para
poner esto a operar en un colegio real es un **5.5**: no porque el algoritmo falle, sino
porque hay dos copias de la lógica que van a divergir, las pruebas no corren en ningún lado
automáticamente, y cambiar de colegio exige editar el código fuente.

---

## 2. Qué hay en el repositorio

| Componente | Archivo | Tamaño | Rol |
|---|---|---|---|
| Motor | `logica.py` | 848 líneas, 58 funciones/clases | Estructuras, datos del caso y solución |
| Vista | `app.py` | 696 líneas, clase `App` | Tkinter: mapa, pestañas, simulación |
| Cuaderno Momento 2 | `1_Cuaderno.../*.ipynb` | 7 celdas de código | Copia de la lógica + gráficas + demo + pruebas |
| Cuaderno final | `2_Cuaderno.../*.ipynb` | 7 celdas de código | Igual, con el guion del pitch ampliado |
| Pitch | `4_Diapositivas/` | 13 diapositivas | PPTX + PDF |
| Dependencias | `requirements.txt` | 1 línea | Solo `matplotlib` (los cuadernos); la app usa solo la stdlib |

Dato relevante para todo lo que sigue: **la lógica existe dos veces.** Comparé función por
función las celdas 19–21 del cuaderno contra `logica.py`: son **58 de 58 funciones
idénticas**, sin una sola diferencia de cuerpo. Hoy no divergen. Mañana sí.

---

## 3. Evidencia verificada

Todo esto lo ejecuté sobre el repositorio, no lo deduje leyendo.

```
Mapa           36 nodos, 54 tramos, 0 errores de validación
Rutas          22.20 km | 63.95 min | costo 38.68 | árbol 23.73 | ratio 1.63
Línea base     70.30 km | 155.40 min | costo 120.86
Reparto        bus1 8/8 (8.6 km) · bus2 5/7 (5.4 km) · bus3 7/7 (8.2 km)
Tiempo motor   0.009 s  (caso completo, incluida la búsqueda sobre 8 pesos)
Pruebas        19 de 19 pasaron
Demo           Emilia (Cl122-Kr11) → 22.4 km; cierre Cl116 Kr15–Kr11 → 23.1 km / 68.8 min
Padres         1003 Sofía a las 6:10 → bus 2, en el bus, 2.0 km, 7 min para llegar
```

Los tres números del pitch que más se prestan a error — 22.2 km, 1.63×, 68 %/59 % — coinciden
exactamente con lo que produce el código. Eso es más de lo que se puede decir de la mayoría
de proyectos de curso, y es el hallazgo más importante de esta evaluación: **lo que el
proyecto afirma, el proyecto lo cumple.**

---

## 4. Fortalezas

Lo que está bien hecho, y por qué está bien hecho (no solo que existe).

**4.1 Cada estructura responde una pregunta del caso.**
No hay una estructura decorativa. El grafo existe porque el bus anda por calles; el montón
porque hay que sacar siempre el mínimo; el hash porque el padre pregunta por un id, no por un
nombre; la pila porque el camino de Dijkstra se reconstruye al revés; la cola porque el bus
avanza por paradas en orden. El cuaderno lo declara en la sección 7 y el código lo cumple.

**4.2 Los invariantes se escribieron antes que el código.**
La sección 8 del cuaderno enumera precondiciones, poscondiciones e invariantes por operación
(`calcularRutas`, `dijkstra`, `kruskal`, `consultarEstudiante`, `cerrarCalle`, `findSet`).
Y las pruebas verifican esos invariantes, no detalles de implementación. Eso es diseño, no
documentación posterior.

**4.3 La suite de pruebas ataca lo que de verdad puede estar mal.**
Tres pruebas valen por veinte:

- **P3** compara `dijkstra` contra la relajación completa de todas las calles (estilo
  Bellman-Ford), que es la *definición* de camino mínimo. No compara contra otra
  implementación parecida.
- **P4** verifica que el árbol mínimo pese menos o igual que la suma de las rutas y que el
  árbol estrella, es decir, comprueba la cota contra el resultado, no la cota contra sí misma.
- **P9** compara el caso de un solo bus contra **todas las permutaciones**. Es la única
  prueba de optimalidad real del proyecto, y está donde se puede hacer.

Y hay dos pruebas que solo se le ocurren a quien pensó en los bordes: **P10** pone a una
estudiante a vivir en la misma esquina del colegio (el caso degenerado que rompe medias
docenas de implementaciones de TSP) y verifica que igual reciba bus; **P15** cierra las dos
calles que llegan a una esquina y verifica que el error nombre al estudiante afectado en vez
de entregar una ruta inválida.

**4.4 `asignarBuses` es un greedy correcto, no un greedy afortunado.**
Ordena rutas y buses de mayor a menor y empareja. Eso decide correctamente si existe reparto
posible: si el i-ésimo recorrido (ordenado) excede el i-ésimo cupo (ordenado), hay i recorridos
que necesitan un cupo estrictamente mayor que `c_i`, y solo existen `i−1` buses así. Se puede
demostrar por intercambio. Es un detalle que casi nadie implementa bien.

**4.5 El proyecto mide su propia ignorancia.**
Usar el árbol de expansión mínimo como cota inferior y publicar el 1.63× es la diferencia
entre "creemos que la ruta es buena" y "la ruta no puede estar más de 63 % sobre el óptimo".
La demostración es correcta: cada ruta es un ciclo por el colegio, la unión de los ciclos es
conexa y cubre colegio + paradas, todo grafo conexo contiene un árbol que pesa menos o igual,
y el árbol mínimo es el menor de esos árboles.

**4.6 Honestidad en los límites.**
El código y el pitch dicen lo mismo: heurística, posición simulada, vías bidireccionales,
velocidad fija. No hay sobreventa. Eso es raro y vale.

**4.7 Superficie de ataque prácticamente nula.**
Sin red, sin base de datos, sin `eval`, sin `pickle`, sin secretos, sin escritura de archivos.
Las únicas entradas externas son tres campos de formulario y un combo, y todos se validan
antes de tocar el motor (`alAgregar`, `alCambiarBuses`, `alCerrar`). No hay nada que explotar
aquí; el riesgo real es de datos personales, no de seguridad técnica.

---

## 5. Hallazgos priorizados

Severidad: **A** = arreglar antes de que el proyecto crezca · **M** = deuda que va a doler ·
**B** = mejora de calidad.

| ID | Sev | Ubicación | Hallazgo | Consecuencia |
|---|---|---|---|---|
| A1 | Alta | `logica.py` completo ↔ celdas 19–21 del cuaderno | La lógica está duplicada y hoy es idéntica (58/58 funciones) | Dos fuentes de verdad; el primer cambio en una sola copia rompe la otra en silencio |
| A2 | Alta | Celda `10. Plan de pruebas` (253 líneas) | Las pruebas viven dentro del notebook, en un solo `ejecutar_pruebas()` que cuenta booleanos | No hay `pytest`, no hay CI, no hay cobertura, no se puede correr en un commit |
| M1 | Media | `app.py:7` | `from logica import *` | Dependencias invisibles: `CALLES`, `BUSES`, `MINUTOS_POR_PARADA` aparecen sin origen; un nombre nuevo en `logica.py` pisa el de `app.py` |
| M2 | Media | `logica.py:283-314` | Mapa, estudiantes y flota incrustados en el módulo de lógica | Cambiar de colegio o de zona exige editar el código, no pasar un dato |
| M3 | Media | `logica.py:619` (`calcularRutas`) | Muta `caso['tabla']` y el `plan` devuelto referencia estructuras del `caso` | Propiedad de estado ambigua; el plan no es un resultado, es una vista del caso |
| M4 | Media | `app.py` (clase `App`, 696 líneas) | Vista, estado y simulación en una sola clase con más de 30 métodos | No se puede probar la interfaz ni el estado sin abrir una ventana |
| M5 | Media | `logica.py:627` (`capMax`) + `653` | Clarke-Wright siempre apunta al cupo mayor; si el reparto resultante no encaja, solo se reintenta con otro peso de ahorro | Puede reportar "no se logró repartir" habiendo otro reparto válido. No ocurre con el caso del colegio |
| B1 | Baja | `logica.py:14, 57, 59` | `data=[]` como valor por defecto y `self.data = data` aliasan la lista | `build()` llamado directo mutaría la lista del llamador. Hoy no explota porque `__init__` pasa `data[:]` |
| B2 | Baja | `logica.py:122-146` | `delete` muta la lista mientras la recorre; `search` devuelve `None` tanto para "no existe" como para "existe con valor `None`" | Funciona por el `return` inmediato; la ambigüedad la sostiene `agregarEstudiante` |
| B3 | Baja | `logica.py:256-276` | Dijkstra sin *decrease-key*: encola duplicados; guarda estado en la instancia (`v_props`, `order`) | O(E log E) en vez de O(E log V); el grafo no es reentrante ni seguro con dos hilos |
| B4 | Baja | `app.py:322` | Deduplica aristas con `if u < v` | Comparación lexicográfica de strings usada como clave de conjunto; se rompe si cambia el formato de los ids |
| B5 | Baja | `app.py:315, 547` | `dibujarMapa` borra y redibuja todo en cada `<Configure>`, sin debounce | Parpadeo y trabajo repetido al redimensionar. A 36 nodos no duele; a 300 sí |
| B6 | Baja | `logica.py:645` | Los km se miden sobre el camino de menor **costo**, no de menor km | Es consistente para comparar, pero no es "la ruta más corta en kilómetros": hay que nombrarlo así |
| B7 | Baja | `logica.py:686` | La tarde es el espejo de la mañana y el sentido se elige con la semántica de la mañana | Correcto con costos simétricos y sin ventanas de tiempo; no con tráfico asimétrico |
| B8 | Baja | `logica.py`, `app.py` | Sin type hints; `camelCase` en funciones | Sin mypy, sin autocompletado útil; es la convención del curso, pero es deuda |
| B9 | Baja | `logica.py:314` | `PESOS_AHORRO` es una rejilla de 8 valores sin justificación | El resultado depende de la rejilla elegida; hay que presentarlo como heurística, no como parámetro |
| I1 | Info | — | Sin red, BD, `eval`, secretos ni escritura de archivos | Superficie de ataque nula |
| I2 | Info | `logica.py:297` | Nombres de estudiantes en el código | Con datos reales aplica la Ley 1581 de 2012 (Colombia): anonimizar antes de cualquier demo pública |
| I3 | Info | `requirements.txt` | Sin lockfile, sin CI, sin versión de Python declarada | "Funciona en mi máquina" documentado como instrucción, no como garantía |

---

## 6. Los seis hallazgos que importan, en detalle

### A1 · Dos copias de la misma lógica

**Qué pasa.** `logica.py` es una copia literal de las celdas 19, 20 y 21 del cuaderno. Lo
verifiqué función por función: 58 funciones en ambas partes, mismos nombres, mismos cuerpos,
cero diferencias. La primera línea de `logica.py` lo admite: *"el mismo código de las celdas
del cuaderno"*.

**Por qué importa.** El proyecto tiene dos públicos: el jurado lee el cuaderno, el usuario
abre la ventana. Un arreglo en cualquiera de los dos lados deja el otro desactualizado, y no
hay nada que lo detecte. Y ya pasó una vez en la historia del repo: el commit `1db360a`
(*"perf(motor): conjuntos disjuntos con Union-Find"*) tuvo que tocar los dos, y el script
`_analisis/parchear_cuadernos.py` existe justamente porque sincronizar a mano es un problema.

**Arreglo.** Una sola fuente. La más barata para un proyecto así:

```python
# primera celda de código del cuaderno
%run -i ../3_Ventana_de_escritorio/efiruta_escritorio/logica.py
```

o `sys.path.append` + `from logica import *` si el cuaderno y la app comparten carpeta. El
cuaderno queda como *cliente* del motor, que es lo que ya es conceptualmente.

**Esfuerzo:** 20 minutos. **Riesgo:** nulo. **Ganancia:** elimina la clase de bug más cara
del proyecto.

---

### A2 · Las pruebas no son ejecutables fuera del notebook

**Qué pasa.** Las 19 pruebas están en una celda de 253 líneas con una función
`ejecutar_pruebas()` que llama a `reportar(...)` y va acumulando `True`/`False` en una lista.
El resultado es una línea impresa: `19 de 19 pruebas pasaron`.

**Por qué importa.** No es que las pruebas sean malas — son mejores que el promedio. Es que
no se pueden ejecutar en un `git push`. Nadie va a abrir Colab, *Ejecutar todas*, bajar hasta
la celda 26 y leer una impresión antes de cada commit. Y cuando una falle, el diagnóstico es
"1 de 19 falló" más una línea de texto, sin traza ni caso aislado.

Hay además una dependencia oculta: `casoDePrueba` usa la lista global `casos_de_prueba`, que
se define en la celda **23** (la demo), no en la de pruebas. Corrí la celda de pruebas sin la
23 y falla con `NameError: name 'casos_de_prueba' is not defined`. La suite depende de una
celda que no es suya.

**Arreglo.** Extraer a `tests/test_logica.py` con `unittest` (stdlib, sin dependencias):

```python
class TestDijkstra(unittest.TestCase):
    def test_coincide_con_relajacion_completa(self):
        ...
    def test_un_bus_igual_a_fuerza_bruta(self):
        ...
```

Los `reportar(...)` se convierten en `assert` y el mensaje observado pasa a ser el mensaje
del `assert`. Se conservan los 19 casos; se pierde cero contenido y se gana `python -m
unittest` en CI.

**Esfuerzo:** 3–4 horas. **Ganancia:** es el requisito para cualquier trabajo futuro sobre
el motor.

---

### M1 · `from logica import *` esconde el contrato

`app.py:7`. La consecuencia práctica: leyendo `app.py` no se sabe de dónde salen `CALLES`,
`CARRERAS`, `BUSES`, `MINUTOS_POR_PARADA` ni `SALIDA_MANANA`. Y al revés: cualquier nombre
nuevo que se agregue a `logica.py` puede pisar silenciosamente algo de `app.py`.

Además acopla la vista a constantes del caso. `app.py` dibuja las etiquetas del mapa iterando
`CALLES` y `CARRERAS` (líneas 337–343), así que la vista conoce el dataset. Lo correcto es que
el caso exponga sus vías y la vista las consuma del caso, no del módulo.

**Arreglo:** `import logica` y prefijo explícito, o `from logica import (calcularRutas,
construirMapa, construirCaso, consultarEstudiante, ...)` con la lista completa. Se ve el
contrato de un vistazo y un renombre rompe en el import, no en ejecución.

---

### M2 · El caso está dentro del motor

`logica.py:283-314`: `CARRERAS`, `CALLES`, `SIN_PASO`, `COLEGIO`, `ESTUDIANTES` (20 tuplas),
`BUSES`, `PESO_DISTANCIA`, `PESO_TIEMPO`, `TAMANO_TABLA`, `PESOS_AHORRO`. Todo a nivel de
módulo.

El propio código demuestra que el diseño quería otra cosa: `construirCaso(nodos, coords,
tramos, colegio, estudiantes, capacidades)` **sí** recibe los datos como parámetros. El
problema es que `App.crearCaso` (`app.py:77`) y `alRestablecer` (`app.py:681`) se los pasan
desde las constantes globales, así que la parametrización existe pero nadie la usa.

**Arreglo:** mover el bloque a `caso_colegio_norte.json` (o a un `datos.py`) y que `app.py`
lo cargue. `construirCaso` ya está listo para recibirlo. Ganancia inmediata: el proyecto pasa
de "un caso" a "un motor con casos", que es lo que la sección 4 del cuaderno promete.

---

### M3 · `calcularRutas` muta su entrada

`logica.py:619-726`. Dos efectos:

1. Escribe en `caso['tabla']` el bus y la parada de cada estudiante (líneas 701–709). Llamar
   `calcularRutas` dos veces seguidas funciona solo porque el bucle previo resetea el valor a
   `None` antes de escribir. Es idempotente por disciplina, no por diseño.
2. El `plan` devuelto contiene `paradas`, `costo`, `padres`, `kmEntre`, `minEntre`, `puntos`
   y `arbol`, casi todos derivados del caso, y `buses` contiene referencias a `paradas`.

Consecuencia: no hay forma de saber, mirando una firma, qué se modifica. `recalcular()`
(`app.py:99`) descarta el plan anterior y recalcula todo, así que hoy no hay bug. Es deuda
latente: el día que alguien guarde dos planes para comparar, el segundo habrá pisado al
primero.

**Arreglo:** que `calcularRutas` no escriba en `caso` y devuelva la asignación como parte del
plan; y que `app.py` la proyecte a la tabla cuando la necesite.

---

### M4 · Una clase que hace tres trabajos

`app.py`: 696 líneas, ~34 métodos, una clase `App`. Construye widgets, mantiene estado
(`minuto`, `corriendo`, `estudiantes`, `cerradas`), simula el movimiento y dibuja el mapa. El
reloj vive en `tic()` (línea 533) y llama a tres métodos de refresco cada 40 ms.

No es un problema de estilo: es que **no se puede probar**. No hay manera de verificar
`posicionBus` con la ventana cerrada sin importar `app.py`, que importa `tkinter` y crea un
`Tk` al instanciar. (Nota: `posicionBus` y `nombreEsquina` son funciones puras en el nivel de
módulo — eso está bien hecho y es justo lo que hay que ampliar.)

**Arreglo mínimo, sin reescribir Tkinter:** extraer tres módulos por responsabilidad —
`vista_mapa.py` (dibujo), `panel.py` (pestañas) y `simulacion.py` (reloj + `posicionBus`) — y
dejar `App` como un coordinador de 100 líneas. No cambia la interfaz ni una píxel.

---

## 7. Correctitud: lo demostrado y lo asumido

Conviene tener esta separación clara porque es exactamente lo que un jurado técnico va a
intentar romper.

**Demostrado por el código o por las pruebas**

| Afirmación | Respaldo |
|---|---|
| Dijkstra calcula caminos mínimos | P3: comparación contra relajación completa |
| Con un bus, la ruta es óptima | P9: comparación contra todas las permutaciones |
| Ninguna ruta cuesta menos que el árbol mínimo | P4: `pesoArbol ≤ sum(rutas)`, e implica brecha ≤ 63 % sobre el óptimo |
| El reparto respeta cupos y no repite estudiantes | P1: `verificarPlan` recorre rutas y capacidades |
| Un cierre de calle se propaga a los caminos | P17: costo 38.68 → 40.58 y cero violaciones |
| Un estudiante incomunicado se detecta | P15/P16 con mensaje por nombre y esquina |
| Cambios ida y vuelta restauran el estado | P18: entra y sale, costo vuelve a 38.68 |
| La asignación de rutas a buses decide bien la factibilidad | Argumento de intercambio (sección 4.4) |

**Asumido, no demostrado**

| Suposición | Dónde vive | Qué la rompería |
|---|---|---|
| El costo es simétrico (`c(a,b) = c(b,a)`) | `construirCaso` inserta ambos sentidos | Vías de un solo sentido |
| La tarde es el espejo de la mañana | `logica.py:686` | Tráfico distinto a las 6:00 y a las 15:00 |
| Los kilómetros de una ruta son los del camino de menor costo | `logica.py:645` | Un objetivo que pondere km por encima de tiempo |
| El sentido elegido en la mañana sirve en la tarde | `calcularRutas` → `minutosABordo` | Ventanas de tiempo por estudiante |
| La rejilla de 8 pesos cubre el espacio útil | `logica.py:314` | Instancias donde otro peso daría un reparto válido |
| `capMax` es el tamaño objetivo correcto de ruta | `logica.py:627` | Flotas muy heterogéneas (p. ej. 20, 4, 4) |

Ninguna de estas suposiciones es un error: están todas declaradas en el cuaderno. El valor de
la tabla es que convierte "creo que está bien" en "sé exactamente qué estoy suponiendo".

---

## 8. Rendimiento y complejidad

**Medido:** 9 ms para el caso completo, incluyendo las 8 corridas de Clarke-Wright + 2-opt y
las 19 ejecuciones de Dijkstra. Para 20 estudiantes, el rendimiento no es un problema y no
hay nada que optimizar aquí.

**Contabilidad de la complejidad**, con las definiciones del proyecto (V=36 esquinas,
E=54 tramos, k=18 paradas):

| Etapa | Complejidad real | Comentario |
|---|---|---|
| Dijkstra × (k+1) | O(k·(V+E)·log E) | Sin *decrease-key*, la cola puede tener hasta E entradas; sigue siendo correcto |
| Matriz de costos | O(k²) consultas | El costo está precalculado por Dijkstra |
| `kmEntre`/`minEntre` | O(k² · longitud de camino) | **Trabajo redundante**: se recorre el camino para medir km después de haber calculado costos |
| Clarke-Wright | O(k² log k²) por peso, × 8 pesos | Los 8 pesos multiplican el costo por 8 |
| 2-opt | O(k²) por pasada, hasta converger | En la práctica converge en pocas pasadas |
| Kruskal | O(k² log k²) | Grafo completo entre 19 puntos: 171 aristas |

El único punto que vale la pena anotar es `kmEntre`: se ejecuta Dijkstra sobre el costo
ponderado, y después se reconstruye el camino y se suman los km de ese camino. Funciona y es
consistente, pero si algún día se necesita el camino de menor *distancia* (no de menor costo),
este código no lo da: hay que correr Dijkstra con los km como peso. Está en B6.

---

## 9. Seguridad y privacidad

**Seguridad técnica:** no hay hallazgos. Sin sockets, sin subprocess, sin `eval`/`exec` sobre
datos, sin SQL, sin deserialización, sin escritura de archivos, sin secretos en el código ni
en el historial. Las entradas del formulario se validan antes de tocar el motor y, en el peor
caso, producen un mensaje en rojo. La superficie es la de una calculadora de escritorio.

**Privacidad:** es el único riesgo real. `logica.py:297-305` contiene 20 nombres de
estudiantes asociados a una esquina y a un id. Hoy son ficticios; el día que esto se pruebe
con el listado real de un colegio pasa a ser un tratamiento de datos personales de menores y
aplica la Ley 1581 de 2012: autorización, finalidad, y nada de nombres reales en un repositorio
público ni en una demo grabada. Sugerencia concreta: dejar el dataset con ids y esquinas, y
generar los nombres en tiempo de ejecución (`Estudiante 1003`), que además es lo que la vista
de padres necesita mostrar.

---

## 10. Plan de mejora, en orden de retorno

| # | Acción | Esfuerzo | Impacto | Por qué primero |
|---|---|---|---|---|
| 1 | Cuaderno importa `logica.py` en vez de copiarlo | 20 min | Alto | Elimina la clase de bug más cara y no cambia nada visible |
| 2 | `import logica` explícito en `app.py` | 15 min | Medio | Contrato visible; un renombre rompe en el import |
| 3 | Mover el caso a JSON y cargarlo | 1 h | Alto | Convierte el proyecto en un motor con casos, que es lo que ya promete |
| 4 | `tests/` con `unittest`, 19 casos migrados | 3–4 h | Alto | Requisito para cualquier trabajo futuro; hoy no hay CI posible |
| 5 | Extraer `simulacion.py` (reloj + `posicionBus`) | 2 h | Medio | Hace testeable lo único que hoy no se puede probar |
| 6 | Type hints en las 12 funciones públicas del motor | 2 h | Bajo | Documentación ejecutable; habilita mypy |
| 7 | `calcularRutas` sin efectos sobre `caso` | 1 h | Medio | Permite comparar dos planes, que es el siguiente paso natural |
| 8 | Reintentar el reparto con tamaños de ruta distintos de `capMax` | 3 h | Medio | Cierra M5 sin cambiar el algoritmo |

Total: unas 13 horas para pasar de 8.0 a 9.0 sin tocar un solo algoritmo. El esfuerzo no está
en la parte difícil.

---

## 11. Cómo verifiqué todo esto

```bash
# 1. Ejecutar el motor y contrastar los números del pitch
cd 3_Ventana_de_escritorio/efiruta_escritorio
python3 -c "
from logica import *
n,c,t = construirMapa()
caso = construirCaso(n,c,t,COLEGIO,ESTUDIANTES,BUSES)
p = calcularRutas(caso)
print(len(n), len(t), p['totalKm'], p['totalMin'], p['totalCosto'], p['pesoArbol'])
"

# 2. Correr la suite del cuaderno (necesita la celda de la demo por casos_de_prueba)
python3 -c "
import json
d=json.load(open('1_Cuaderno_segunda_entrega/DDYA_S15_2026_2_Proyecto_Integrador_Momento2.ipynb'))
exec(compile('\n'.join(''.join(d['cells'][i]['source']) for i in (19,20,21,23,26)),'nb','exec'),{})
"

# 3. Verificar que la lógica está duplicada sin divergencias
#    → 58 defs en el cuaderno, 58 en logica.py, 0 funciones con cuerpo distinto

# 4. Reproducir la demo del pitch
#    Emilia en Cl122-Kr11 → 22.4 km
#    cerrar Cl116-Kr15 / Cl116-Kr11 → 23.1 km, 68.8 min
```

---

## 12. Resumen para llevar

- El motor es correcto y está respaldado por pruebas que atacan lo que puede fallar
  (Dijkstra contra su definición, un bus contra fuerza bruta, la cota contra el resultado).
- Los números publicados son exactos: 22.2 / 64.0 / 38.68 / 23.73 / 1.63 / 19 de 19.
- La deuda no es algorítmica sino estructural: lógica duplicada, pruebas no ejecutables fuera
  del notebook, datos del caso dentro del motor, vista y estado en la misma clase.
- Ninguna de esas cuatro cosas se nota en una demo y todas se notan en el segundo mes de uso.
- Seguridad: sin hallazgos técnicos. Privacidad: anonimizar antes de cualquier demo con datos
  reales.
