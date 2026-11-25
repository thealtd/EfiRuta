# Prueba final — EfiRuta

**Commit verificado:** `911308d` (rama `exp`, árbol limpio).
**Entorno:** Linux, Python 3.14.10, matplotlib 3.11.2, Tk 8.6.
**Alcance:** los dos cuadernos, el motor `logica.py` y la ventana `app.py`.

---

## 1. Veredicto

Nada roto. Los dos cuadernos corren de punta a punta, pasan las 19 pruebas y su salida
impresa es byte a byte la que quedó guardada en el archivo. El motor del escritorio y el del
cuaderno, que son dos copias del mismo código, entregan las mismas cifras al centavo. La
ventana se construye y recalcula sin excepciones.

Al contrastar el código con lo que dice `EVALUACION_CODIGO.md` aparecieron **cinco cifras
desactualizadas en el documento, no en el código**; se corrigieron y se listan abajo.

---

## 2. Qué se ejecutó

| # | Prueba | Cómo | Resultado |
|---|---|---|---|
| 1 | Cuaderno Momento 2, completo | 7 celdas de código concatenadas y ejecutadas | exit 0 · **19 de 19 pruebas pasaron** · 10 295 B de salida |
| 2 | Cuaderno de entrega final, completo | igual, sobre el otro `.ipynb` | exit 0 · 19/19 · salida **idéntica** a la del Momento 2 |
| 3 | Salidas guardadas vs. ejecución fresca | comparación del `stdout` almacenado en las celdas contra el de la corrida | **idénticas** (mismo hash) |
| 4 | Integridad del cuaderno | `nbformat` 4.5 · 33 celdas (7 de código, 26 de texto) · ids únicos · `execution_count` 1..7 · 5 imágenes PNG decodificables | todo conforme |
| 5 | Motor del escritorio | `construirMapa` → `construirCaso` → `calcularRutas` | 22.2000 km · costo 38.6804 · árbol 23.73 |
| 6 | Cuaderno vs. escritorio | mismas cifras, mismo código | **iguales** en los cuatro valores |
| 7 | Ventana Tkinter | `App(tk.Tk())` + `recalcular()` sobre display oculto | se construye, recalcula, sin excepciones |
| 8 | Compilación | `py_compile` de `logica.py` y `app.py` | limpio |
| 9 | Lint | `ruff --select F,E9,W6` sobre el código de los cuadernos | limpio |
| 10 | Identidad de las dos copias | árbol sintáctico por función, celdas 19–21 vs `logica.py` | **63 de 63 nodos idénticos** (58 funciones + 5 clases) |

Los únicos mensajes en `stderr` son los cinco `FigureCanvasAgg is non-interactive` que emite
matplotlib al mostrar figuras sin pantalla. No aparecen en Colab ni en Jupyter.

---

## 3. Contraste documento ↔ código

| Dato publicado | Decía el documento | Dice el código hoy | Corrección |
|---|---|---|---|
| Líneas de la lógica en el cuaderno | 273 + 65 + 504 | 266 + 65 + 503 | actualizado |
| Commits en el historial | 6 | 7 | actualizado |
| Costo de calcular el caso | 9 ms | ~20 ms (mediana de 20 corridas: 16,7–28,3) | actualizado con el método de medición |
| Métodos de la clase `App` | ~34 | 40 en `App` + 3 funciones sueltas | actualizado |
| Identidad de las dos copias | 58/58 funciones, "mismos cuerpos" | 63/63 nodos: código idéntico, comentarios distintos desde la poda | precisado |

**Sobre el último punto.** El código de las dos copias sigue siendo el mismo — comparado por
árbol sintáctico, que ignora comentarios. Lo que cambió es el texto: los cuadernos perdieron
11 líneas de comentario y `logica.py` las conserva. Es inofensivo, pero es exactamente el
riesgo que el hallazgo A1 describe: dos fuentes de verdad que empiezan a separarse por lo
barato. Si se quiere volver a la igualdad literal, la poda de `REVISION_SLOP.md` se replica en
`logica.py` en cinco minutos.

**Sobre los 9 ms.** El algoritmo no cambió entre esa medición y hoy, así que la diferencia es
de máquina y de versión de Python. Con 20 estudiantes, 20 ms no es un problema; el número
quedó anotado con su margen para que nadie lo cite como si fuera una constante.

---

## 4. Lo que no se probó

- **Colab real.** No hay entorno Colab aquí. Se mitiga con lo observable: `nbformat` 4.5,
  sin widgets, y `matplotlib` como única dependencia externa, que Colab ya trae.
- **Trazo de las figuras.** Las 5 imágenes se generan y decodifican como PNG válidos; no se
  revisó a ojo que cada línea y etiqueta esté donde debe.
- **La ventana en Windows o macOS.** Solo se probó Tk en Linux.

---

## 5. Cómo reproducir

```bash
# cuaderno completo (sustituir A por B para el otro)
python3 - <<'PY'
import json
p = "1_Cuaderno_segunda_entrega/DDYA_S15_2026_2_Proyecto_Integrador_Momento2.ipynb"
nb = json.load(open(p, encoding="utf-8"))
open("/tmp/nb.py","w",encoding="utf-8").write(
    "\n\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"]=="code"))
PY
MPLBACKEND=Agg python3 /tmp/nb.py        # debe terminar en "19 de 19 pruebas pasaron"
ruff check --isolated --select F,E9,W6 /tmp/nb.py

# motor y ventana del escritorio
cd 3_Ventana_de_escritorio/efiruta_escritorio
python3 -c "import logica; n,c,t=logica.construirMapa(); \
caso=logica.construirCaso(n,c,t,logica.COLEGIO,logica.ESTUDIANTES,logica.BUSES); \
r=logica.calcularRutas(caso); print(r['totalKm'], r['totalCosto'], r['pesoArbol'])"
```

---

## 6. Cifras para el pitch, verificadas en esta corrida

| Dato | Valor |
|---|---|
| Recorrido optimizado | 22.2 km · 64 min (23 + 17 + 24 por bus) · costo 38.68 |
| Cota inferior (árbol de expansión mínimo) | 23.73 |
| Brecha frente a la cota | 1.63× |
| Ruta sin optimizar | 70.3 km · 155 min · costo 120.86 |
| Ahorro | 68 % en distancia · 59 % en tiempo |
| Ocupación | 8/8 · 5/7 · 7/7 |
| Estudiante nuevo (1021) | 22.2 → 22.4 km |
| Calle 116 cerrada | 22.4 → 23.1 km · 65 → 69 min |
| Fuerza bruta (un solo bus, 5040 rutas) | 22.5449, igual que el programa |
| Mapa | 36 esquinas · 54 tramos · 20 estudiantes · 3 buses |
