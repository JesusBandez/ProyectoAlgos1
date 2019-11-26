import pygame
from pygame.locals import *
from sys import exit
from time import sleep
from random import randint

# Funciones lógicas
def cambiarJugador(turno:int, jugador_de_turno:int,) -> int: # Cambia el turno y al jugador en turno 
	if turno == 0:
		turno = 1
	elif turno ==1:
		turno = 0
	if jugador_de_turno == 0:
		jugador_de_turno = 1
	elif jugador_de_turno == 1:
		jugador_de_turno = 0
	return turno, jugador_de_turno 

def consumo(tablero:[[int]], fila:int, columna:int, turno:int) -> [[int]]: # Cambia las fichas de color al ser flanqueadas 
	consumidas = []
	for i in [[-1,0], [1,0], [0,1], [0,-1], [-1,-1], [-1,1], [1,1], [1,-1]]:
		j, posibles_consumidas, fin_de_linea = 1, [], False
		while j < 8 and not fin_de_linea:			
			if 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 2 - turno:
				posibles_consumidas.append([fila + j*i[0],columna + j*i[1]])			
			elif  0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == turno + 1:
				consumidas = consumidas + posibles_consumidas				
				fin_de_linea = True
			elif  0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 0:
				fin_de_linea = True
			j = j+1	
	for i in consumidas:
		tablero[i[0]][i[1]] = turno + 1
	return tablero
	""" Teniendo en cuenta que hay que demostrar esta funcion, tal vez habrá que cambiarla. Ademas, se tiene que este subprograma
	debe separarse en otros tres subprogramas (consumoVertical,consumoHorizontal y consumoDiagonal) sin embargo, la idea de esto es tener adelantado
	parte de la lógica """ 

def dibujarJugada(tablero:[[int]], fila:int, columna:int, turno:int) -> "void": # Dibuja la última jugada válida 
	# Precondicion
	assert(0 <= fila < 8 and 0 <= columna < 8 and 0 <= turno < 2)
	tablero[fila][columna] = turno+1
	dibujarFichas(tablero)
	# Post condicion
	assert(tablero[fila][columna] == turno+1)  
	
def inicializarTablero() -> [[int]]: # Prepara la matriz 
	tablero = [[0 for i in range(0,8)] for i in range(0,8)]
	# Precondicion
	assert(all(all(tablero[i][j] == 0 for i in range(0,8)) for j in range(0,8)))
	tablero[3][3],tablero[4][4] = 1, 1
	tablero[3][4],tablero[4][3] = 2, 2
	ventana.blit(fondo, (0,0))
	dibujarFichas(tablero)
	resultadoParcial(tablero)
	# Post condicion
	assert(all(all(tablero[i][j] == 0 for i in range(0,8) if i != 3 and i != 4) for j in range(0,8)))	
	return tablero

def esValida(tablero:[[int]], fila:int, columna:int, turno:int) -> bool: # Indica si una jugada es válida 
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

def obtenerJugada() -> [int]: # Recibe las coordenadas del mouse y las transforma en subíndices de la matriz 
	coordenadas = (0,0)
	while coordenadas == (0,0):
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			elif event.type == pygame.MOUSEBUTTONUP:				
				coordenadas = pygame.mouse.get_pos()
				if 205 <= coordenadas[0] <= 605 and 56 <= coordenadas[1] <= 456:
					pass
				else:
					coordenadas = (0,0)					
	i = 0
	while i < 8:
		j = 0
		while j < 8:
			if 205 + 50*j <= coordenadas[0] <= 205 + 50*(j+1) and 56 + 50*i <= coordenadas[1] <= 56 + 50*(i+1):
				jugada = [i,j]
			else:
				pass
			j = j+1
		i = i+1
	# Post condicion
	assert(0 <= jugada[0] < 8 and 0 <= jugada[1] < 8)
	return jugada 

def otraPartida() -> bool: # Pregunta si se quiere jugar otra partida
	print("¿Quieren jugar otra partida?:")
	respuesta = ""
	while respuesta != "si" and respuesta != "no":
		respuesta = input()
	return respuesta 

def quedanFichas(tablero:[[int]]) -> bool: # Indica si aún quedan espacios vacíos en el tablero
	i, quedan = 0, False
	while i < 8 and not quedan:
		j = 0
		while j < 8 and not quedan:
			if tablero[i][j] == 0:
				quedan = True
			j = j + 1
		i = i + 1
	return quedan 

def puedeJugar(tablero:[[int]], turno:int) -> bool: # Evalúa si el turno puede hacer al menos una jugada válida
	fila, puede = 0, False 
	while fila < 8 and not puede:
		columna = 0
		while columna < 8 and not puede:
			if tablero[fila][columna] == turno+1:
				for i in [[-1,0], [1,0], [0,1], [0,-1], [-1,-1], [-1,1], [1,1], [1,-1]]:
					k, vecino, fin_de_linea = 1, True, False
					while k < 8 and vecino and not puede and not fin_de_linea:
						if k == 1 and 0 <= fila + k*i[0] < 8 and 0 <= columna + k*i[1] < 8 and tablero[fila + k*i[0]][columna + k*i[1]] != 2 - turno:
							vecino = False							
						elif k == 1 and 0 <= fila + k*i[0] < 8 and 0 <= columna + k*i[1] < 8 and tablero[fila + k*i[0]][columna + k*i[1]] == 2 - turno:
							pass
						elif k > 1 and 0 <= fila + k*i[0] < 8 and 0 <= columna + k*i[1] < 8 and tablero[fila + k*i[0]][columna + k*i[1]] == 0:
							puede = True
						elif k > 1 and 0 <= fila + k*i[0] < 8 and 0 <= columna + k*i[1] < 8 and tablero[fila + k*i[0]][columna + k*i[1]] == turno+1:
							fin_de_linea = True							
						k = k+1

			columna = columna + 1
		fila = fila + 1	
	return puede 

# Funciones para la interfaz
def dibujarFichas(tablero:[[int]]) -> "void": # Dibuja las fichas sobre el tablero 
	i = 0
	while i < 8:
		j = 0
		while j < 8:
			if tablero[i][j] == 0:
				pass
			elif tablero[i][j] == 1:
				ventana.blit(fichaBlanca,(205 + 50*j, 56 + 50*i))
			elif tablero[i][j] == 2:
				ventana.blit(fichaNegra,(205 + 50*j, 56 + 50*i))
			j = j+1
		i = i+1
	pygame.display.flip() # Dibuja las fichas en la ventana 

def nombresPuntaje(jugador_de_turno:int) -> "void": # Dibuja nombres sobre las fichas
	if jugador_de_turno == 0:
		texto = nombreJugador1
		mensaje = fuente_peq.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (630,420))
		texto = nombreJugador2
		mensaje = fuente_peq.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (30, 420))
	elif jugador_de_turno == 1:
		texto = nombreJugador2
		mensaje = fuente_peq.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (630,420))
		texto = nombreJugador1
		mensaje = fuente_peq.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (30, 420))
	pygame.display.flip()

def quienJuega(jugador_de_turno: int) -> "void": # Mensaje de a quien le toca jugar
	if jugador_de_turno == 0: 
		texto = "Ingrese jugada " + str(nombreJugador1)
	elif jugador_de_turno == 1:
		texto = "Ingrese jugada " + str(nombreJugador2)
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(tablon, (180,460))
	ventana.blit(mensaje, (180,460))
	pygame.display.flip()

def error(turno:int) -> "void": # Mensaje de jugada inválida 
	texto = "Jugada inválida"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(tablon, (180,460))
	ventana.blit(mensaje, (180,460))
	pygame.display.flip()
	sleep(1.1) 

def resultadoParcial(tablero:[[int]]) -> "void": # Imprime la cantidad de fichas de cada color en el tablero
	i , fichasB, fichasN = 0, 0, 0
	while i < 8:
		j = 0
		while j < 8:
			if tablero[i][j] == 0:
				pass
			elif tablero[i][j] == 1:
				fichasB = fichasB + 1
			elif tablero[i][j] == 2:
				fichasN = fichasN + 1
			j = j+1
		i = i+1
	ventana.blit(fichaBlancaContador, (50, 460)) 
	ventana.blit(fichaNegraContador, (650, 460))
	textoFichasB = str(fichasB)
	textoFichasN = str(fichasN)
	mensajeFichasB = fuente_peq.render(textoFichasB, 1, (100,100,100))
	mensajeFichasN = fuente_peq.render(textoFichasN, 1, (125,125,125))
	ventana.blit(mensajeFichasB, (85, 480))
	ventana.blit(mensajeFichasN, (685,480))
	pygame.display.flip()

def escribir(caracteres:[str] ,jugador:int) -> "void": # Escribe los nombres a tiempo real cuando se piden 
	ventana.blit(tabla, (0,0))
	texto = "Ingrese su nombre jugador " + str(jugador) + ":"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (150, 200))
	pygame.display.flip()
	mensaje = str(caracteres)
	mensaje = fuente_peq.render(mensaje, 1, (0,0,0))
	ventana.blit(mensaje, (200,260))
	pygame.display.flip()

def pedirNombre(jugador:int) -> str: # Permite a los jugadores escribir su nombre
	caracteres = ""
	asignado = ""
	while asignado == "":
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_BACKSPACE:
					caracteres = caracteres[0:len(caracteres)-1]
				elif event.key == K_RETURN:
					asignado = caracteres				
				elif event.key == K_SPACE or len(caracteres) > 7:
					pass
				else:						
					caracteres = caracteres + event.unicode
			escribir(caracteres, jugador)
	return caracteres

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
# Inicializacion
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Reversi")

# Fuentes
fuente = pygame.font.Font("BOOKOS.ttf", 40)
fuente_peq = pygame.font.Font("BOOKOS.ttf", 35)
# Cargar y modificar imagenes
fondo = pygame.image.load("Tablero.png").convert()
fichaBlanca = pygame.image.load("Ficha_Blanca.png").convert_alpha()
fichaNegra = pygame.image.load("Ficha_Negra.png").convert_alpha()
tablon = pygame.image.load("Tablon.png")
tabla = pygame.image.load("Tabla.jpg")
fichaBlancaContador = pygame.transform.scale(fichaBlanca, (90,90))
fichaNegraContador = pygame.transform.scale(fichaNegra, (90,90))

# Nombres de jugadores
nombreJugador1 = pedirNombre(1)
nombreJugador2 = pedirNombre(2)

# Juego
jugar_otra = "si"
while True:
	while jugar_otra != "no":
		turno = 1
		cambios_de_turno = 0
		jugador_en_turno = randint(0,1)
		tablero = inicializarTablero()
		nombresPuntaje(jugador_en_turno)
		while quedanFichas(tablero) and cambios_de_turno != 2:
			cambios_de_turno = 0
			while not puedeJugar(tablero, turno) and cambios_de_turno != 2:
				turno, jugador_en_turno = cambiarJugador(turno, jugador_en_turno)
				cambios_de_turno = cambios_de_turno + 1
				print("No puede jugar, se cambio el turno")	
			if cambios_de_turno == 2:
				print("Ninguno de los jugadores puede jugar")
				break
			quienJuega(jugador_en_turno)
			jugada = obtenerJugada()	
			if esValida(tablero, jugada[0], jugada[1], turno):
				tablero = consumo(tablero, jugada[0], jugada[1], turno)
				dibujarJugada(tablero, jugada[0], jugada[1], turno)
				turno, jugador_en_turno = cambiarJugador(turno, jugador_en_turno)
			elif not esValida(tablero,jugada[0], jugada[1], turno):
				error(turno)
			resultadoParcial(tablero)
		print("Mensaje de Victoria")
		jugar_otra = input("¿Quieren jugar otra?").lower()
	print("bye")
	break

""" Cosas por hacer:
Logica:
- Comprobar que los jugadores quieran jugar una nueva partida
Interfaz:
- Agregar mensajes:
Al saltar el turno de un jugador
Al acabar el juego por no poder jugar
Mensaje de Victoria
Al pedir una nueva partida
"""