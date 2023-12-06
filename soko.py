PARED='#'
CAJA="$"
JUGADOR='@'
OBJETIVO='.'
OBJETIVO_CAJA='*'
OBJETIVO_JUGADOR='+'
CELDA_VACIA=' '


def crear_grilla(desc):
	'''Crea una grilla a partir de la descripción del estado inicial.'''
	grilla=[]
	for fila_desc in desc:
		grilla.append(list(fila_desc))
	return grilla

def dimensiones(grilla):
	'''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
	cantidad_columnas_filas= (len(grilla[0]),len(grilla))
	return cantidad_columnas_filas

def hay_pared(grilla, c, f):
	'''Devuelve True si hay una pared en la columna y fila (c, f).'''
	if grilla[f][c]==PARED:
		return True
	return False

def hay_objetivo(grilla, c, f):
	'''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
	if grilla[f][c]==OBJETIVO or grilla[f][c]==OBJETIVO_CAJA or grilla[f][c]==OBJETIVO_JUGADOR:
		return True
	return False

def hay_caja(grilla, c, f):
	'''Devuelve True si hay una caja en la columna y fila (c, f).'''
	if grilla[f][c]==CAJA:
		return True
	return False

def hay_caja_objetivo(grilla, c, f):
	'''Devuelve True si hay una caja con objetivo en la columna y fila (c, f).'''
	if grilla[f][c]==OBJETIVO_CAJA:
		return True
	return False

def hay_jugador(grilla, c, f):
	'''Devuelve True si el jugador está en la columna y fila (c, f).'''
	if grilla[f][c]==JUGADOR or grilla[f][c]==OBJETIVO_JUGADOR:
		return True
	return False

def juego_ganado(grilla):
	'''Devuelve True si el juego está ganado.'''
	for fila in grilla:
		for columna in fila:
			if columna==CAJA or columna==OBJETIVO or columna==OBJETIVO_JUGADOR:
				return False
	return True


def posicion_del_jugador(grilla):
	''' Devuelve una lista con la posicion del jugador'''
	for fila in range(len(grilla)):
		for columna in range(len(grilla[fila])):
			if grilla[fila][columna]==JUGADOR or grilla[fila][columna]==OBJETIVO_JUGADOR:
				posicion_jugador=[]
				posicion_jugador.append(fila)
				posicion_jugador.append(columna)
				return posicion_jugador


def suma_posicion_direccion(posicion,direccion):
	'''Devuelve la suma de la posicion donde se encuentra el jugador
	y otra la direccion en la que se mueve:
	direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur'''
	posicion_final=[]
	
	x1,y1= posicion[0],posicion[1]
	x2,y2= direccion[1],direccion[0]
	
	posicion_final.append(x1+x2)
	posicion_final.append(y1+y2)
	
	return posicion_final

def movimientos_no_permitidos(grilla,direccion):
	'''Recive una grilla, la direccion en que se efectua el movimiento y devuelve True si el movimiento no puede ser efectuado
		direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur'''
	posicion_jugador= posicion_del_jugador(grilla)
	jugador_en_grilla= grilla[posicion_jugador[0]][posicion_jugador[1]]

	posicion_siguiente= suma_posicion_direccion(posicion_jugador,direccion)
	casilla_siguiente= grilla[posicion_siguiente[0]][posicion_siguiente[1]]

	posicion_dos_adelante= suma_posicion_direccion(posicion_siguiente,direccion)

	if casilla_siguiente==PARED:
		return True

	if (casilla_siguiente==CAJA) or (casilla_siguiente==OBJETIVO_CAJA):
		dos_adelante= grilla[posicion_dos_adelante[0]][posicion_dos_adelante[1]]
		if dos_adelante==CAJA or dos_adelante==PARED or dos_adelante==OBJETIVO_CAJA:
			return True
	return False


def mover(grilla, direccion):
	'''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    el movimiento columna dsps fila
    Si la celda vecina está vacía, el movimiento está permitido
    Si la celda vecina es una pared, no esya permitido
    Si la celda vecina es una caja, puede ocurrir dos cosas
        Empuja la caja si puede hacer el movimiento
        No se puede'''

	copia_grilla= crear_grilla(grilla)

	posicion_jugador= posicion_del_jugador(copia_grilla)
	jugador_en_grilla= copia_grilla[posicion_jugador[0]][posicion_jugador[1]]

	posicion_siguiente= suma_posicion_direccion(posicion_jugador,direccion)
	casilla_siguiente= copia_grilla[posicion_siguiente[0]][posicion_siguiente[1]]

	posicion_dos_adelante= suma_posicion_direccion(posicion_siguiente,direccion)

	if movimientos_no_permitidos(copia_grilla,direccion)==True:
		return copia_grilla


	if jugador_en_grilla == JUGADOR:
		copia_grilla[posicion_jugador[0]][posicion_jugador[1]]= CELDA_VACIA
	else:
		copia_grilla[posicion_jugador[0]][posicion_jugador[1]]= OBJETIVO  

	if casilla_siguiente == OBJETIVO:
		copia_grilla[posicion_siguiente[0]][posicion_siguiente[1]]=OBJETIVO_JUGADOR
		return copia_grilla

	elif casilla_siguiente == CELDA_VACIA:
		copia_grilla[posicion_siguiente[0]][posicion_siguiente[1]]=JUGADOR
		return copia_grilla

	
	elif (casilla_siguiente == OBJETIVO_CAJA) or (casilla_siguiente == CAJA):
		
		dos_adelante= copia_grilla[posicion_dos_adelante[0]][posicion_dos_adelante[1]]
		
		if casilla_siguiente == OBJETIVO_CAJA:
			copia_grilla[posicion_siguiente[0]][posicion_siguiente[1]]=OBJETIVO_JUGADOR
		else:
			copia_grilla[posicion_siguiente[0]][posicion_siguiente[1]]=JUGADOR

		if dos_adelante == CELDA_VACIA:
			copia_grilla[posicion_dos_adelante[0]][posicion_dos_adelante[1]]=CAJA
			return copia_grilla

		elif dos_adelante == OBJETIVO:
			copia_grilla[posicion_dos_adelante[0]][posicion_dos_adelante[1]]=OBJETIVO_CAJA
			return copia_grilla