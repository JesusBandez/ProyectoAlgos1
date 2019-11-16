def cambiarJugador(turno) -> int:
	if turno == 0:
		turno = 1
	elif turno ==1:
		turno = 0
	return turno

def consumo(tablero, fila, columna, turno) -> [[int]]:
	consumidas = []
	for i in [[-1,0], [1,0], [0,1], [0,-1], [-1,-1], [-1,1], [1,1], [1,-1]]:
		j, posibles_consumidas, vecino, fin_de_linea = 1, [], True, False
		while j < 8 and vecino and not fin_de_linea:		 
			if j == 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] != 2 - turno:
				vecino = False
			elif j >= 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 2 - turno:
				posibles_consumidas.append([fila + j*i[0],columna + j*i[1]])			
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == turno + 1:
				consumidas = consumidas + posibles_consumidas				
				fin_de_linea = True
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 0:
				fin_de_linea = True
			j = j+1	
	for i in consumidas:
		tablero[i[0]][i[1]] = turno+1
	return tablero
	""" Teniendo en cuenta que hay que demostrar esta funcion, tal vez habrá que cambiarla. Ademas, se tiene que este subprograma
	debe separarse en otros tres subprogramas (consumoVertical,consumoHorizontal y consumoDiagonal) sin embargo, la idea de esto es tener adelantado
	parte de la lógica """


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
	# Casilla no esta ocupada por una ficha
	if tablero[fila][columna] == 0:
		casillaValida = True
	elif tablero[fila][columna] != 0:
		casillaValida = False
	# Comprueba la jugada en todas las direcciones
	cambiadas = 0
	for i in [[-1,0], [1,0], [0,1], [0,-1], [-1,-1], [-1,1], [1,1], [1,-1]]:
		j, vecino, contador, flanqueada = 1, True, 0, False 
		while j < 8 and vecino and not flanqueada: 
			if j == 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] != 2 - turno:
				vecino = False
			elif j == 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 2 - turno:
				contador = contador + 1
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == turno + 1:
				flanqueada = True
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 2-turno:
				contador = contador + 1
			j = j + 1
		if flanqueada:
			cambiadas = cambiadas + contador
		elif not flanqueada:
			pass
		
	# Comprueba si hubieron fichas que cambiaron de color
	if cambiadas == 0:
		cambio = False
	elif cambiadas > 0:
		cambio = True

	# Comprueba que la jugada sea valida
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
		tablero = consumo(tablero, jugada[0], jugada[1], turno)
		dibujarJugada(tablero, jugada[0], jugada[1], turno)
		turno = cambiarJugador(turno)
	elif not esValida(tablero,jugada[0], jugada[1], turno):
		print("Jugada invalida, prueba otra vez\n")


	
