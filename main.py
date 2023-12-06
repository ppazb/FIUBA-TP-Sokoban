import soko
import gamelib
import pilas 
import backtracking
import time
from datetime import datetime

RUTA_NIVELES='niveles.txt'
RUTA_TECLAS='teclas.txt'
NIVEL_COMPLETADO= 'img/finish.wav'
CANTIDAD_NIVELES=155

ALTO_CASILLA=70
LARGO_CASILLA=70

ANCHO_MENSAJE=70
ALTO_MENSAJE=70

COLOR_NIVEL='black'
COLOR_ERROR_PISTA= '#330066'
COLOR_PISTA_DISPONIBLE= '#990033'
COMANDOS_PRINCIPALES="\n Flechas o WASD para moverse \n H = Pista \n Z = Deshacer \n R = Reiniciar \n Esc = Salir"

MOVIMIENTOS={'ESTE':(1, 0) , 'OESTE': (-1, 0) , 'NORTE': (0, -1) , 'SUR': (0, 1),'SALIR':'salir','REINICIAR':'reiniciar','DESHACER':'deshacer','PISTA':'pista'}
URL={'PISO':'img/ground.gif',soko.CAJA:'img/chest.gif',soko.OBJETIVO_JUGADOR:'img/player.gif',soko.JUGADOR:'img/player.gif',soko.OBJETIVO:'img/goal.gif',soko.PARED:'img/wall.gif',soko.OBJETIVO_CAJA:'img/open_chest.gif'}
CARTEL={'izq':'img/textoizq.gif','centro':'img/textocentro.gif','der':'img/textoderecha.gif'}


def generar_desc_niveles(ruta_niveles):
    '''Recibe un string con la ruta donde se encuentran los niveles y devuelve una lista con los mismos.
    Dentro de la lista se encuentra un diccionario con desc de clave y la descripcion como valor. En caso
    de tener nombre se agrega la clave 'nombre' del nivel '''
    niveles=[]
    
    with open(ruta_niveles,'r') as file:
        clave= ''

        for linea in file:
            if linea[0:5] == 'Level':
                clave = int(linea[6:].rstrip('\n'))-1   
                niveles.append({})
                niveles[clave]['desc'] = []

            elif (linea[0] != "'") and (linea[0] !=  '\n') :
                niveles[clave]['desc'].append(linea.rstrip('\n'))

            elif linea[0] == "'":
                niveles[clave]['nombre'] = linea.rstrip('\n')
    return niveles

def emparejar_matriz(nivel):
    '''Recibe un nivel, y completa las filas para que todas tengan igual largo, esto es en el
    caso de que finalice con espacios en blanco no registrados en el archivo de nivel'''
    fila_mas_larga = 0
    for fila in nivel:
        if len(fila) > fila_mas_larga:
            fila_mas_larga = len(fila)

    for fila in nivel:
        while len(fila) < fila_mas_larga:
            fila.append(' ')
    return nivel

def dimension_tablero(nivel):
    '''recibe la grilla del nivel y devuelve 4 variables que representan, en orden:
    numero de columnas, numero de filas, el ancho del tablero en pixeles y alto del tablero en pixeles'''
    dimension = soko.dimensiones(nivel)
    return dimension[0], dimension[1], dimension[0]*LARGO_CASILLA , dimension[1]*ALTO_CASILLA

def coordenada_a_pixel(columna,fila):
    '''recibe una fila y columna de la grilla y devuelve su coordenada del tablero en pixeles teniendo en consideracion el espacio que ocupa
    cada casilla'''
    x =  fila*LARGO_CASILLA
    y = columna*ALTO_CASILLA
    return x,y

def dibujar_piso(columnas,filas):
    '''recibe la cantidad de columnas, filas, ancho y alto del nivel y muestra el piso por pantalla'''
    for x in range(0,LARGO_CASILLA*columnas,LARGO_CASILLA):
        for y in range(0,ALTO_CASILLA*filas,ALTO_CASILLA):
            gamelib.draw_image(URL['PISO'],x,y)

def dibujar_cartel(columnas,filas):
    gamelib.draw_image(CARTEL['izq'], 0, filas*ALTO_CASILLA)
    gamelib.draw_image(CARTEL['der'], LARGO_CASILLA*(columnas-1), filas*ALTO_CASILLA)

    for x in range(LARGO_CASILLA, LARGO_CASILLA*(columnas-1), LARGO_CASILLA):
        gamelib.draw_image(CARTEL['centro'], x, filas*ALTO_CASILLA)


def mostrar_juego(nivel,columnas,filas,numero_nivel,nombre_nivel):
    '''Recibe el nivel actual, el numero del nivel, su nombre(o None), las columnas y filas del mismo, y muestra en pantallas sus elementos'''
    dibujar_piso(columnas,filas)
    dibujar_cartel(columnas,filas)
    if nombre_nivel == None:
        gamelib.draw_text(f'Nivel {numero_nivel+1}', (LARGO_CASILLA*columnas/2), ALTO_CASILLA*filas+ALTO_MENSAJE/3+4,  size=12 , fill=COLOR_NIVEL,anchor='c')

    else:
        nombre_nivel_final= ": "+ nombre_nivel
        gamelib.draw_text(f'Nivel {numero_nivel+1}{nombre_nivel_final}', (LARGO_CASILLA*columnas/2), ALTO_CASILLA*filas+ALTO_MENSAJE/3+4,  size=12 , fill=COLOR_NIVEL,anchor='c')

    for fila in range(0,filas):
        for columna in range(0,columnas):
                elemento = nivel[fila][columna]

                if elemento == soko.OBJETIVO_JUGADOR or elemento == soko.OBJETIVO_CAJA:
                    x,y = coordenada_a_pixel(fila,columna)
                    gamelib.draw_image(URL[soko.OBJETIVO], x, y)

                if elemento != soko.CELDA_VACIA :
                    x,y = coordenada_a_pixel(fila,columna)
                    gamelib.draw_image(URL[elemento], x, y)


def diccionario_de_teclas(ruta_teclas):
    '''Recibe la ruta de las teclas para el juego como string y genera un diccionario la tecla como clave
    y la accionen el juego como valor'''
    dic_teclas = {}

    with open(ruta_teclas,'r') as teclas:
         for linea in teclas:
            if linea !='\n':
                linea = linea.rstrip('\n').split(' = ')
                linea[1] = linea[1]
                dic_teclas[linea[0]] = linea[1]

    return dic_teclas


def tecla_a_accion(diccionario, tecla):
    '''Recibe un diccionario de teclas con sus respectivas acciones como valor y una tecla y devuelve la accion que le corresponde.
    En caso de no ser una tecla que realice una accion, devuelve False'''
    valor = diccionario.get(tecla)
    if valor == None:
        return False
    return MOVIMIENTOS.get(valor.upper())


def main():

    desc_niveles = generar_desc_niveles(RUTA_NIVELES)
    dic_teclas = diccionario_de_teclas(RUTA_TECLAS)
    numero_nivel = 0
    nivel_actual = soko.crear_grilla(desc_niveles[numero_nivel]['desc'])

    try:
        nombre_nivel = desc_niveles[numero_nivel]['nombre']
    except:
        nombre_nivel = None

    nivel_actual = emparejar_matriz(nivel_actual)
    columnas,filas,ancho_tablero,alto_tablero = dimension_tablero(nivel_actual)

    mov_anteriores = pilas.Pila()
    posibilidad_hint, movimientos_hint = None,None
    solucion_no_posible = False #Si no hay pistas para el estado

    gamelib.title('Comandos Principales')
    gamelib.say(f'{COMANDOS_PRINCIPALES} \n\n El juego cuenta con sonido')

    while gamelib.is_alive():

        gamelib.title('Sokoban')
        gamelib.resize(ancho_tablero, alto_tablero+ALTO_MENSAJE)

        gamelib.draw_begin()
        # Dibujar la pantalla
        mostrar_juego(nivel_actual,columnas,filas,numero_nivel,nombre_nivel)
        if solucion_no_posible == True:
            gamelib.draw_text('No se encontraron pistas', (LARGO_CASILLA*columnas/2), ALTO_CASILLA*filas+ALTO_MENSAJE/2+10,  size=11, fill=COLOR_ERROR_PISTA,anchor='c')
        if posibilidad_hint == True:
            gamelib.draw_text('Hay pistas disponibles', (LARGO_CASILLA*columnas/2), ALTO_CASILLA*filas+ALTO_MENSAJE/2+10,  size=11, fill=COLOR_PISTA_DISPONIBLE,anchor='c')
        gamelib.draw_end()

        if soko.juego_ganado(nivel_actual):
            gamelib.play_sound(NIVEL_COMPLETADO)
            time.sleep(2)

            if numero_nivel == (CANTIDAD_NIVELES-1):
                gamelib.title('GAME OVER')
                gamelib.say('¡Juego Ganado!')
                break

            numero_nivel+=1
            nivel_actual= soko.crear_grilla(desc_niveles[numero_nivel]['desc'])
            nivel_actual= emparejar_matriz(nivel_actual)
            columnas,filas,ancho_tablero,alto_tablero= dimension_tablero(nivel_actual)
            try:
                nombre_nivel= desc_niveles[numero_nivel]['nombre']
            except:
                nombre_nivel= None

            while not mov_anteriores.esta_vacia():
                mov_anteriores.desapilar()
            posibilidad_hint, movimientos_hint= None, None
            continue

        # Actualizar el estado del juego, según la `tecla` presionada
        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break
        tecla = ev.key
        movimiento= tecla_a_accion(dic_teclas,tecla)

        if movimiento == False or (movimiento == 'deshacer' and mov_anteriores.esta_vacia()):
            #Tecla apretada/Deshacer no valido
            continue

        if movimiento != 'pista':
            posibilidad_hint, movimientos_hint= None, None
        solucion_no_posible = False #Resetea el mensaje de mov no posible para que no aparezca

        if movimiento == 'reiniciar':
            nivel_actual = soko.crear_grilla(desc_niveles[numero_nivel]['desc'])
            nivel_actual = emparejar_matriz(nivel_actual)
            while not mov_anteriores.esta_vacia():
                mov_anteriores.desapilar()

        elif movimiento == 'salir':
            break

        elif movimiento == 'deshacer' and not mov_anteriores.esta_vacia():
            nivel_actual= soko.crear_grilla(mov_anteriores.desapilar())

        elif movimiento == 'pista':
            if posibilidad_hint == None and movimientos_hint == None:
                posibilidad_hint, movimientos_hint = backtracking.buscar_solucion(nivel_actual)

                if movimientos_hint != False:
                    direcciones=pilas.Pila()
                    cantidad_movs= len(movimientos_hint.keys()) #asumo que el diccionario no necesariamente se guarda en orden
                    for i in range(0,cantidad_movs):
                        direcciones.apilar(movimientos_hint[i])

            if posibilidad_hint == True:
                mov_anteriores.apilar(nivel_actual)
                accion= MOVIMIENTOS.get(direcciones.desapilar())
                nivel_actual= soko.mover(nivel_actual,accion)

            elif posibilidad_hint == False:
                solucion_no_posible = True
        else:
            mov_anteriores.apilar(nivel_actual)
            nivel_actual= soko.mover(nivel_actual,movimiento)

gamelib.init(main)
