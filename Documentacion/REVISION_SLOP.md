# Revisión de slop y poda de comentarios — Cuadernos EfiRuta

Fecha: 2026-11-24 · Rama: `exp` · Alcance: los dos cuadernos del proyecto integrador.

| Cuaderno | Ruta |
|---|---|
| Momento 2 | `1_Cuaderno_segunda_entrega/DDYA_S15_2026_2_Proyecto_Integrador_Momento2.ipynb` |
| Entrega final | `2_Cuaderno_entrega_final/DDYA_S15_2026_2_Plantilla_Proyecto_Integrador_Colab.ipynb` |

## Veredicto

El código no tiene slop de IA: no se encontró código muerto, sobre-ingeniería,
defensas redundantes ni pruebas de relleno. El hallazgo real fue **densidad de
comentarios**: 84 líneas comentadas sobre 1374 de código (6,1 %), muchas de ellas
redundantes entre sí o con la sección 9 del cuaderno.

Se aplicó una poda conservadora: **11 líneas eliminadas y 8 reformuladas por
cuaderno**, sin tocar una sola línea de código. Quedan 73 comentarios sobre 1363
líneas (5,4 %).

## Qué se auditó

| Comprobación | Resultado |
|---|---|
| Estructura | 7 celdas de código, idénticas byte a byte entre los dos cuadernos |
| Comportamiento antes y después | `19 de 19 pruebas pasaron`, salida idéntica byte a byte |
| Lint (`ruff --select F,E9,W6`) | All checks passed |
| Código muerto | solo `Heap.peek`, que es superficie pública documentada de la clase |
| Calidad de las pruebas | referencias independientes (relajación de aristas, fuerza bruta, cota del MST); sin aserciones sobre prosa, sin *greps* al código fuente, sin inventarios copiados |
| Prosa markdown | sin patrones de slop (ES/EN); "eficiente" aparece solo en el enunciado de la asignatura |
| Metadatos | ids válidos, `execution_count` 1 a 7, sin widgets ni salidas huérfanas; las salidas guardadas coinciden con la ejecución actual |
| Marcadores | sin `TODO`/`FIXME`/`XXX`, sin atribución a IA |

## Poda aplicada

Todas las líneas eliminadas eran comentarios. El código de cada celda quedó
idéntico, verificado línea por línea.

| Celda | Líneas | Qué se quitó |
|---|---|---|
| 19 · estructuras | −7 | Cinco marcas de cambio en línea (`# Corregido:` ×4, `# Completado:` ×1): la sección 9 ya las enumera y son la fuente autorizada. Una nota que documentaba una ausencia (`# Se quitó el print de cada inserción`). Bloque de cabecera de `DisjointSets` de 3 líneas a 2. |
| 20 · datos | 0 | Solo retoques de redacción: banner compactado y "son aproximadas, solo para la simulación". |
| 21 · solución | −1 | Bloque de Clarke-Wright de 4 líneas a 3, con el mismo contenido. |
| 22 · gráficas | 0 | Banner compactado. |
| 23 · demo | −3 | Tres divisores decorativos dentro de `ejecutar_demo` (`Lectura…`, `Escritura…`, `Impresión…`): el orden ya se lee en 15 líneas de código. |
| 26 · pruebas | 0 | Banner compactado. |

Los banners `# ===================== X =====================` pasaron a `# X` en las
seis celdas. Se conserva la correspondencia uno a uno con el orden de celdas que
describe la sección 9.

## Conservado a propósito

| Ítem | Motivo |
|---|---|
| Complejidades (`O(log n)`, `O(alfa(n))`, `O(V^2)`) | La rúbrica pide justificar la eficiencia de cada estructura |
| `# config : True // Max_Heap` y demás contratos de tuplas | Son la única documentación de la firma: el cuaderno no usa docstrings |
| Bloque de invariantes de `Graph.dijkstra` | Explica por qué un vértice se cierra al salir del montón; no se deduce del código |
| Pasos numerados 1 a 5 en `calcularRutas` | Son el mapa del pseudocódigo de la sección 9 dentro de una función de 100 líneas |
| Grupos `# ---------- X ----------` en `ejecutar_pruebas` | Organizan 19 pruebas en cinco bloques; sostienen la lectura de un archivo largo |
| `# Figuras del caso principal (son las mismas de la sección 6)` | Justifica por qué se reconstruye el caso: el demo lo muta al agregar a 1021 y cerrar la Calle 116 |
| `# Referencia: se llenan los buses en el orden de inscripción` | Explica qué se está midiendo en la comparación base |
| Comentarios de dirección de bucle (`oriente-occidente`, `sur-norte`) | Evitan invertir las coordenadas al leer el mapa |

## Observaciones sin cambio

1. **Celda 21 con 424 líneas efectivas.** Supera la regla de 250, pero partirla
   rompe el orden de celdas documentado en la sección 9 y obliga a reasignar
   salidas. Se preserva.
2. **Pitch duplicado** en la celda 29 de la entrega final, en `GUION_PITCH.md` y en
   `README.md`. Es duplicación entre entregables, no slop interno.
3. **"Momento 3" sin marcar** en el control de entregas del cuaderno final. Es
   correcto al día de hoy: las sustentaciones son del 25 al 27 de noviembre.

## Cómo verificar

```bash
# salida funcional
python3 - <<'PY'
import json
nb = json.load(open("2_Cuaderno_entrega_final/DDYA_S15_2026_2_Plantilla_Proyecto_Integrador_Colab.ipynb"))
c = [x for x in nb["cells"] if x["cell_type"] == "code"]
open("/tmp/nb.py", "w").write("\n\n".join("".join(x["source"]) for x in c))
PY
MPLBACKEND=Agg python3 /tmp/nb.py | tail -1   # 19 de 19 pruebas pasaron

# lint
ruff check --isolated --select F,E9,W6 /tmp/nb.py
```

## Respaldo

Copia previa a cualquier cambio, verificada con `sha256sum` y `diff -q`:

```
_analisis/backup/pre-slop-review-20261124-191709/
  DDYA_S15_2026_2_Proyecto_Integrador_Momento2.ipynb        3272894c458037152c303fa420468957d1b933cf388787a45fd560e0793b94b9
  DDYA_S15_2026_2_Plantilla_Proyecto_Integrador_Colab.ipynb 251d7bd36fef3c0dce69d362332e9f41e04524ddfd65aed46197ba76a7d156f5
  SHA256SUMS.txt
```

Restaurar: `cp _analisis/backup/pre-slop-review-20261124-191709/*.ipynb <destino>`.
