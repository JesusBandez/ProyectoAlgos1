# Un juego de Reversi
# Autor: Jesús Bandez

import pygame
from pygame.locals import *
from sys import exit
from time import sleep
from random import randint

# Funciones lógicas
def cambiarJugador(turno:int) -> int: # Cambia el turno 
	# Precondicion
	assert(0 <= turno < 2)
	if turno == 0:
		cambio = 1
	elif turno ==1:
		cambio = 0
	# Postcondicion
	assert((turno == 0 and cambio == 1) 
		or (turno == 1 and cambio == 0))
	return cambio

def consumo(tablero:[[int]], fila:int, columna:int, turno:int) -> "void": # Cambia las fichas de color al ser flanqueadas 
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
	
def dibujarJugada(tablero:[[int]], fila:int, columna:int, turno:int) -> "void": # Dibuja la última jugada válida 
	# Precondicion
	assert(0 <= fila < 8 and 0 <= columna < 8 and 0 <= turno < 2)
	tablero[fila][columna] = turno+1
	dibujarFichas(tablero)
	# Post condicion
	assert(tablero[fila][columna] == turno+1)  
	
def inicializarTablero() -> [[int]]: # Prepara la matriz 
	# Precondicion
	assert(True)
	tablero = [[0 for i in range(0,8)] for i in range(0,8)]
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
		j, fin_de_linea, contador, flanqueada = 1, False, 0, False 
		while j < 8 and not fin_de_linea and not flanqueada: 
			if j == 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] != 2 - turno:
				fin_de_linea = True
			elif j >= 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 2 - turno:
				contador = contador + 1
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == turno + 1:
				flanqueada = True			
			elif j > 1 and 0 <= fila + j*i[0] < 8 and 0 <= columna + j*i[1] < 8 and tablero[fila + j*i[0]][columna + j*i[1]] == 0:
				fin_de_linea = True
			j = j + 1
		if flanqueada:
			cambiadas = cambiadas + contador
		elif not flanqueada:
			pass	

	# Comprueba que la jugada sea valida
	if cambiadas != 0 and casillaValida:
		esvalida = True
	elif cambiadas == 0 or not casillaValida:
		esvalida = False

	return esvalida

def obtenerJugada() -> [int]: # Recibe las coordenadas del mouse y las transforma en subíndices de la matriz 
	# Precondicion
	assert(True)
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
			j = j+1
		i = i+1
	# Post condicion
	assert(0 <= jugada[0] < 8 and 0 <= jugada[1] < 8)
	return jugada 

def quedanFichas(tablero:[[int]]) -> bool: # Indica si aún quedan espacios vacíos en el tablero
	# Precondicion
	assert(True)
	i, quedan = 0, False
	while i < 8 and not quedan:
		j = 0
		while j < 8 and not quedan:
			if tablero[i][j] == 0:
				quedan = True
			j = j + 1
		i = i + 1
	# Postcondicion
	assert(quedan == any(any(tablero[i][j]==0 for i in range(0,8)) for j in range(0,8)))
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

def nombresPuntaje(jugador_de_turno:int, nombreJugador1:str, nombreJugador2:str) -> [str]: # Dibuja los nombres sobre las fichas 
# y retorna quienes son las negras y las blancas
	if jugador_de_turno == 0:
		texto = nombreJugador1
		mensaje = fuente_peq.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (630,420))
		negras = nombreJugador1
		texto = nombreJugador2
		mensaje = fuente_peq.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (30, 420))
		blancas = nombreJugador2
	elif jugador_de_turno == 1:
		texto = nombreJugador2
		mensaje = fuente_peq.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (630,420))
		negras = nombreJugador2
		texto = nombreJugador1
		mensaje = fuente_peq.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (30, 420))
		blancas = nombreJugador1
	pygame.display.flip()
	return [negras, blancas]

def quienJuega(turno:int, orden:[str]) -> "void": # Mensaje de a quien le toca jugar
	if turno == 0: 
		texto = "Ingrese jugada " + str(orden[1])
	elif turno == 1:
		texto = "Ingrese jugada " + str(orden[0])
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(tablon, (180,460))
	ventana.blit(mensaje, (180,460))
	pygame.display.flip()

def error() -> "void": # Mensaje de jugada inválida 
	texto = "Jugada inválida"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(tablon, (180,460))
	ventana.blit(mensaje, (180,460))
	pygame.display.flip()
	sleep(0.8) 

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
	mensajeFichasB = fuente_peq.render(textoFichasB, 1, (40,40,40))
	mensajeFichasN = fuente_peq.render(textoFichasN, 1, (215,215,215))
	ventana.blit(mensajeFichasB, (82, 480))
	ventana.blit(mensajeFichasN, (682,480))
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
	if len(caracteres) > 0:
		texto = "Pulse enter para continuar"
		mensaje = fuente_peq.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (200, 560))
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
				elif event.key == K_SPACE or len(caracteres) > 6:
					pass
				else:						
					caracteres = caracteres + event.unicode
			elif event.type == QUIT:
				exit()
			escribir(caracteres, jugador)
	return caracteres

def jugarOtra() -> str: # Dice si los jugadores quieren jugar otra partida
	mensajeJugarOtra()
	coordenadas = (0,0)
	while coordenadas == (0,0):
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			elif event.type == pygame.MOUSEBUTTONUP:				
				coordenadas = pygame.mouse.get_pos()
				if 250 <= coordenadas[0] <= 285 and 300 <= coordenadas[1] <= 340:
					jugar_otra = "sí"
				elif 450 <= coordenadas[0] <= 500 and 300 <= coordenadas[1] <= 340:
					jugar_otra = "no"
				else:
					coordenadas = (0,0)
	return jugar_otra									 

def mensajeJugarOtra() -> "void": # Pregunta en la interfaz si se quiere jugar otra vez
	ventana.blit(tabla, (0,0))
	texto = "¿Quieren jugar otra partida?"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (150,200))
	texto = "Sí"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (250,300))
	texto = "No"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (450,300))
	pygame.display.flip()

def mensajeVictoria(tablero:[[int]], orden:[int]) -> "void": # Muestra un mensaje de quien ha ganado la partida
	i, negras, blancas = 0, 0, 0
	while i < 8:
		j = 0
		while j < 8:
			if tablero[i][j] == 1:
				blancas = blancas + 1
			elif tablero[i][j] == 2:
				negras = negras + 1
			j = j + 1
		i = i + 1

	sleep(0.8)
	ventana.blit(tablon, (180,460))
	if negras > blancas:
		texto = "¡Has ganado " + str(orden[0]) + "!"
		mensaje = fuente.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (180, 460))
	elif blancas > negras:
		texto = "¡Has ganado " + str(orden[1]) + "!"
		mensaje = fuente.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (180, 460))
	elif blancas == negras:
		texto = "¡Empate!"
		mensaje = fuente.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (180, 460))
	pygame.display.flip()
	sleep(2.8) 

def mensajeSaltoDeTurno(orden:[str], turno:int) -> "void": # Muestra un mensaje de a quien se la ha saltado el turno
	ventana.blit(tablon, (180,460))
	if turno == 0:
		texto = orden[1] + " no puede jugar"
		mensaje = fuente.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (180, 460))
		texto = "Se saltará su turno"
		mensaje = fuente.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (180, 500))
	elif turno == 1:
		texto = orden[0] + " no puede jugar"
		mensaje = fuente.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (180, 460))
		texto = "Se saltará su turno"
		mensaje = fuente.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (180, 500))
	pygame.display.flip()
	sleep(1.5)

def mensajeDosSaltosDeTurno() -> "void": # Advierte que se acabará la partida porque nadie pude jugar
	ventana.blit(tablon, (180,460))
	texto = "Dos saltos consecutivos"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (180, 460))
	texto = "La partida se ha acabado"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (180, 500))
	pygame.display.flip()
	sleep(1.5)

def despedida() -> "void": # Mensaje de despedida
	ventana.blit(tabla, (0,0))
	texto = "¡Muchas gracias por jugar!"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (180, 260))
	texto = "Autor:"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (180, 300))
	texto = "Jesus \"Krooz\" Bandez"
	mensaje = fuente_despedida.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (180, 345))
	pygame.display.flip()
	sleep(3)

def bienvenida() -> "void": # Mensaje de bienvenida
	ventana.blit(tabla, (0,0))
	texto = "Reversi"
	mensaje = fuente_bienvenida.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (50, 200))
	texto = "Pulsa click"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (350, 450))
	pygame.display.flip()	
	texto = ""
	while texto == "":
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				texto = "a"
			elif event.type == QUIT:
				exit()

# Inicializacion
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Reversi")

# Fuentes
fuente = pygame.font.Font("BOOKOS.ttf", 40)
fuente_peq = pygame.font.Font("BOOKOS.ttf", 35)
fuente_bienvenida = pygame.font.Font("Triforce.ttf", 260)
fuente_despedida = pygame.font.Font("Triforce.ttf", 55)

# Cargar y modificar imagenes
fondo = pygame.image.load("Tablero.png").convert()
fichaBlanca = pygame.image.load("Ficha_Blanca.png").convert_alpha()
fichaNegra = pygame.image.load("Ficha_Negra.png").convert_alpha()
tablon = pygame.image.load("Tablon.png")
tabla = pygame.image.load("Tabla.jpg")
fichaBlancaContador = pygame.transform.smoothscale(fichaBlanca, (90,90))
fichaNegraContador = pygame.transform.smoothscale(fichaNegra, (90,90))

# Juego

bienvenida()
nombreJugador1 = pedirNombre(1)
nombreJugador2 = pedirNombre(2)
jugar_otra = "sí"
while jugar_otra != "no":
	turno, cambios_de_turno = 1, 0	
	jugador_en_turno = randint(0,1)
	tablero = inicializarTablero()
	orden = nombresPuntaje(jugador_en_turno, nombreJugador1, nombreJugador2)

	while quedanFichas(tablero) and cambios_de_turno != 2:
		cambios_de_turno = 0

		while not puedeJugar(tablero, turno) and cambios_de_turno != 2:
			mensajeSaltoDeTurno(orden, turno)
			turno = cambiarJugador(turno)
			cambios_de_turno = cambios_de_turno + 1

		if cambios_de_turno == 2:
			mensajeDosSaltosDeTurno()
			break

		quienJuega(turno, orden)
		jugada = obtenerJugada()

		if esValida(tablero, jugada[0], jugada[1], turno):
			consumo(tablero, jugada[0], jugada[1], turno)
			dibujarJugada(tablero, jugada[0], jugada[1], turno)
			turno = cambiarJugador(turno)

		elif not esValida(tablero,jugada[0], jugada[1], turno):
			error()

		resultadoParcial(tablero)

	mensajeVictoria(tablero, orden)		
	jugar_otra = jugarOtra()

despedida()