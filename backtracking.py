import soko
DIRECCIONES={'ESTE':(1, 0) , 'OESTE': (-1, 0) , 'NORTE': (0, -1) , 'SUR': (0, 1)}

def grilla_a_inmutable(grilla):
    '''Recibe una grilla de listas y devuelve una nueva grilla de tuplas'''
    grilla_inmutable = []

    for fila in grilla:
        grilla_inmutable.append(tuple(fila)) 

    grilla_inmutable = tuple(grilla_inmutable)
    return grilla_inmutable

def inmutable_a_grilla(inmutable):
    '''Recibe una grilla de tuplas y la vuelve una lista de listas'''
    grilla = []
    for fila in inmutable:
        grilla.append(list(fila))
    return grilla

def agregar(estado,visitados):
    '''Recibe un estado y un diccionario con los estados ya visitados, 
    y agrega el estado a visitados con el numero de estados realizados (empezando desde 0) como clave'''
    contador = len(visitados.keys())
    visitados[estado] = contador

def concatenar(accion,acciones):
    '''Recibe un diccionario con las acciones realizadas hasta el momento y le agrega una nueva accion
    realizada cuya clave es el numero de acciones realizadas hasta el momento (cuenta desde 0)'''
    contador = len(acciones.keys())
    acciones[contador] = accion
    return acciones

def buscar_solucion(grilla_actual):
    '''Busca una solucion a la grilla actual, devuelve True si existe y un diccionario con los movimientos (las claves corresponden
    al orden en que se realizan iniciando en 0. De lo contrario devuelve False y False'''
    visitados = {}
    grilla_actual = grilla_a_inmutable(grilla_actual)
    return backtrack(grilla_actual, visitados)


def backtrack(estado, visitados):
    '''Recibe un estado como grilla de tuplas y los estados ya visitados y realiza un backtrack, en caso de encontrar
    la solucion devuelve True y como llegar a la misma en forma de diccionario. De lo contrario devuelve False y False.'''

    agregar(estado,visitados)
   
    if soko.juego_ganado(estado):
        return True, {}

    for direccion in DIRECCIONES.keys():
        if soko.movimientos_no_permitidos(estado,DIRECCIONES[direccion]) == True:
            continue

        nuevo_estado = grilla_a_inmutable(soko.mover(estado, DIRECCIONES[direccion]))
        if  nuevo_estado in visitados:
            continue

        solución_encontrada, acciones = backtrack(nuevo_estado, visitados)
        
        if solución_encontrada:
            return True, concatenar(direccion,acciones)

    return False, False
