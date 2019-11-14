def cambiarJugador(turno) -> int:
	if turno == 0:
		turno = 1
	elif turno ==1:
		turno = 0
	return turno

def dibujarJugada(tablero, fila, columna, turno) -> "void": # Debe entregrase el martes!!!!!!
	# Precondicion
	assert(0 <= fila < 8 and 0 <= columna < 8)
	tablero[fila][columna] = turno+1
	# Post condicion
	assert(tablero[fila][columna] == turno+1)
	# ///////////////// Interfaz temporal
	for i in tablero:
		print(i)
	# \\\\\\\\\\\\\\\\\\

def inicializarTablero() -> [[int]]: # Debe entregrase el martes!!!!!!
	# Precondicion
	assert(True)
	tablero = [[0 for i in range(0,8)] for i in range(0,8)]
	tablero[3][3],tablero[4][4] = 1, 1
	tablero[3][4],tablero[4][3] = 2, 2
	# Post condicion
	assert(all(all(tablero[i][j] == 0 for i in range(0,8) if i != 3 and i != 4) for j in range(0,8)))	
	# ///////////////// 
	for i in tablero:
		print(i)
	# \\\\\\\\\\\\\\\\\\
	return tablero

def esValida(tablero, fila, columna, turno) -> bool: 
	# Casilla no es distinta de vacia
	if tablero[fila][columna] == 0:
		casillaValida = True
	elif tablero[fila][columna] != 0:
		casillaValida = False
	# Comprueba en todas direcciones
	cambiadas = 0
	i, vecino, contador, flanqueada = 1, True, 0, False # Comprueba hacia arriba
	while i < 8 and vecino and not flanqueada: 
		if i == 1 and 0 <= fila-i < 8 and tablero[fila-i][columna] != 2 - turno :
			vecino = False
		elif i == 1 and 0 <= fila-i < 8 and tablero[fila-i][columna] == 2 - turno:
			contador = contador + 1
		elif i > 1 and 0 <= fila-i < 8 and tablero[fila-i][columna] == turno + 1:
			flanqueada = True
		elif i > 1 and 0 <= fila-i < 8 and tablero[fila-i][columna] == 2-turno:
			contador = contador + 1
		i = i + 1
	if flanqueada:
		cambiadas = cambiadas + contador
	elif not flanqueada:
		pass
	

	i, vecino, contador, flanqueada = 1, True, 0, False # Comprueba hacia abajo
	while i < 8 and vecino and not flanqueada: 
		if i == 1 and 0 <= fila+i < 8 and tablero[fila+i][columna] != 2 - turno :
			vecino = False
		elif i == 1 and 0 <= fila+i < 8 and tablero[fila+i][columna] == 2 - turno:
			contador = contador + 1
		elif i > 1 and 0 <= fila+i < 8 and tablero[fila+i][columna] == turno + 1:
			flanqueada = True
		elif i > 1 and 0 <= fila+i < 8 and tablero[fila+i][columna] == 2-turno:
			contador = contador + 1
		i = i + 1
	if flanqueada:
		cambiadas = cambiadas + contador
	elif not flanqueada:
		pass
	

	i, vecino, contador, flanqueada = 1, True, 0, False # Comprueba hacia la derecha
	while i < 8 and vecino and not flanqueada: 
		if i == 1 and 0 <= columna+i < 8 and tablero[fila][columna+i] != 2 - turno :
			vecino = False
		elif i == 1 and 0 <= columna+i < 8 and tablero[fila][columna+i] == 2 - turno:
			contador = contador + 1
		elif i > 1 and 0 <= columna+i < 8 and tablero[fila][columna+i] == turno + 1:
			flanqueada = True
		elif i > 1 and 0 <= columna+i < 8 and tablero[fila][columna+i] == 2-turno:
			contador = contador + 1
		i = i + 1
	if flanqueada:
		cambiadas = cambiadas + contador
	elif not flanqueada:
		pass
	

	i, vecino, contador, flanqueada = 1, True, 0, False # Comprueba hacia la izquierda
	while i < 8 and vecino and not flanqueada: 
		if i == 1 and 0 <= columna-i < 8 and tablero[fila][columna-i] != 2 - turno :
			vecino = False
		elif i == 1 and 0 <= columna-i < 8 and tablero[fila][columna-i] == 2 - turno:
			contador = contador + 1
		elif i > 1 and 0 <= columna-i < 8 and tablero[fila][columna-i] == turno + 1:
			flanqueada = True
		elif i > 1 and 0 <= columna-i < 8 and tablero[fila][columna-i] == 2-turno:
			contador = contador + 1
		i = i + 1
	if flanqueada:
		cambiadas = cambiadas + contador
	elif not flanqueada:
		pass
	

	i, vecino, contador, flanqueada = 1, True, 0, False # Comprueba hacia diagonal arriba-izquierda
	while i < 8 and vecino and not flanqueada: 
		if i == 1 and 0 <= fila-i < 8 and 0 <= columna-i < 8 and tablero[fila-i][columna-i] != 2 - turno :
			vecino = False
		elif i == 1 and 0 <= fila-i < 8 and 0 <= columna-i < 8 and tablero[fila-i][columna-i] == 2 - turno:
			contador = contador + 1
		elif i > 1 and 0 <= fila-i < 8 and 0 <= columna-i < 8 and tablero[fila-i][columna-i] == turno + 1:
			flanqueada = True
		elif i > 1 and 0 <= fila-i < 8 and 0 <= columna-i < 8 and tablero[fila-i][columna-i] == 2-turno:
			contador = contador + 1
		i = i + 1
	if flanqueada:
		cambiadas = cambiadas + contador
	elif not flanqueada:
		pass
	

	i, vecino, contador, flanqueada = 1, True, 0, False # Comprueba hacia diagonal arriba-derecha
	while i < 8 and vecino and not flanqueada: 
		if i == 1 and 0 <= fila-i < 8 and 0 <= columna+i < 8 and tablero[fila-i][columna+i] != 2 - turno :
			vecino = False
		elif i == 1 and 0 <= fila-i < 8 and 0 <= columna+i < 8 and tablero[fila-i][columna+i] == 2 - turno:
			contador = contador + 1
		elif i > 1 and 0 <= fila-i < 8 and 0 <= columna+i < 8 and tablero[fila-i][columna+i] == turno + 1:
			flanqueada = True
		elif i > 1 and 0 <= fila-i < 8 and 0 <= columna+i < 8 and tablero[fila-i][columna+i] == 2-turno:
			contador = contador + 1
		i = i + 1
	if flanqueada:
		cambiadas = cambiadas + contador
	elif not flanqueada:
		pass
	

	i, vecino, contador, flanqueada = 1, True, 0, False # Comprueba hacia diagonal abajo-derecha
	while i < 8 and vecino and not flanqueada: 
		if i == 1 and 0 <= fila+i < 8 and 0 <= columna+i < 8 and tablero[fila+i][columna+i] != 2 - turno :
			vecino = False
		elif i == 1 and 0 <= fila+i < 8 and 0 <= columna+i < 8 and tablero[fila+i][columna+i] == 2 - turno:
			contador = contador + 1
		elif i > 1 and 0 <= fila+i < 8 and 0 <= columna+i < 8 and tablero[fila+i][columna+i] == turno + 1:
			flanqueada = True
		elif i > 1 and 0 <= fila+i < 8 and 0 <= columna+i < 8 and tablero[fila+i][columna+i] == 2-turno:
			contador = contador + 1
		i = i + 1
	if flanqueada:
		cambiadas = cambiadas + contador
	elif not flanqueada:
		pass
	

	i, vecino, contador, flanqueada = 1, True, 0, False # Comprueba hacia diagonal abajo-izquierda
	while i < 8 and vecino and not flanqueada: 
		if i == 1 and 0 <= fila+i < 8 and 0 <= columna-i < 8 and tablero[fila+i][columna-i] != 2 - turno :
			vecino = False
		elif i == 1 and 0 <= fila+i < 8 and 0 <= columna-i < 8 and tablero[fila+i][columna-i] == 2 - turno:
			contador = contador + 1
		elif i > 1 and 0 <= fila+i < 8 and 0 <= columna-i < 8 and tablero[fila+i][columna-i] == turno + 1:
			flanqueada = True
		elif i > 1 and 0 <= fila+i < 8 and 0 <= columna-i < 8 and tablero[fila+i][columna-i] == 2-turno:
			contador = contador + 1
		i = i + 1
	if flanqueada:
		cambiadas = cambiadas + contador
	elif not flanqueada:
		pass
	
	# Comprueba si hubieron fichas que cambiaron de color
	if cambiadas == 0:
		cambio = False
	elif cambiadas > 0:
		cambio = True

	# Comprobacion final
	if cambio and casillaValida:
		esvalida = True
	elif not cambio or not casillaValida:
		esvalida = False

	return esvalida


def obtenerJugada() -> [int]:  # Debe entregrase el martes!!!!!!
	assert(True)
	while True:
		# ////////////////
		fila = int(input("¿En qué fila desea jugar (" + str(turno+1) + ")?")) 
		columna = int(input("¿En qué columna desea jugar (" + str(turno+1) + ")?"))
		# \\\\\\\\\\\\\\\\\\
		jugada = [fila, columna]
		try: # ¿Como afecta esto a la demostracion?
			assert(0 <= fila < 8 and 0 <= columna < 8)
			break
		except:
			print("Ingrese una coordenada válida")
	return jugada

def otraPartida() -> bool:
	print("¿Quieren jugar otra partida?:")
	respuesta = ""
	while respuesta != "si" and respuesta != "no":
		respuesta = input()
	return respuesta


	



# "Aproximacion de como deber ser el programa"
"""
turno = 0
otro = True
while otro:
	while quedanFichas:
		obtenerJugada(fila,columna) ¿Para qué el fil y el col como entrada?
		if esValida(tablero, fila, columna):
			consumo(tablero, fila, columna, turno)
			dibujarJugada(tablero, fila, columna, turno)
			cambiarJugador(turno)
		elif not esValida(tablero, fila, columna):
			error()
		resultado()
	otro = otraPartida()
"""

# Pruebas

turno = 0
tablero = inicializarTablero()
while True:
	jugada = obtenerJugada()	
	if esValida(tablero, jugada[0], jugada[1], turno):
		dibujarJugada(tablero, jugada[0], jugada[1], turno)
		turno = cambiarJugador(turno)
	elif not esValida(tablero,jugada[0], jugada[1], turno):
		print("Jugada invalida, prueba otra vez")


	
