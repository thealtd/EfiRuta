# Algoritmos de EfiRuta — versión de 5 minutos

Resumen hablado de `ALGORITMOS.md`, para una exposición de cinco minutos. Está escrito
para leerse en voz alta: cada bloque trae su minutaje, una frase de entrada y los
números que hay que decir sin dudar. Si el tiempo se acorta, la última sección dice qué
quitar sin romper el argumento.

Regla de oro: no leer el documento largo. Los cinco minutos alcanzan para tres ideas
(qué se decide, con qué, cuánto mejora) y un solo número por algoritmo.

---

## 0:00 – 0:25 · Qué problema resuelve

"Veinte estudiantes, dieciocho paradas, tres buses de ocho, siete y siete puestos. Hay
que decidir qué bus lleva cada parada y en qué orden las visita. Ese es el problema de
ruteo de vehículos con capacidad, y es NP-difícil: probar todos los repartos no termina
nunca. Así que no buscamos la ruta perfecta: buscamos una buena y un número que diga qué
tan buena es."

## 0:25 – 1:05 · Dijkstra

"El bus anda por calles, no en línea recta. El mapa es un grafo de treinta y seis
esquinas y cincuenta y cuatro tramos, y cada tramo pesa ochenta por ciento distancia y
veinte por ciento tiempo. Para saber por dónde ir corremos Dijkstra con montón mínimo
desde el colegio y desde cada parada: diecinueve veces, y quedan las distancias entre
los diecinueve puntos que importan.

De la Calle 116 a la 122 hay quinientos metros por dos rutas, pero la Autopista
cuesta menos porque va al doble de velocidad. Y si cierran una calle, se quita la arista
y el siguiente Dijkstra trae otro camino."

## 1:05 – 1:55 · Clarke-Wright

"Con las distancias listas hay que repartir las paradas entre los tres buses. Eso lo
hace el método de ahorros de Clarke y Wright: al principio cada parada es su propia
ruta, y unir dos rutas ahorra lo que cuesta ir del colegio a cada una menos lo que
cuesta ir de una a la otra. Los ahorros salen de mayor a menor de un montón máximo, y
los conjuntos disjuntos dicen si dos paradas ya están en la misma ruta.

La unión solo se acepta si las paradas están en un extremo y si la carga cabe en el
bus: aquí se descartan trece uniones por capacidad. Y como no hay un peso de ahorro
correcto de antemano, se prueban ocho y gana el reparto más barato. Aquí, 1.8."

## 1:55 – 3:05 · 2-opt, el que agregamos por fuera

"Clarke-Wright une paradas por ahorro, no por geografía. La ruta pasa cerca de todo,
pero muchas veces cruza sobre sí misma: sube, vuelve y sube otra vez. El ahorro no mira
el mapa, mira la cuenta.

Para eso está 2-opt, que no viene del temario: es del problema del viajante, de un
artículo de Croes de 1958. Prueba invertir un tramo de la ruta; si queda más barata se la
queda, y repite hasta que ninguna inversión mejore. No cambia el reparto entre buses,
solo el orden.

Y se mide, no es opinión. Apagando la mejora en la misma corrida, las rutas pasan de
veintidós punto veinte a veintitrés punto diez kilómetros, y el costo sube de treinta y
ocho punto sesenta y ocho a cuarenta punto cero nueve. Son novecientos metros y dos
inversiones, por un cuarto de milisegundo.

Su límite: llega a un óptimo local. Por eso hay una prueba con un solo bus, donde se
prueban las cinco mil cuarenta permutaciones: el programa da la misma ruta que la mejor."

## 3:05 – 3:40 · Kruskal

"Queda la pregunta incómoda: qué tan buena es la ruta si no conocemos el óptimo. Kruskal
calcula el árbol de expansión mínimo, la forma más barata de conectar el colegio con
todas las paradas, con montón mínimo y conjuntos disjuntos para no formar ciclos. Pesa
veintitrés punto setenta y tres; las rutas cuestan treinta y ocho punto sesenta y ocho.
Ninguna ruta puede costar menos que el árbol, así que estamos a una vez sesenta y tres
o menos de la mejor posible."

## 3:40 – 4:10 · Lo demás

"Los buses se asignan con dos montones máximos: la ruta más llena al bus más grande, y
si no cabe se avisa en vez de repartir de más. Una pila reconstruye el camino de
Dijkstra y una cola simula el bus para los padres: a qué distancia va y cuánto falta.
Todo tarda veinte milisegundos, y por eso al cerrar una calle la ruta nueva aparece sin
espera."

## 4:10 – 5:00 · Resultados

"Contra lo que el colegio hace a mano, recoger en orden de inscripción: setenta punto
tres kilómetros y ciento cincuenta y cinco minutos. Con EfiRuta: veintidós punto dos y
sesenta y tres punto nueve. Sesenta y ocho por ciento menos distancia, cincuenta y
nueve por ciento menos tiempo, y diecinueve pruebas que pasan.

En resumen: Dijkstra decide por dónde, Clarke-Wright con quién, 2-opt ordena y Kruskal
dice qué tan lejos estamos del óptimo. Cada uno tiene su prueba, y el registro muestra
línea por línea por qué se unió o se invirtió cada tramo."

---

## Los números, de memoria

| Dato | Valor |
|---|---|
| Estudiantes / paradas / buses | 20 / 18 / 3 (8, 7 y 7 puestos) |
| Esquinas y tramos del mapa | 36 y 54 |
| Ponderación del costo | 0.8 distancia + 0.2 tiempo |
| Dijkstra | 19 orígenes, 361 pares |
| Peso de ahorro ganador | 1.8, de 8 probados |
| Uniones descartadas por cupo | 13 |
| Con 2-opt | 22.20 km, costo 38.68, 63.9 min |
| Sin 2-opt | 23.10 km, costo 40.09, 64.8 min |
| Árbol mínimo (Kruskal) | 23.73 |
| Razón rutas / árbol | 1.63 |
| Orden de inscripción | 70.3 km, 155 min |
| Mejora | 68 % menos km, 59 % menos tiempo |
| Tiempo de cálculo | ~20 ms (mediana 19.6) |
| Pruebas | 19 de 19 |

## Si preguntan

**"¿Es óptima?"** No se sabe y no se afirma. Está a 1.63 del árbol mínimo o menos, y en
el caso de un solo bus coincide con la fuerza bruta.

**"¿Por qué no usaron una librería?"** Porque el curso pide implementar las estructuras
y porque con 36 esquinas el cálculo entero son 20 ms; una librería habría escondido
justo lo que hay que explicar.

**"¿Por qué 0.8 y 0.2?"** Porque el colegio paga kilómetros y los padres sufren minutos;
están en dos constantes al inicio del archivo y cambiarlas cambia las rutas.

## Si el tiempo se acorta

Para tres minutos: mantener el problema (25 s), Clarke-Wright (50 s) y 2-opt (70 s), y
cerrar con resultados (50 s). Dijkstra cabe en una frase: "los caminos salen de Dijkstra
con montón mínimo". Kruskal se reduce a "el árbol pesa 23.73 y las rutas 38.68, estamos
a 1.63", que es el único dato necesario.

Para demostrarlo en vivo en lugar de explicar 2-opt:

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

Imprime `22.20` y `23.10`. Con eso se explica solo y ahorra un minuto de discurso.
