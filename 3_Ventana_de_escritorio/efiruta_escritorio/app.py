# EfiRuta - ventana de escritorio
# Se ejecuta desde la terminal o el cmd, dentro de esta carpeta:   python app.py
# (en Mac puede ser:  python3 app.py). No necesita instalar nada: usa tkinter, que viene con Python.

import tkinter as tk
from tkinter import ttk
from logica import *

COLOR_BUS = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948']
AZUL = '#14213d'
FONDO = '#f3f2ee'
PAPEL = '#fcfcfb'
TINTA = '#0b0b0b'
TINTA_SUAVE = '#52514e'
VIA = '#c4c3bd'
ROJO = '#c0392b'
VERDE = '#1e7d4f'
AMARILLO = '#f2b705'
FUENTE = 'Helvetica'
ANCHO_KM = 2.6          # ancho del mapa en km (de la Autopista Norte a la Carrera 7)
ALTO_KM = 3.2           # alto del mapa en km (de la Calle 100 a la Calle 134)


def nombreEsquina(nodo):
    # 'Cl116-Kr11' -> 'Cl 116 con Kr 11'
    partes = nodo.split('-')
    calle = partes[0].replace('Cl', 'Cl ')
    carrera = partes[1].replace('Kr', 'Kr ').replace('Auto', 'Autopista')
    return calle + ' con ' + carrera


def posicionBus(horario, minuto):
    # Devuelve (índice del último punto por el que pasó el bus, fracción recorrida hacia el siguiente)
    ultimo = len(horario) - 1
    if minuto >= horario[ultimo]['min']:
        return ultimo, 0
    i = 0
    while i + 1 < len(horario) and horario[i + 1]['min'] <= minuto:
        i = i + 1
    salida = horario[i]['min']
    if len(horario[i]['estudiantes']) > 0:
        salida = salida + MINUTOS_POR_PARADA          # el bus espera en la parada
    if minuto <= salida or horario[i + 1]['min'] <= salida:
        return i, 0
    return i, (minuto - salida) / (horario[i + 1]['min'] - salida)


class App:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title('EfiRuta - Rutas escolares')
        self.raiz.geometry('1320x800')
        self.raiz.minsize(1120, 700)
        self.raiz.configure(bg=FONDO)

        self.caso = self.crearCaso()
        self.plan = calcularRutas(self.caso)
        self.cerradas = []              # calles cerradas, para dibujarlas en rojo
        self.minuto = 0.0               # minutos desde que salen los buses
        self.corriendo = False
        self.resaltados = []            # esquinas que se resaltan al elegir una decisión
        self.estudiante = None          # id del estudiante que consulta el padre

        self.turno = tk.StringVar(value='manana')
        self.verArbol = tk.BooleanVar(value=False)
        self.varTiempo = tk.DoubleVar(value=0)
        self.varVelocidad = tk.DoubleVar(value=1.5)

        self.ponerEstilos()
        self.construirEncabezado()
        self.construirCuerpo()
        self.refrescarTodo()
        self.raiz.after(40, self.tic)

    # ------------------------------------------------------------------ datos

    def crearCaso(self):
        nodos, coords, tramos = construirMapa()
        self.tramos = tramos
        return construirCaso(nodos, coords, tramos, COLEGIO, ESTUDIANTES, BUSES)

    def horarioDe(self, bus):
        if self.turno.get() == 'manana':
            return bus['horarioManana']
        return bus['horarioTarde']

    def salida(self):
        if self.turno.get() == 'manana':
            return SALIDA_MANANA
        return SALIDA_TARDE

    def duracion(self):
        mayor = 0
        if self.plan is not None:
            for bus in self.plan['buses']:
                mayor = max(mayor, bus['min'])
        return mayor

    def recalcular(self, mensaje):
        # Vuelve a calcular las rutas después de un cambio y actualiza toda la ventana
        plan = calcularRutas(self.caso)
        if len(plan['errores']) > 0:
            self.plan = None
            self.avisar(mensaje + ' No se pueden armar las rutas: ' + ' '.join(plan['errores']), ROJO)
        else:
            self.plan = plan
            self.avisar(mensaje + ' Rutas recalculadas: ' + str(round(plan['totalKm'], 1)) + ' km y ' + str(round(plan['totalMin'])) + ' min.', VERDE)
        self.minuto = 0.0
        self.corriendo = False
        self.resaltados = []
        self.refrescarTodo()

    # ------------------------------------------------------------------ ventana

    def ponerEstilos(self):
        estilo = ttk.Style()
        estilo.theme_use('clam')
        estilo.configure('.', background=FONDO, foreground=TINTA, font=(FUENTE, 11))
        estilo.configure('TNotebook', background=FONDO, borderwidth=0)
        estilo.configure('TNotebook.Tab', padding=(14, 7), font=(FUENTE, 11), background='#e4e2db')
        estilo.map('TNotebook.Tab', background=[('selected', PAPEL)], foreground=[('selected', AZUL)])
        estilo.configure('TFrame', background=FONDO)
        estilo.configure('Panel.TFrame', background=PAPEL)
        estilo.configure('TLabel', background=FONDO)
        estilo.configure('Panel.TLabel', background=PAPEL)
        estilo.configure('Suave.TLabel', background=PAPEL, foreground=TINTA_SUAVE, font=(FUENTE, 10))
        estilo.configure('Titulo.TLabel', background=PAPEL, foreground=AZUL, font=(FUENTE, 12, 'bold'))
        estilo.configure('TButton', padding=(10, 5), background='#e4e2db', font=(FUENTE, 11))
        estilo.map('TButton', background=[('active', '#d6d4cc')])
        estilo.configure('Principal.TButton', background=AZUL, foreground='white', font=(FUENTE, 11, 'bold'))
        estilo.map('Principal.TButton', background=[('active', '#23375c')])
        estilo.configure('TRadiobutton', background=FONDO)
        estilo.configure('TCheckbutton', background=FONDO)

    def construirEncabezado(self):
        barra = tk.Frame(self.raiz, bg=AZUL, height=58)
        barra.pack(side='top', fill='x')
        barra.pack_propagate(False)
        tk.Label(barra, text='EfiRuta', bg=AZUL, fg='white', font=(FUENTE, 20, 'bold')).pack(side='left', padx=(18, 10))
        tk.Label(barra, text='Rutas de transporte escolar · Bogotá, Calle 100 a Calle 134', bg=AZUL, fg='#b9c3d6', font=(FUENTE, 11)).pack(side='left')
        self.reloj = tk.Label(barra, text='', bg=AZUL, fg='white', font=(FUENTE, 20, 'bold'))
        self.reloj.pack(side='right', padx=18)
        self.textoTurno = tk.Label(barra, text='', bg=AZUL, fg='#b9c3d6', font=(FUENTE, 11))
        self.textoTurno.pack(side='right')

    def construirCuerpo(self):
        cuerpo = ttk.Frame(self.raiz)
        cuerpo.pack(side='top', fill='both', expand=True, padx=12, pady=12)

        # ----- panel derecho: pestañas -----
        derecha = ttk.Frame(cuerpo, width=430)
        derecha.pack(side='right', fill='y', padx=(12, 0))
        derecha.pack_propagate(False)
        self.mensaje = tk.Label(derecha, text='', bg=FONDO, fg=VERDE, font=(FUENTE, 10), wraplength=420, justify='left', anchor='w')
        self.mensaje.pack(side='bottom', fill='x', pady=(8, 0))
        self.pestanas = ttk.Notebook(derecha)
        self.pestanas.pack(side='top', fill='both', expand=True)
        self.construirPestanaRutas()
        self.construirPestanaDecisiones()
        self.construirPestanaPadres()
        self.construirPestanaCoordinador()

        # ----- panel izquierdo: mapa y controles -----
        izquierda = ttk.Frame(cuerpo)
        izquierda.pack(side='left', fill='both', expand=True)
        controles = ttk.Frame(izquierda)
        controles.pack(side='bottom', fill='x', pady=(10, 0))
        fila = ttk.Frame(controles)
        fila.pack(side='top', fill='x')
        ttk.Radiobutton(fila, text='Mañana (recogida)', variable=self.turno, value='manana', command=self.alCambiarTurno).pack(side='left')
        ttk.Radiobutton(fila, text='Tarde (entrega)', variable=self.turno, value='tarde', command=self.alCambiarTurno).pack(side='left', padx=(8, 16))
        self.botonIniciar = ttk.Button(fila, text='Iniciar recorrido', style='Principal.TButton', command=self.alIniciar, width=16)
        self.botonIniciar.pack(side='left')
        ttk.Button(fila, text='Reiniciar', command=self.alReiniciar).pack(side='left', padx=6)
        ttk.Checkbutton(fila, text='Ver árbol mínimo (Kruskal)', variable=self.verArbol, command=self.dibujarMapa).pack(side='right')
        fila = ttk.Frame(controles)
        fila.pack(side='top', fill='x', pady=(8, 0))
        ttk.Label(fila, text='Tiempo').pack(side='left', padx=(0, 6))
        self.barraTiempo = ttk.Scale(fila, variable=self.varTiempo, from_=0, to=1, command=self.alMoverTiempo)
        self.barraTiempo.pack(side='left', fill='x', expand=True)
        ttk.Label(fila, text='Velocidad').pack(side='left', padx=(16, 6))
        ttk.Scale(fila, variable=self.varVelocidad, from_=0.5, to=6, length=110).pack(side='left')

        self.lienzo = tk.Canvas(izquierda, bg=PAPEL, highlightthickness=1, highlightbackground='#dcdad2')
        self.lienzo.pack(side='top', fill='both', expand=True)
        self.lienzo.bind('<Configure>', self.alCambiarTamano)

    def construirPestanaRutas(self):
        marco = ttk.Frame(self.pestanas, style='Panel.TFrame')
        self.pestanas.add(marco, text='Rutas')
        barra = ttk.Scrollbar(marco, orient='vertical')
        self.textoRutas = tk.Text(marco, wrap='word', bg=PAPEL, fg=TINTA, font=(FUENTE, 11), relief='flat', padx=12, pady=10,
                                  yscrollcommand=barra.set, cursor='arrow', spacing1=2, spacing3=2)
        barra.config(command=self.textoRutas.yview)
        barra.pack(side='right', fill='y')
        self.textoRutas.pack(side='left', fill='both', expand=True)
        self.textoRutas.tag_configure('titulo', font=(FUENTE, 12, 'bold'), foreground=AZUL, spacing1=10)
        self.textoRutas.tag_configure('suave', foreground=TINTA_SUAVE, font=(FUENTE, 10))
        self.textoRutas.tag_configure('error', foreground=ROJO)
        for b in range(len(COLOR_BUS)):
            self.textoRutas.tag_configure('bus' + str(b), foreground=COLOR_BUS[b], font=(FUENTE, 13, 'bold'))

    def construirPestanaDecisiones(self):
        marco = ttk.Frame(self.pestanas, style='Panel.TFrame')
        self.pestanas.add(marco, text='Decisiones')
        ttk.Label(marco, text='Paso a paso de lo que decidió el programa. Al elegir un paso se marcan sus esquinas en el mapa.',
                  style='Suave.TLabel', wraplength=400, justify='left').pack(side='top', fill='x', padx=12, pady=(10, 6))
        self.detalle = tk.Label(marco, text='', bg='#eef2f8', fg=TINTA, font=(FUENTE, 11), wraplength=380, justify='left', anchor='nw', padx=10, pady=8, height=5)
        self.detalle.pack(side='bottom', fill='x', padx=12, pady=10)
        botones = ttk.Frame(marco, style='Panel.TFrame')
        botones.pack(side='bottom', fill='x', padx=12)
        ttk.Button(botones, text='Paso anterior', command=self.alPasoAnterior).pack(side='left')
        ttk.Button(botones, text='Paso siguiente', command=self.alPasoSiguiente).pack(side='left', padx=6)
        barra = ttk.Scrollbar(marco, orient='vertical')
        self.listaDecisiones = tk.Listbox(marco, bg=PAPEL, fg=TINTA, font=(FUENTE, 10), relief='flat', activestyle='none', highlightthickness=0,
                                          selectbackground=AZUL, selectforeground='white', yscrollcommand=barra.set, exportselection=False)
        barra.config(command=self.listaDecisiones.yview)
        barra.pack(side='right', fill='y', pady=(0, 8))
        self.listaDecisiones.pack(side='left', fill='both', expand=True, padx=(12, 0), pady=(0, 8))
        self.listaDecisiones.bind('<<ListboxSelect>>', self.alElegirDecision)

    def construirPestanaPadres(self):
        marco = ttk.Frame(self.pestanas, style='Panel.TFrame')
        self.pestanas.add(marco, text='Padres')
        ttk.Label(marco, text='¿Dónde va mi hijo?', style='Titulo.TLabel').pack(side='top', anchor='w', padx=14, pady=(14, 2))
        ttk.Label(marco, text='Elija al estudiante. Los datos cambian mientras avanza el recorrido.', style='Suave.TLabel',
                  wraplength=390, justify='left').pack(side='top', anchor='w', padx=14)
        self.comboEstudiante = ttk.Combobox(marco, state='readonly', font=(FUENTE, 11))
        self.comboEstudiante.pack(side='top', fill='x', padx=14, pady=10)
        self.comboEstudiante.bind('<<ComboboxSelected>>', self.alElegirEstudiante)
        tarjeta = tk.Frame(marco, bg='#eef2f8')
        tarjeta.pack(side='top', fill='x', padx=14)
        self.padreNombre = tk.Label(tarjeta, text='', bg='#eef2f8', fg=TINTA, font=(FUENTE, 15, 'bold'), anchor='w')
        self.padreNombre.pack(side='top', fill='x', padx=14, pady=(12, 0))
        self.padreBus = tk.Label(tarjeta, text='', bg='#eef2f8', fg='white', font=(FUENTE, 11, 'bold'), padx=8, pady=2)
        self.padreBus.pack(side='top', anchor='w', padx=14, pady=(6, 0))
        self.padreEstado = tk.Label(tarjeta, text='', bg='#eef2f8', fg=AZUL, font=(FUENTE, 22, 'bold'), anchor='w')
        self.padreEstado.pack(side='top', fill='x', padx=14, pady=(10, 0))
        self.padreDatos = tk.Label(tarjeta, text='', bg='#eef2f8', fg=TINTA, font=(FUENTE, 12), anchor='w', justify='left', wraplength=370)
        self.padreDatos.pack(side='top', fill='x', padx=14, pady=(8, 14))
        ttk.Label(marco, text='La posición del bus es simulada con el reloj de la ventana. No es un GPS.', style='Suave.TLabel',
                  wraplength=390, justify='left').pack(side='top', anchor='w', padx=14, pady=10)

    def construirPestanaCoordinador(self):
        marco = ttk.Frame(self.pestanas, style='Panel.TFrame')
        self.pestanas.add(marco, text='Coordinador')
        self.nombreANodo = {}
        nombres = []
        for nodo in self.caso['grafo'].vertexes:
            self.nombreANodo[nombreEsquina(nodo)] = nodo
            nombres.append(nombreEsquina(nodo))

        ttk.Label(marco, text='Buses', style='Titulo.TLabel').pack(side='top', anchor='w', padx=14, pady=(12, 2))
        ttk.Label(marco, text='Puestos de cada bus, separados por espacio', style='Suave.TLabel').pack(side='top', anchor='w', padx=14)
        fila = ttk.Frame(marco, style='Panel.TFrame')
        fila.pack(side='top', fill='x', padx=14, pady=4)
        self.entradaBuses = ttk.Entry(fila, font=(FUENTE, 11))
        self.entradaBuses.pack(side='left', fill='x', expand=True)
        ttk.Button(fila, text='Aplicar', command=self.alCambiarBuses).pack(side='left', padx=(6, 0))

        ttk.Label(marco, text='Agregar estudiante', style='Titulo.TLabel').pack(side='top', anchor='w', padx=14, pady=(12, 2))
        fila = ttk.Frame(marco, style='Panel.TFrame')
        fila.pack(side='top', fill='x', padx=14, pady=2)
        ttk.Label(fila, text='Id', style='Panel.TLabel', width=8).pack(side='left')
        self.entradaId = ttk.Entry(fila, font=(FUENTE, 11), width=10)
        self.entradaId.pack(side='left')
        ttk.Label(fila, text='Nombre', style='Panel.TLabel').pack(side='left', padx=(10, 6))
        self.entradaNombre = ttk.Entry(fila, font=(FUENTE, 11))
        self.entradaNombre.pack(side='left', fill='x', expand=True)
        fila = ttk.Frame(marco, style='Panel.TFrame')
        fila.pack(side='top', fill='x', padx=14, pady=2)
        ttk.Label(fila, text='Esquina', style='Panel.TLabel', width=8).pack(side='left')
        self.comboEsquina = ttk.Combobox(fila, state='readonly', values=nombres, font=(FUENTE, 11))
        self.comboEsquina.pack(side='left', fill='x', expand=True)
        ttk.Button(fila, text='Agregar', command=self.alAgregar).pack(side='left', padx=(6, 0))

        ttk.Label(marco, text='Retirar estudiante', style='Titulo.TLabel').pack(side='top', anchor='w', padx=14, pady=(12, 2))
        fila = ttk.Frame(marco, style='Panel.TFrame')
        fila.pack(side='top', fill='x', padx=14, pady=2)
        self.comboRetirar = ttk.Combobox(fila, state='readonly', font=(FUENTE, 11))
        self.comboRetirar.pack(side='left', fill='x', expand=True)
        ttk.Button(fila, text='Retirar', command=self.alRetirar).pack(side='left', padx=(6, 0))

        ttk.Label(marco, text='Cerrar una calle', style='Titulo.TLabel').pack(side='top', anchor='w', padx=14, pady=(12, 2))
        fila = ttk.Frame(marco, style='Panel.TFrame')
        fila.pack(side='top', fill='x', padx=14, pady=2)
        ttk.Label(fila, text='Desde', style='Panel.TLabel', width=8).pack(side='left')
        self.comboDesde = ttk.Combobox(fila, state='readonly', values=nombres, font=(FUENTE, 11))
        self.comboDesde.pack(side='left', fill='x', expand=True)
        self.comboDesde.bind('<<ComboboxSelected>>', self.alElegirDesde)
        fila = ttk.Frame(marco, style='Panel.TFrame')
        fila.pack(side='top', fill='x', padx=14, pady=2)
        ttk.Label(fila, text='Hasta', style='Panel.TLabel', width=8).pack(side='left')
        self.comboHasta = ttk.Combobox(fila, state='readonly', font=(FUENTE, 11))
        self.comboHasta.pack(side='left', fill='x', expand=True)
        ttk.Button(fila, text='Cerrar', command=self.alCerrar).pack(side='left', padx=(6, 0))

        ttk.Button(marco, text='Volver al caso inicial', command=self.alRestablecer).pack(side='top', anchor='w', padx=14, pady=(18, 0))

    # ------------------------------------------------------------------ mapa

    def aPixel(self, x, y):
        # Pasa de km del mapa a pixeles del lienzo (el norte queda arriba)
        ancho = max(self.lienzo.winfo_width(), 300)
        alto = max(self.lienzo.winfo_height(), 300)
        escala = min((ancho - 135) / ANCHO_KM, (alto - 125) / ALTO_KM)
        x0 = 100 + (ancho - 135 - ANCHO_KM * escala) / 2
        y0 = 62 + (alto - 125 - ALTO_KM * escala) / 2
        return x0 + x * escala, y0 + (ALTO_KM - y) * escala

    def puntoDe(self, nodo):
        x, y = self.caso['coords'][nodo]
        return self.aPixel(x, y)

    def dibujarMapa(self):
        # Capa fija: calles, nombres, rutas, árbol mínimo y colegio
        lienzo = self.lienzo
        lienzo.delete('all')
        grafo = self.caso['grafo']
        for relation in grafo.relations:
            u, v = relation[0], relation[1]
            if u < v:
                velocidad = self.caso['km'][(u, v)] / self.caso['minutos'][(u, v)] * 60
                grosor = 2
                if velocidad > 25:
                    grosor = 5
                if velocidad > 35:
                    grosor = 9
                x1, y1 = self.puntoDe(u)
                x2, y2 = self.puntoDe(v)
                lienzo.create_line(x1, y1, x2, y2, fill=VIA, width=grosor, capstyle='round')
        for calle in self.cerradas:
            x1, y1 = self.puntoDe(calle[0])
            x2, y2 = self.puntoDe(calle[1])
            lienzo.create_line(x1, y1, x2, y2, fill=ROJO, width=3, dash=(6, 4))
            lienzo.create_text((x1 + x2) / 2, (y1 + y2) / 2 - 10, text='cerrada', fill=ROJO, font=(FUENTE, 9, 'bold'))
        for calle in CALLES:
            x, y = self.aPixel(0, calle[2])
            lienzo.create_text(x - 26, y, text=calle[1], anchor='e', fill=TINTA_SUAVE, font=(FUENTE, 10))
        for carrera in CARRERAS:
            x, y = self.aPixel(carrera[2], 0)
            texto = carrera[1].replace('Carrera', 'Kr').replace('Autopista Norte', 'Autopista')
            lienzo.create_text(x, y + 36, text=texto, fill=TINTA_SUAVE, font=(FUENTE, 10))
        # leyenda de vías
        x = 16
        for via in [(9, 'Autopista (40 km/h)'), (5, 'Avenida (30 km/h)'), (2, 'Calle de barrio (20 km/h)')]:
            lienzo.create_line(x, 20, x + 30, 20, fill=VIA, width=via[0], capstyle='round')
            texto = lienzo.create_text(x + 38, 20, text=via[1], anchor='w', fill=TINTA_SUAVE, font=(FUENTE, 10))
            x = lienzo.bbox(texto)[2] + 22

        if self.plan is not None:
            if self.verArbol.get():
                for arista in self.plan['arbol']:
                    x1, y1 = self.puntoDe(arista[0])
                    x2, y2 = self.puntoDe(arista[1])
                    lienzo.create_line(x1, y1, x2, y2, fill=AZUL, width=2, dash=(5, 4))
            cantidad = len(self.plan['buses'])
            for b in range(cantidad):
                horario = self.horarioDe(self.plan['buses'][b])
                if len(horario) > 1:
                    color = COLOR_BUS[b % len(COLOR_BUS)]
                    corrimiento = (b - (cantidad - 1) / 2) * 6
                    puntos = []
                    for punto in horario:
                        x, y = self.puntoDe(punto['nodo'])
                        puntos.append((x + corrimiento, y + corrimiento))
                    plano = []
                    for punto in puntos:
                        plano.append(punto[0])
                        plano.append(punto[1])
                    lienzo.create_line(plano, fill=color, width=4, capstyle='round', joinstyle='round')
                    for k in range(len(puntos) - 1):
                        if puntos[k] != puntos[k + 1]:
                            mx, my = (puntos[k][0] + puntos[k + 1][0]) / 2, (puntos[k][1] + puntos[k + 1][1]) / 2
                            dx, dy = (puntos[k + 1][0] - puntos[k][0]) * 0.02, (puntos[k + 1][1] - puntos[k][1]) * 0.02
                            lienzo.create_line(mx - dx, my - dy, mx + dx, my + dy, fill=color, width=4, arrow='last', arrowshape=(9, 11, 5))
        x, y = self.puntoDe(self.caso['colegio'])
        lienzo.create_rectangle(x - 11, y - 11, x + 11, y + 11, fill=TINTA, outline=PAPEL, width=2)
        lienzo.create_text(x, y + 22, text='Colegio', fill=TINTA, font=(FUENTE, 10, 'bold'))
        self.dibujarMovil()

    def dibujarMovil(self):
        # Capa que cambia con el reloj: paradas, resaltados y buses
        lienzo = self.lienzo
        lienzo.delete('movil')
        for nodo in self.resaltados:
            x, y = self.puntoDe(nodo)
            lienzo.create_oval(x - 21, y - 21, x + 21, y + 21, outline=AMARILLO, width=5, tags='movil')
        if self.plan is None:
            return
        cantidad = len(self.plan['buses'])
        for b in range(cantidad):
            horario = self.horarioDe(self.plan['buses'][b])
            color = COLOR_BUS[b % len(COLOR_BUS)]
            corrimiento = (b - (cantidad - 1) / 2) * 6
            orden = 0
            for punto in horario:
                if len(punto['estudiantes']) > 0:
                    orden = orden + 1
                    x, y = self.puntoDe(punto['nodo'])
                    x, y = x + corrimiento, y + corrimiento
                    if self.estudiante in punto['estudiantes']:
                        lienzo.create_oval(x - 20, y - 20, x + 20, y + 20, outline=TINTA, width=3, tags='movil')
                        nombre = self.caso['tabla'].search(self.estudiante)['nombre']
                        lienzo.create_text(x, y - 30, text=nombre, fill=TINTA, font=(FUENTE, 11, 'bold'), tags='movil')
                    if self.minuto >= punto['min'] and self.minuto > 0:       # el bus ya pasó por esta parada
                        lienzo.create_oval(x - 12, y - 12, x + 12, y + 12, fill=color, outline=PAPEL, width=2, tags='movil')
                        lienzo.create_text(x, y, text=str(orden), fill='white', font=(FUENTE, 10, 'bold'), tags='movil')
                    else:
                        lienzo.create_oval(x - 12, y - 12, x + 12, y + 12, fill='white', outline=color, width=3, tags='movil')
                        lienzo.create_text(x, y, text=str(orden), fill=TINTA, font=(FUENTE, 10, 'bold'), tags='movil')
        for b in range(cantidad):
            horario = self.horarioDe(self.plan['buses'][b])
            if len(horario) > 1:
                color = COLOR_BUS[b % len(COLOR_BUS)]
                corrimiento = (b - (cantidad - 1) / 2) * 6
                i, fraccion = posicionBus(horario, self.minuto)
                x, y = self.puntoDe(horario[i]['nodo'])
                if fraccion > 0:
                    x2, y2 = self.puntoDe(horario[i + 1]['nodo'])
                    x, y = x + (x2 - x) * fraccion, y + (y2 - y) * fraccion
                x, y = x + corrimiento, y + corrimiento
                lienzo.create_rectangle(x - 17, y - 11, x + 17, y + 11, fill=color, outline=TINTA, width=2, tags='movil')
                lienzo.create_text(x, y, text='Bus ' + str(b + 1), fill='white', font=(FUENTE, 9, 'bold'), tags='movil')

    # ------------------------------------------------------------------ paneles

    def avisar(self, texto, color):
        self.mensaje.config(text=texto, fg=color)

    def refrescarTodo(self):
        self.barraTiempo.config(to=max(self.duracion(), 1))
        self.varTiempo.set(self.minuto)
        self.botonIniciar.config(text='Iniciar recorrido')
        capacidades = []
        for cupo in self.caso['capacidades']:
            capacidades.append(str(cupo))
        self.entradaBuses.delete(0, 'end')
        self.entradaBuses.insert(0, ' '.join(capacidades))
        estudiantes = []
        for idEst in self.caso['ids']:
            estudiantes.append(idEst + ' - ' + self.caso['tabla'].search(idEst)['nombre'])
        self.comboEstudiante.config(values=estudiantes)
        self.comboRetirar.config(values=estudiantes)
        self.comboRetirar.set('')
        if self.estudiante is not None and self.caso['tabla'].search(self.estudiante) is None:
            self.estudiante = None
            self.comboEstudiante.set('')
        self.llenarRutas()
        self.llenarDecisiones()
        self.actualizarReloj()
        self.actualizarPadres()
        self.dibujarMapa()

    def llenarRutas(self):
        texto = self.textoRutas
        texto.config(state='normal')
        texto.delete('1.0', 'end')
        if self.plan is None:
            texto.insert('end', 'No hay rutas calculadas.\n', 'error')
            texto.insert('end', 'Revise el aviso de abajo y corrija los datos en la pestaña Coordinador.\n', 'suave')
            texto.config(state='disabled')
            return
        tabla = self.caso['tabla']
        for b in range(len(self.plan['buses'])):
            bus = self.plan['buses'][b]
            texto.insert('end', 'Bus ' + str(b + 1) + '\n', 'bus' + str(b % len(COLOR_BUS)))
            if len(bus['paradas']) == 0:
                texto.insert('end', 'No se necesita en este caso.\n', 'suave')
            else:
                texto.insert('end', str(bus['ocupados']) + ' de ' + str(bus['cupo']) + ' puestos · ' + str(round(bus['km'], 1)) + ' km · ' + str(round(bus['min'])) +
                             ' min · llega ' + formatoHora(self.salida() + bus['min']) + '\n', 'suave')
                for punto in self.horarioDe(bus):
                    if len(punto['estudiantes']) > 0:
                        nombres = []
                        for idEst in punto['estudiantes']:
                            nombres.append(tabla.search(idEst)['nombre'])
                        texto.insert('end', formatoHora(self.salida() + punto['min']) + '   ' + nombreEsquina(punto['nodo']) + '   ' + ', '.join(nombres) + '\n')
        costoBase, kmBase, minBase = rutaSinOptimizar(self.caso, self.plan)
        texto.insert('end', 'Total\n', 'titulo')
        texto.insert('end', str(round(self.plan['totalKm'], 1)) + ' km y ' + str(round(self.plan['totalMin'])) + ' min de bus\n')
        texto.insert('end', 'En orden de inscripción serían ' + str(round(kmBase, 1)) + ' km y ' + str(round(minBase)) + ' min\n', 'suave')
        texto.insert('end', 'Calidad de la ruta\n', 'titulo')
        texto.insert('end', 'Costo ' + str(round(self.plan['totalCosto'], 2)) + ' · árbol mínimo ' + str(round(self.plan['pesoArbol'], 2)) + '\n')
        texto.insert('end', 'Las rutas cuestan ' + str(round(self.plan['totalCosto'] / self.plan['pesoArbol'], 2)) + ' veces la cota de Kruskal\n', 'suave')
        texto.config(state='disabled')

    def llenarDecisiones(self):
        self.listaDecisiones.delete(0, 'end')
        self.detalle.config(text='')
        if self.plan is not None:
            numero = 0
            for linea in self.plan['decisiones']:
                numero = numero + 1
                self.listaDecisiones.insert('end', str(numero) + '. ' + linea)

    def actualizarReloj(self):
        self.reloj.config(text=formatoHora(self.salida() + self.minuto))
        if self.turno.get() == 'manana':
            self.textoTurno.config(text='Recogida de la mañana')
        else:
            self.textoTurno.config(text='Entrega de la tarde')

    def actualizarPadres(self):
        if self.estudiante is None or self.plan is None:
            self.padreNombre.config(text='Sin estudiante elegido')
            self.padreBus.config(text='', bg='#eef2f8')
            self.padreEstado.config(text='')
            self.padreDatos.config(text='')
            return
        r = consultarEstudiante(self.caso, self.plan, self.estudiante, self.turno.get(), self.salida() + self.minuto)
        if r is None or r['bus'] is None:
            # El estudiante ya no existe o no tiene bus: se deja la tarjeta vacía
            self.estudiante = None
            self.comboEstudiante.set('')
            self.actualizarPadres()
            return
        self.padreNombre.config(text=r['nombre'] + ' (' + self.estudiante + ')')
        self.padreBus.config(text='Bus ' + str(r['bus']), bg=COLOR_BUS[(r['bus'] - 1) % len(COLOR_BUS)])
        self.padreEstado.config(text=r['estado'].capitalize())
        lineas = ['El bus va por ' + nombreEsquina(r['ubicacionBus'])]
        lineas.append('Distancia al colegio: ' + str(round(r['kmAlColegio'], 1)) + ' km')
        if 'minutosParaRecogida' in r:
            lineas.append('Lo recogen en ' + str(round(r['minutosParaRecogida'])) + ' min')
        if r['minutosParaLlegar'] > 0:
            lineas.append('Llega ' + r['destino'] + ' en ' + str(round(r['minutosParaLlegar'])) + ' min (' + formatoHora(r['horaLlegada']) + ')')
        else:
            lineas.append('Llegó ' + r['destino'] + ' a las ' + formatoHora(r['horaLlegada']))
        self.padreDatos.config(text='\n'.join(lineas))

    # ------------------------------------------------------------------ eventos

    def tic(self):
        # Reloj de la simulación: se llama cada 40 milisegundos
        if self.corriendo:
            self.minuto = self.minuto + self.varVelocidad.get() * 0.04
            if self.minuto >= self.duracion():
                self.minuto = self.duracion()
                self.corriendo = False
                self.botonIniciar.config(text='Iniciar recorrido')
            self.varTiempo.set(self.minuto)
            self.actualizarReloj()
            self.actualizarPadres()
            self.dibujarMovil()
        self.raiz.after(40, self.tic)

    def alCambiarTamano(self, evento):
        self.dibujarMapa()

    def alIniciar(self):
        if self.plan is None:
            return
        if self.corriendo:
            self.corriendo = False
            self.botonIniciar.config(text='Continuar')
        else:
            if self.minuto >= self.duracion():
                self.minuto = 0.0
            self.corriendo = True
            self.botonIniciar.config(text='Pausar')

    def alReiniciar(self):
        self.corriendo = False
        self.minuto = 0.0
        self.varTiempo.set(0)
        self.botonIniciar.config(text='Iniciar recorrido')
        self.actualizarReloj()
        self.actualizarPadres()
        self.dibujarMovil()

    def alMoverTiempo(self, valor):
        self.minuto = float(valor)
        self.actualizarReloj()
        self.actualizarPadres()
        self.dibujarMovil()

    def alCambiarTurno(self):
        self.alReiniciar()
        self.llenarRutas()
        self.dibujarMapa()

    def alElegirDecision(self, evento):
        elegido = self.listaDecisiones.curselection()
        self.resaltados = []
        if len(elegido) > 0:
            linea = self.plan['decisiones'][elegido[0]]
            self.detalle.config(text=linea)
            for nodo in self.caso['grafo'].vertexes:
                if nodo in linea:
                    self.resaltados.append(nodo)
        self.dibujarMovil()

    def moverPaso(self, cambio):
        if self.plan is None:
            return
        elegido = self.listaDecisiones.curselection()
        nuevo = 0
        if len(elegido) > 0:
            nuevo = elegido[0] + cambio
        nuevo = max(0, min(nuevo, len(self.plan['decisiones']) - 1))
        self.listaDecisiones.selection_clear(0, 'end')
        self.listaDecisiones.selection_set(nuevo)
        self.listaDecisiones.see(nuevo)
        self.alElegirDecision(None)

    def alPasoAnterior(self):
        self.moverPaso(-1)

    def alPasoSiguiente(self):
        self.moverPaso(1)

    def alElegirEstudiante(self, evento):
        self.estudiante = self.comboEstudiante.get().split(' - ')[0]
        if self.caso['tabla'].search(self.estudiante) is None:
            self.estudiante = None
        self.actualizarPadres()
        self.dibujarMovil()

    def alCambiarBuses(self):
        partes = self.entradaBuses.get().split()
        capacidades = []
        for parte in partes:
            if parte.isdigit() and int(parte) > 0:
                capacidades.append(int(parte))
        if len(partes) == 0 or len(capacidades) != len(partes):
            self.avisar('Escriba los puestos de cada bus con números mayores que 0, separados por espacio. Ejemplo: 8 7 7', ROJO)
            return
        self.caso['capacidades'] = capacidades
        self.recalcular('Ahora hay ' + str(len(capacidades)) + ' buses.')

    def alAgregar(self):
        idEst = self.entradaId.get().strip()
        nombre = self.entradaNombre.get().strip()
        esquina = self.comboEsquina.get()
        if idEst == '' or nombre == '' or esquina not in self.nombreANodo:
            self.avisar('Para agregar un estudiante faltan el id, el nombre o la esquina.', ROJO)
            return
        problema = agregarEstudiante(self.caso, idEst, nombre, self.nombreANodo[esquina])
        if problema is not None:
            self.avisar(problema, ROJO)
            return
        self.entradaId.delete(0, 'end')
        self.entradaNombre.delete(0, 'end')
        self.recalcular('Se agregó a ' + nombre + '.')

    def alRetirar(self):
        elegido = self.comboRetirar.get()
        if elegido == '':
            self.avisar('Elija al estudiante que se va a retirar.', ROJO)
            return
        idEst = elegido.split(' - ')[0]
        est = self.caso['tabla'].search(idEst)
        if est is None:
            self.avisar('No existe un estudiante con id ' + idEst + '.', ROJO)
            return
        retirarEstudiante(self.caso, idEst)
        self.recalcular('Se retiró a ' + est['nombre'] + '.')

    def alElegirDesde(self, evento):
        vecinos = []
        if self.comboDesde.get() in self.nombreANodo:
            for vecino in self.caso['grafo'].getNeighbors(self.nombreANodo[self.comboDesde.get()]):
                vecinos.append(nombreEsquina(vecino))
        vecinos.sort()
        self.comboHasta.config(values=vecinos)
        self.comboHasta.set('')

    def alCerrar(self):
        if self.comboDesde.get() not in self.nombreANodo or self.comboHasta.get() not in self.nombreANodo:
            self.avisar('Elija las dos esquinas de la calle que se va a cerrar.', ROJO)
            return
        u, v = self.nombreANodo[self.comboDesde.get()], self.nombreANodo[self.comboHasta.get()]
        if cerrarCalle(self.caso, u, v):
            self.cerradas.append((u, v))
            self.comboHasta.set('')
            self.comboHasta.config(values=[])
            self.recalcular('Se cerró la calle entre ' + nombreEsquina(u) + ' y ' + nombreEsquina(v) + '.')
        else:
            self.avisar('No hay una calle entre esas dos esquinas.', ROJO)

    def alRestablecer(self):
        self.caso = self.crearCaso()
        self.cerradas = []
        self.estudiante = None
        self.comboEstudiante.set('')
        self.recalcular('Se volvió al caso inicial.')


def main():
    raiz = tk.Tk()
    App(raiz)
    raiz.mainloop()


if __name__ == '__main__':
    main()
