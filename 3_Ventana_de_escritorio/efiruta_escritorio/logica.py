# EfiRuta - lógica del MVP (el mismo código de las celdas del cuaderno): estructuras, datos del caso y solución

# ===================== ESTRUCTURAS DE DATOS (código base de clase, adaptado) =====================
import math

WHITE = "white"
BLACK = "black"
GRAY = "gray"


class Heap:
    # config : True // Max_Heap
    # config : False // Min_heap
    def __init__(self, data=[], config=True):
        self.data = []
        self.config = config
        self.build(data[:])

    def left(self, index):
        return 2 * index + 1

    def right(self, index):
        return 2 * (index + 1)

    def parent(self, index):
        return (index - 1) // 2

    def __len__(self):
        return len(self.data)

    def goesAbove(self, child, parent):
        # Dice si el hijo debe quedar por encima del padre según el tipo de montón
        if self.config:
            return self.data[parent] < self.data[child]
        return self.data[child] < self.data[parent]

    def insert(self, new):
        # Corregido: el elemento nuevo entra al final y sube hasta su lugar. O(log n)
        self.data.append(new)
        index = len(self.data) - 1
        while index > 0 and self.goesAbove(index, self.parent(index)):
            parent_index = self.parent(index)
            self.data[parent_index], self.data[index] = self.data[index], self.data[parent_index]
            index = parent_index

    def extract(self):
        # Corregido: saca la raíz pasando el último elemento arriba y bajándolo. O(log n)
        if len(self) == 0:
            raise Exception("El montón está vacio")
        top = self.data[0]
        last = self.data.pop()
        if len(self) > 0:
            self.data[0] = last
            self.heapify(0)
        return top

    def build(self, data=[]):
        if data and len(data) > 0 and isinstance(data, list):
            self.data = data
        for index in range(len(self) // 2, -1, -1):
            self.heapify(index)

    def heapify(self, index):
        if self.config:
            self.max_heapify(index)
        else:
            self.min_heapify(index)

    def max_heapify(self, index):
        left_index, right_index, largest_index = self.left(index), self.right(index), index
        if left_index < len(self) and self.data[largest_index] < self.data[left_index]:
            largest_index = left_index
        if right_index < len(self) and self.data[largest_index] < self.data[right_index]:
            largest_index = right_index
        if largest_index != index:
            self.data[largest_index], self.data[index] = self.data[index], self.data[largest_index]
            self.max_heapify(largest_index)

    def min_heapify(self, index):
        # Completado: igual que max_heapify, pero deja arriba al menor
        left_index, right_index, smallest_index = self.left(index), self.right(index), index
        if left_index < len(self) and self.data[left_index] < self.data[smallest_index]:
            smallest_index = left_index
        if right_index < len(self) and self.data[right_index] < self.data[smallest_index]:
            smallest_index = right_index
        if smallest_index != index:
            self.data[smallest_index], self.data[index] = self.data[index], self.data[smallest_index]
            self.min_heapify(smallest_index)

    def peek(self):
        return self.data[0]


class PriorityQueue:
    def __init__(self, data=[], config=True):
        self.data = Heap(data, config)

    def __len__(self):
        return len(self.data)

    def enqueue(self, new):
        self.data.insert(new)

    def dequeue(self):
        if len(self) == 0:
            raise Exception("Underflow")
        return self.data.extract()


class HashTable:
    def __init__(self, size):
        self.elements = [ [] for x in range(size)]

    def hash(self, key):
        return hash(key) % len(self.elements)

    def insert(self, key, value):
        # Se quitó el print de cada inserción para no llenar la salida
        index = self.hash(key)
        self.elements[index].append((key, value))

    def search(self, key):
        index = self.hash(key)
        for e in self.elements[index]:
            if e[0] == key:
                return e[1]
        return None

    def update(self, key, value2):
        # Corregido: se reemplaza la tupla completa (las tuplas no se pueden modificar)
        index = self.hash(key)
        for pos in range(len(self.elements[index])):
            if self.elements[index][pos][0] == key:
                self.elements[index][pos] = (key, value2)

    def delete(self, key):
        # Corregido: se elimina el par (clave, valor) completo
        index = self.hash(key)
        for e in self.elements[index]:
            if e[0] == key:
                self.elements[index].remove(e)
                return


class DisjointSets:
    # Conjuntos disjuntos con Union-Find. Cada elemento guarda su padre y su rango.
    # La unión por rango cuelga el árbol más bajo del más alto y la compresión de caminos
    # aplana el árbol en cada findSet, así que las dos operaciones son O(alfa(n)) amortizado
    def __init__(self, A):
        self.padre = {}
        self.rango = {}
        for x in A:
            self.padre[x] = x
            self.rango[x] = 0

    def findSet(self, x):
        # Devuelve la raíz del conjunto de x, comprimiendo el camino a la raíz
        if x not in self.padre:
            return None
        raiz = x
        while self.padre[raiz] != raiz:
            raiz = self.padre[raiz]
        while self.padre[x] != raiz:
            siguiente = self.padre[x]
            self.padre[x] = raiz
            x = siguiente
        return raiz

    def makeSet(self, x):
        if x not in self.padre:
            self.padre[x] = x
            self.rango[x] = 0
        return self.findSet(x)

    def cuentaConjuntos(self):
        # Cuenta cuántas raíces distintas quedan: una por cada conjunto o zona conectada
        raices = set()
        for x in self.padre:
            raices.add(self.findSet(x))
        return len(raices)

    def union(self, x, y):
        # Une los conjuntos de x y de y por rango. Devuelve False si ya estaban juntos
        raizX = self.findSet(x)
        raizY = self.findSet(y)
        if raizX is None:
            raizX = self.makeSet(x)
        if raizY is None:
            raizY = self.makeSet(y)
        if raizX == raizY:
            return False
        if self.rango[raizX] < self.rango[raizY]:
            raizX, raizY = raizY, raizX
        self.padre[raizY] = raizX
        if self.rango[raizX] == self.rango[raizY]:
            self.rango[raizX] = self.rango[raizX] + 1
        return True


class Graph:
    # Cada relación es (u, v, peso). En este proyecto el peso es el costo ponderado de la calle
    def _buildRelation(self, e):
        if self.directed:
            self.relations = e
        else:
            self.relations = set()
            for el in e:
                self.relations.add(el)
                self.relations.add((el[1], el[0], el[2]))

    def _buildAdjList(self):
        self.adjList = {}
        for v in self.vertexes:
            self.adjList[v] = []
        for relation in self.relations:
            self.adjList[relation[0]].append(relation[1])

    def _buildWeights(self):
        self.weights = {}
        for relation in self.relations:
            self.weights[(relation[0], relation[1])] = relation[2]

    def __init__(self, v, e, directed = True):
        self.directed = directed
        self.vertexes = v
        self._buildRelation(e)
        self._buildAdjList()
        self._buildWeights()

    def getNeighbors(self, vertex):
        return self.adjList[vertex]

    def removeEdge(self, u, v):
        # Quita la calle u-v (y v-u si no es dirigido) y reconstruye la lista de adyacencia
        newRelations = set()
        found = False
        for relation in self.relations:
            if relation[0] == u and relation[1] == v:
                found = True
            elif relation[0] == v and relation[1] == u and not self.directed:
                found = True
            else:
                newRelations.add(relation)
        self.relations = newRelations
        self._buildAdjList()
        self._buildWeights()
        return found

    def _buildVProps(self, source = None):
        self.v_props = {}
        for v in self.vertexes:
            self.v_props[v] = {'color': WHITE, 'distance': math.inf, 'parent': None}
        if source is not None:
            self.v_props[source] = {'color': GRAY, 'distance': 0, 'parent': None}

    def dijkstra(self, source):
        # Caminos mínimos desde source con cola de prioridad (montón mínimo).
        # En la cola van pares (costo, vértice). Un vértice se cierra (BLACK) la primera vez que sale,
        # y en ese momento su costo ya es el mínimo. self.order guarda el orden en que se cierran
        self._buildVProps(source)
        self.order = []
        pq = PriorityQueue([], False)
        pq.enqueue((0, source))
        while len(pq) > 0:
            d, u = pq.dequeue()
            if self.v_props[u]['color'] != BLACK:
                self.v_props[u]['color'] = BLACK
                self.order.append(u)
                for neighbor in self.getNeighbors(u):
                    newDistance = d + self.weights[(u, neighbor)]
                    if newDistance < self.v_props[neighbor]['distance']:
                        self.v_props[neighbor]['distance'] = newDistance
                        self.v_props[neighbor]['parent'] = u
                        pq.enqueue((newDistance, neighbor))
        return self.v_props


# ===================== DATOS DEL CASO: zona norte de Bogotá =====================
# Mapa simplificado: los nombres de las vías son reales; las distancias (km) y las
# velocidades (km/h) son aproximadas y se usan solo para la simulación.

# (código, nombre, posición en km, velocidad en km/h)
CARRERAS = [('Auto', 'Autopista Norte', 0.0, 40), ('Kr19', 'Carrera 19', 0.9, 20),
            ('Kr15', 'Carrera 15', 1.4, 30), ('Kr11', 'Carrera 11', 1.9, 20),
            ('Kr9', 'Carrera 9', 2.25, 30), ('Kr7', 'Carrera 7', 2.6, 30)]
CALLES = [('Cl100', 'Calle 100', 0.0, 30), ('Cl106', 'Calle 106', 0.6, 20),
          ('Cl116', 'Calle 116', 1.5, 30), ('Cl122', 'Calle 122', 2.0, 20),
          ('Cl127', 'Calle 127', 2.5, 30), ('Cl134', 'Calle 134', 3.2, 30)]

# Tramos que no existen en el mapa (no hay paso entre esas dos esquinas)
SIN_PASO = [('Cl106-Kr19', 'Cl106-Auto'), ('Cl122-Kr19', 'Cl122-Auto'), ('Cl122-Kr9', 'Cl122-Kr7'),
            ('Cl127-Kr11', 'Cl134-Kr11'), ('Cl100-Kr19', 'Cl106-Kr19'), ('Cl127-Kr19', 'Cl134-Kr19')]

COLEGIO = 'Cl116-Kr11'

# (id, nombre, esquina donde vive)
ESTUDIANTES = [('1001', 'Ana', 'Cl134-Kr7'), ('1002', 'Luis', 'Cl100-Auto'), ('1003', 'Sofia', 'Cl127-Kr15'),
               ('1004', 'Mateo', 'Cl106-Kr7'), ('1005', 'Valentina', 'Cl134-Kr15'), ('1006', 'Samuel', 'Cl134-Kr7'),
               ('1007', 'Isabella', 'Cl100-Kr15'), ('1008', 'Martin', 'Cl122-Kr19'), ('1009', 'Camila', 'Cl127-Kr7'),
               ('1010', 'Tomas', 'Cl116-Auto'), ('1011', 'Lucia', 'Cl100-Kr9'), ('1012', 'Andres', 'Cl134-Auto'),
               ('1013', 'Mariana', 'Cl106-Kr15'), ('1014', 'Juan', 'Cl127-Kr9'), ('1015', 'Daniela', 'Cl100-Kr15'),
               ('1016', 'Felipe', 'Cl122-Kr7'), ('1017', 'Sara', 'Cl127-Auto'), ('1018', 'Nicolas', 'Cl106-Kr11'),
               ('1019', 'Gabriela', 'Cl134-Kr9'), ('1020', 'David', 'Cl116-Kr19')]

# Puestos de cada bus (la cantidad de buses es la cantidad de números)
BUSES = [8, 7, 7]

PESO_DISTANCIA = 0.8
PESO_TIEMPO = 0.2
MINUTOS_POR_PARADA = 1          # tiempo que el bus se detiene en cada parada
SALIDA_MANANA = 6 * 60          # 6:00 a. m. en minutos desde la medianoche
SALIDA_TARDE = 15 * 60          # 3:00 p. m.
TAMANO_TABLA = 101
PESOS_AHORRO = [1.0, 0.6, 0.8, 1.2, 1.4, 1.6, 1.8, 2.0]


def construirMapa():
    # Arma las esquinas y los tramos de calle a partir de las listas de calles y carreras.
    # Devuelve: nodos, coords (esquina -> (x, y)) y tramos (u, v, km, velocidad)
    nodos = []
    coords = {}
    for calle in CALLES:
        for carrera in CARRERAS:
            nodo = calle[0] + '-' + carrera[0]
            nodos.append(nodo)
            coords[nodo] = (carrera[2], calle[2])
    tramos = []
    for calle in CALLES:                       # tramos sobre cada calle (oriente-occidente)
        for c in range(len(CARRERAS) - 1):
            u = calle[0] + '-' + CARRERAS[c][0]
            v = calle[0] + '-' + CARRERAS[c + 1][0]
            km = round(CARRERAS[c + 1][2] - CARRERAS[c][2], 2)
            if (u, v) not in SIN_PASO and (v, u) not in SIN_PASO:
                tramos.append((u, v, km, calle[3]))
    for carrera in CARRERAS:                   # tramos sobre cada carrera (sur-norte)
        for c in range(len(CALLES) - 1):
            u = CALLES[c][0] + '-' + carrera[0]
            v = CALLES[c + 1][0] + '-' + carrera[0]
            km = round(CALLES[c + 1][2] - CALLES[c][2], 2)
            if (u, v) not in SIN_PASO and (v, u) not in SIN_PASO:
                tramos.append((u, v, km, carrera[3]))
    return nodos, coords, tramos


# ===================== SOLUCIÓN DEL PROBLEMA =====================

def construirCaso(nodos, coords, tramos, colegio, estudiantes, capacidades):
    # Escribe los datos en las estructuras: grafo (calles), diccionarios (km y minutos) y tabla hash (estudiantes).
    # Ponderación: costo = 0.8 * (km / km promedio) + 0.2 * (minutos / minutos promedio)
    km = {}
    minutos = {}
    sumaKm = 0
    sumaMin = 0
    for tramo in tramos:
        if tramo[0] not in nodos or tramo[1] not in nodos:
            raise Exception('La calle ' + str(tramo[0]) + ' - ' + str(tramo[1]) + ' usa una esquina que no existe')
        tiempo = tramo[2] / tramo[3] * 60
        km[(tramo[0], tramo[1])] = tramo[2]
        km[(tramo[1], tramo[0])] = tramo[2]
        minutos[(tramo[0], tramo[1])] = tiempo
        minutos[(tramo[1], tramo[0])] = tiempo
        sumaKm = sumaKm + tramo[2]
        sumaMin = sumaMin + tiempo
    kmProm = sumaKm / len(tramos)
    minProm = sumaMin / len(tramos)
    relaciones = []
    for tramo in tramos:
        costo = PESO_DISTANCIA * tramo[2] / kmProm + PESO_TIEMPO * minutos[(tramo[0], tramo[1])] / minProm
        relaciones.append((tramo[0], tramo[1], costo))
    tabla = HashTable(TAMANO_TABLA)
    ids = []
    for est in estudiantes:
        if tabla.search(est[0]) is None:
            tabla.insert(est[0], {'nombre': est[1], 'nodo': est[2], 'bus': None, 'orden': None})
            ids.append(est[0])
    return {'grafo': Graph(nodos, relaciones, False), 'coords': coords, 'km': km, 'minutos': minutos,
            'kmProm': kmProm, 'minProm': minProm, 'colegio': colegio, 'tabla': tabla, 'ids': ids,
            'capacidades': list(capacidades)}


def validarDatos(caso):
    # Conjuntos disjuntos: se une cada calle y queda un conjunto por cada zona conectada.
    # Un estudiante es alcanzable si su esquina está en el mismo conjunto que el colegio
    grafo, colegio, tabla = caso['grafo'], caso['colegio'], caso['tabla']
    errores = []
    if colegio not in grafo.vertexes:
        errores.append('El colegio (' + str(colegio) + ') no es una esquina del mapa')
        return errores
    dj = DisjointSets(grafo.vertexes)
    for relation in grafo.relations:
        dj.union(relation[0], relation[1])
    conjuntoColegio = dj.findSet(colegio)
    for idEst in caso['ids']:
        est = tabla.search(idEst)
        if est['nodo'] not in grafo.vertexes:
            errores.append('El estudiante ' + idEst + ' (' + est['nombre'] + ') vive en ' + est['nodo'] + ', que no existe en el mapa')
        elif dj.findSet(est['nodo']) != conjuntoColegio:
            errores.append('El estudiante ' + idEst + ' (' + est['nombre'] + ') vive en ' + est['nodo'] + ', que no tiene camino al colegio')
    if len(caso['capacidades']) == 0:
        errores.append('No hay buses')
    for cupo in caso['capacidades']:
        if cupo <= 0:
            errores.append('Hay un bus con ' + str(cupo) + ' puestos')
    if len(caso['ids']) > sum(caso['capacidades']):
        errores.append('Hay ' + str(len(caso['ids'])) + ' estudiantes y solo ' + str(sum(caso['capacidades'])) + ' puestos en total')
    return errores


def agruparParadas(caso):
    # Los estudiantes que viven en la misma esquina (por ejemplo hermanos) comparten parada
    paradas = {}
    nodos = []
    for idEst in caso['ids']:
        nodo = caso['tabla'].search(idEst)['nodo']
        if nodo not in paradas:
            paradas[nodo] = []
            nodos.append(nodo)
        paradas[nodo].append(idEst)
    return paradas, nodos


def calcularCostos(grafo, origenes):
    # Un Dijkstra por cada origen. costo[(a, b)] = costo mínimo de a a b; padres[a] = árbol de caminos desde a
    costo = {}
    padres = {}
    for origen in origenes:
        props = grafo.dijkstra(origen)
        padres[origen] = {}
        for v in grafo.vertexes:
            costo[(origen, v)] = props[v]['distance']
            padres[origen][v] = props[v]['parent']
    return costo, padres


def caminoCalles(padres, origen, destino):
    # Pila: se sube desde el destino por los padres de Dijkstra y al sacar queda en orden origen -> destino
    pila = []
    actual = destino
    while actual is not None:
        pila.append(actual)
        actual = padres[origen][actual]
    camino = []
    while len(pila) > 0:
        camino.append(pila.pop())
    return camino


def medirCamino(camino, km, minutos):
    totalKm = 0
    totalMin = 0
    for p in range(len(camino) - 1):
        totalKm = totalKm + km[(camino[p], camino[p + 1])]
        totalMin = totalMin + minutos[(camino[p], camino[p + 1])]
    return totalKm, totalMin


def cargaRuta(ruta, paradas):
    carga = 0
    for nodo in ruta:
        carga = carga + len(paradas[nodo])
    return carga


def costoRuta(orden, colegio, costo):
    if len(orden) == 0:
        return 0
    puntos = [colegio] + orden + [colegio]
    total = 0
    for p in range(len(puntos) - 1):
        total = total + costo[(puntos[p], puntos[p + 1])]
    return total


def ahorrosClarkeWright(colegio, nodos, paradas, costo, capMax, peso, registro):
    # Al inicio cada parada es su propia ruta: colegio -> parada -> colegio.
    # Unir las rutas de i y j ahorra: c(colegio, i) + c(colegio, j) - peso * c(i, j)
    # Los ahorros salen de un montón máximo (primero el mayor) y los conjuntos disjuntos
    # dicen si i y j ya están en la misma ruta
    dj = DisjointSets(nodos)
    rutaDe = {}
    for nodo in nodos:
        rutaDe[nodo] = [nodo]
    ahorros = PriorityQueue([], True)
    for a in range(len(nodos)):
        for b in range(a + 1, len(nodos)):
            i, j = nodos[a], nodos[b]
            ahorro = costo[(colegio, i)] + costo[(colegio, j)] - peso * costo[(i, j)]
            ahorros.enqueue((ahorro, i, j))
    descartadas = 0
    while len(ahorros) > 0:
        ahorro, i, j = ahorros.dequeue()
        if dj.findSet(i) != dj.findSet(j):
            rutaI, rutaJ = rutaDe[i], rutaDe[j]
            # Solo se pueden pegar dos rutas por sus extremos
            extremoI = rutaI[0] == i or rutaI[len(rutaI) - 1] == i
            extremoJ = rutaJ[0] == j or rutaJ[len(rutaJ) - 1] == j
            carga = cargaRuta(rutaI, paradas) + cargaRuta(rutaJ, paradas)
            if extremoI and extremoJ and carga <= capMax:
                # Se voltean para que quede ... i -> j ...
                if rutaI[0] == i:
                    rutaI.reverse()
                if rutaJ[len(rutaJ) - 1] == j:
                    rutaJ.reverse()
                nueva = rutaI + rutaJ
                for nodo in nueva:
                    rutaDe[nodo] = nueva
                dj.union(i, j)
                registro.append('Clarke-Wright: se unen las rutas por ' + i + ' y ' + j + ' (ahorro ' + str(round(ahorro, 2)) + ', quedan ' + str(carga) + ' estudiantes)')
            elif extremoI and extremoJ:
                descartadas = descartadas + 1
    registro.append('Clarke-Wright: ' + str(descartadas) + ' uniones descartadas porque el bus pasaría de ' + str(capMax) + ' puestos')
    # Cada ruta se toma una sola vez: desde su primera parada
    rutas = []
    for nodo in nodos:
        if rutaDe[nodo][0] == nodo:
            rutas.append(rutaDe[nodo])
    return rutas


def mejorar2opt(orden, colegio, costo, registro):
    # 2-opt: si invertir un tramo de la ruta la hace más barata, se invierte.
    # Se repite hasta que ninguna inversión mejore
    ruta = [colegio] + orden + [colegio]
    mejoro = True
    while mejoro:
        mejoro = False
        for a in range(1, len(ruta) - 2):
            for b in range(a + 1, len(ruta) - 1):
                antes = costo[(ruta[a - 1], ruta[a])] + costo[(ruta[b], ruta[b + 1])]
                despues = costo[(ruta[a - 1], ruta[b])] + costo[(ruta[a], ruta[b + 1])]
                if despues < antes - 0.000001:
                    registro.append('2-opt: se invierte el tramo ' + ruta[a] + ' ... ' + ruta[b] + ' (ahorra ' + str(round(antes - despues, 2)) + ')')
                    tramo = ruta[a:b + 1]
                    tramo.reverse()
                    ruta = ruta[:a] + tramo + ruta[b + 1:]
                    mejoro = True
    return ruta[1:len(ruta) - 1]


def asignarBuses(rutas, paradas, capacidades):
    # La ruta con más estudiantes va al bus con más puestos, y así sucesivamente (dos montones máximos)
    if len(rutas) > len(capacidades):
        return None
    pqRutas = PriorityQueue([], True)
    for r in range(len(rutas)):
        pqRutas.enqueue((cargaRuta(rutas[r], paradas), r))
    pqBuses = PriorityQueue([], True)
    for b in range(len(capacidades)):
        pqBuses.enqueue((capacidades[b], b))
    asignacion = [[] for b in range(len(capacidades))]
    while len(pqRutas) > 0:
        carga, r = pqRutas.dequeue()
        cupo, b = pqBuses.dequeue()
        if carga > cupo:
            return None
        asignacion[b] = rutas[r]
    return asignacion


def kruskal(puntos, costo):
    # Árbol de expansión mínimo sobre el colegio y las paradas (la arista a-b pesa el costo mínimo entre a y b).
    # Las aristas salen de menor a mayor de un montón mínimo; se acepta la que une dos conjuntos distintos
    pq = PriorityQueue([], False)
    for a in range(len(puntos)):
        for b in range(a + 1, len(puntos)):
            pq.enqueue((costo[(puntos[a], puntos[b])], puntos[a], puntos[b]))
    dj = DisjointSets(puntos)
    aristas = []
    traza = []
    peso = 0
    while len(pq) > 0 and len(aristas) < len(puntos) - 1:
        c, a, b = pq.dequeue()
        if dj.findSet(a) != dj.findSet(b):
            dj.union(a, b)
            aristas.append((a, b, c))
            peso = peso + c
            traza.append((a, b, c, True))
        else:
            traza.append((a, b, c, False))
    return aristas, peso, traza


def minutosABordo(orden, colegio, paradas, minEntre):
    # Suma de los minutos que cada estudiante pasa en el bus en la mañana (desde que sube hasta el colegio)
    total = 0
    alColegio = 0
    siguiente = colegio
    for i in range(len(orden) - 1, -1, -1):
        alColegio = alColegio + minEntre[(orden[i], siguiente)]
        total = total + alColegio * len(paradas[orden[i]])
        alColegio = alColegio + MINUTOS_POR_PARADA
        siguiente = orden[i]
    return total


def construirHorario(orden, colegio, padres, km, minutos, paradas):
    # Lista de puntos por donde pasa el bus, con km y minutos acumulados desde la salida.
    # En las paradas se guarda quiénes suben (mañana) o bajan (tarde)
    horario = [{'nodo': colegio, 'km': 0, 'min': 0, 'estudiantes': []}]
    if len(orden) == 0:
        return horario
    puntos = [colegio] + orden + [colegio]
    kmAcum = 0
    minAcum = 0
    for p in range(len(puntos) - 1):
        tramo = caminoCalles(padres, puntos[p], puntos[p + 1])
        for k in range(1, len(tramo)):
            kmAcum = kmAcum + km[(tramo[k - 1], tramo[k])]
            minAcum = minAcum + minutos[(tramo[k - 1], tramo[k])]
            horario.append({'nodo': tramo[k], 'km': kmAcum, 'min': minAcum, 'estudiantes': []})
        if len(tramo) == 1:
            horario.append({'nodo': puntos[p + 1], 'km': kmAcum, 'min': minAcum, 'estudiantes': []})
        if p + 1 < len(puntos) - 1:
            horario[len(horario) - 1]['estudiantes'] = paradas[puntos[p + 1]]
            minAcum = minAcum + MINUTOS_POR_PARADA
    return horario


def calcularRutas(caso):
    grafo, colegio, tabla, ids, capacidades = caso['grafo'], caso['colegio'], caso['tabla'], caso['ids'], caso['capacidades']
    plan = {'errores': validarDatos(caso)}
    if len(ids) == 0:
        plan['errores'].append('No hay estudiantes inscritos')
    if len(plan['errores']) > 0:
        return plan
    paradas, nodos = agruparParadas(caso)
    capMax = max(capacidades)
    for nodo in nodos:
        if len(paradas[nodo]) > capMax:
            plan['errores'].append('En la parada ' + nodo + ' hay ' + str(len(paradas[nodo])) + ' estudiantes y ningún bus tiene tantos puestos')
    if len(plan['errores']) > 0:
        return plan
    decisiones = []

    # 1. Caminos mínimos (Dijkstra) desde el colegio y desde cada parada
    puntos = [colegio]
    for nodo in nodos:
        if nodo != colegio:
            puntos.append(nodo)
    costo, padres = calcularCostos(grafo, puntos)
    kmEntre = {}
    minEntre = {}
    for a in puntos:
        for b in puntos:
            kmEntre[(a, b)], minEntre[(a, b)] = medirCamino(caminoCalles(padres, a, b), caso['km'], caso['minutos'])
    decisiones.append('Dijkstra: caminos de menor costo desde el colegio y desde las ' + str(len(puntos) - 1) + ' paradas (' + str(len(puntos)) + ' ejecuciones)')

    # 2. Reparto y orden: Clarke-Wright con varios pesos + 2-opt; se queda la asignación válida más barata
    asignacion = None
    mejorTotal = None
    mejorRegistro = None
    mejorPeso = None
    for peso in PESOS_AHORRO:
        registro = []
        rutas = ahorrosClarkeWright(colegio, nodos, paradas, costo, capMax, peso, registro)
        for r in range(len(rutas)):
            rutas[r] = mejorar2opt(rutas[r], colegio, costo, registro)
        candidata = asignarBuses(rutas, paradas, capacidades)
        if candidata is not None:
            totalCandidata = 0
            for ruta in candidata:
                totalCandidata = totalCandidata + costoRuta(ruta, colegio, costo)
            if mejorTotal is None or totalCandidata < mejorTotal - 0.000001:
                asignacion, mejorTotal, mejorRegistro, mejorPeso = candidata, totalCandidata, registro, peso
    if asignacion is None:
        plan['errores'].append('Con ' + str(len(capacidades)) + ' buses y esos puestos no se logró repartir a los estudiantes. Pruebe con más buses o más puestos')
        return plan
    decisiones.append('Se probaron ' + str(len(PESOS_AHORRO)) + ' pesos de ahorro; el mejor fue ' + str(mejorPeso) + ' con costo total ' + str(round(mejorTotal, 2)))
    for linea in mejorRegistro:
        decisiones.append(linea)

    # 3. Sentido del recorrido y horarios de la mañana y de la tarde
    buses = []
    totalKm = 0
    totalMin = 0
    for b in range(len(capacidades)):
        orden = asignacion[b]
        if len(orden) > 0:
            alReves = orden[:]
            alReves.reverse()
            ida = minutosABordo(orden, colegio, paradas, minEntre)
            vuelta = minutosABordo(alReves, colegio, paradas, minEntre)
            if vuelta < ida - 0.000001:
                orden = alReves
            decisiones.append('Bus ' + str(b + 1) + ': ' + str(cargaRuta(orden, paradas)) + ' estudiantes (cupo ' + str(capacidades[b]) + '). Sentido elegido: empieza en ' + orden[0] + ' (' + str(round(min(ida, vuelta), 1)) + ' minutos de estudiantes a bordo contra ' + str(round(max(ida, vuelta), 1)) + ' en el otro sentido)')
        tarde = orden[:]
        tarde.reverse()
        horarioManana = construirHorario(orden, colegio, padres, caso['km'], caso['minutos'], paradas)
        horarioTarde = construirHorario(tarde, colegio, padres, caso['km'], caso['minutos'], paradas)
        ultimo = horarioManana[len(horarioManana) - 1]
        totalKm = totalKm + ultimo['km']
        totalMin = totalMin + ultimo['min']
        buses.append({'cupo': capacidades[b], 'ocupados': cargaRuta(orden, paradas), 'paradas': orden,
                      'costo': costoRuta(orden, colegio, costo), 'km': ultimo['km'], 'min': ultimo['min'],
                      'horarioManana': horarioManana, 'horarioTarde': horarioTarde})

    # 4. Calidad de la ruta: árbol de expansión mínimo (Kruskal) como cota inferior
    aristas, pesoArbol, traza = kruskal(puntos, costo)
    decisiones.append('Kruskal: el árbol mínimo que une el colegio con las paradas pesa ' + str(round(pesoArbol, 2)) + '; ninguna ruta puede costar menos')

    # 5. Se guarda en la tabla hash qué bus recoge a cada estudiante y en qué parada
    for idEst in ids:
        est = tabla.search(idEst)
        tabla.update(idEst, {'nombre': est['nombre'], 'nodo': est['nodo'], 'bus': None, 'orden': None})
    for b in range(len(buses)):
        for pos in range(len(buses[b]['paradas'])):
            for idEst in paradas[buses[b]['paradas'][pos]]:
                est = tabla.search(idEst)
                tabla.update(idEst, {'nombre': est['nombre'], 'nodo': est['nodo'], 'bus': b + 1, 'orden': pos + 1})

    plan['buses'] = buses
    plan['totalCosto'] = mejorTotal
    plan['totalKm'] = totalKm
    plan['totalMin'] = totalMin
    plan['paradas'] = paradas
    plan['puntos'] = puntos
    plan['costo'] = costo
    plan['padres'] = padres
    plan['kmEntre'] = kmEntre
    plan['minEntre'] = minEntre
    plan['arbol'] = aristas
    plan['pesoArbol'] = pesoArbol
    plan['trazaKruskal'] = traza
    plan['decisiones'] = decisiones
    return plan


def rutaSinOptimizar(caso, plan):
    # Referencia: se llenan los buses en el orden de inscripción y se recoge en ese mismo orden
    colegio, ids, tabla = caso['colegio'], caso['ids'], caso['tabla']
    totalCosto = 0
    totalKm = 0
    totalMin = 0
    pos = 0
    for cupo in caso['capacidades']:
        actual = colegio
        ocupados = 0
        while pos < len(ids) and ocupados < cupo:
            nodo = tabla.search(ids[pos])['nodo']
            if nodo != actual:
                totalCosto = totalCosto + plan['costo'][(actual, nodo)]
                totalKm = totalKm + plan['kmEntre'][(actual, nodo)]
                totalMin = totalMin + plan['minEntre'][(actual, nodo)] + MINUTOS_POR_PARADA
            actual = nodo
            ocupados = ocupados + 1
            pos = pos + 1
        totalCosto = totalCosto + plan['costo'][(actual, colegio)]
        totalKm = totalKm + plan['kmEntre'][(actual, colegio)]
        totalMin = totalMin + plan['minEntre'][(actual, colegio)]
    return totalCosto, totalKm, totalMin


def consultarEstudiante(caso, plan, idEst, turno, hora):
    # Vista de padres. turno: 'manana' o 'tarde'. hora: minutos desde la medianoche.
    # La posición del bus se simula con una cola: los puntos del recorrido se atienden en orden de llegada
    est = caso['tabla'].search(idEst)
    if est is None:
        return None
    if est['bus'] is None:
        return {'nombre': est['nombre'], 'bus': None, 'estado': 'sin bus asignado'}
    bus = plan['buses'][est['bus'] - 1]
    if turno == 'manana':
        horario, salida = bus['horarioManana'], SALIDA_MANANA
    else:
        horario, salida = bus['horarioTarde'], SALIDA_TARDE
    minuto = hora - salida
    final = horario[len(horario) - 1]
    for punto in horario:
        if idEst in punto['estudiantes']:
            evento = punto                      # punto donde lo recogen (mañana) o lo dejan (tarde)
    cola = []
    for punto in horario:
        cola.append(punto)
    actual = cola.pop(0)                        # el bus arranca en el colegio
    while len(cola) > 0 and cola[0]['min'] <= minuto:
        actual = cola.pop(0)
    respuesta = {'nombre': est['nombre'], 'bus': est['bus'], 'turno': turno, 'ubicacionBus': actual['nodo']}
    if turno == 'manana':
        respuesta['destino'] = 'al colegio'
        respuesta['horaLlegada'] = salida + final['min']
        if minuto < evento['min']:
            respuesta['estado'] = 'esperando el bus'
            respuesta['minutosParaRecogida'] = evento['min'] - minuto
            respuesta['kmAlColegio'] = final['km'] - evento['km']
            respuesta['minutosParaLlegar'] = final['min'] - minuto
        elif minuto < final['min']:
            respuesta['estado'] = 'en el bus'
            respuesta['kmAlColegio'] = final['km'] - actual['km']
            respuesta['minutosParaLlegar'] = final['min'] - minuto
        else:
            respuesta['estado'] = 'en el colegio'
            respuesta['kmAlColegio'] = 0
            respuesta['minutosParaLlegar'] = 0
    else:
        respuesta['destino'] = 'a la casa'
        respuesta['horaLlegada'] = salida + evento['min']
        if minuto < 0:
            respuesta['estado'] = 'en el colegio'
            respuesta['kmAlColegio'] = 0
            respuesta['minutosParaLlegar'] = evento['min'] - minuto
        elif minuto < evento['min']:
            respuesta['estado'] = 'en el bus'
            respuesta['kmAlColegio'] = actual['km']
            respuesta['minutosParaLlegar'] = evento['min'] - minuto
        else:
            respuesta['estado'] = 'en casa'
            respuesta['kmAlColegio'] = evento['km']
            respuesta['minutosParaLlegar'] = 0
    return respuesta


def agregarEstudiante(caso, idEst, nombre, nodo):
    # Devuelve None si se agregó, o el mensaje del problema
    if caso['tabla'].search(idEst) is not None:
        return 'Ya existe un estudiante con id ' + idEst
    if nodo not in caso['grafo'].vertexes:
        return 'La esquina ' + nodo + ' no existe en el mapa'
    caso['tabla'].insert(idEst, {'nombre': nombre, 'nodo': nodo, 'bus': None, 'orden': None})
    caso['ids'].append(idEst)
    return None


def retirarEstudiante(caso, idEst):
    if caso['tabla'].search(idEst) is None:
        return 'No existe un estudiante con id ' + idEst
    caso['tabla'].delete(idEst)
    caso['ids'].remove(idEst)
    return None


def cerrarCalle(caso, u, v):
    # True si la calle existía y se cerró
    return caso['grafo'].removeEdge(u, v)


def formatoHora(minutos):
    total = int(round(minutos))
    h = total // 60
    m = total % 60
    sufijo = 'a. m.'
    if h >= 12:
        sufijo = 'p. m.'
    if h > 12:
        h = h - 12
    texto = str(m)
    if m < 10:
        texto = '0' + texto
    return str(h) + ':' + texto + ' ' + sufijo
