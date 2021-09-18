# Un juego de Reversi
# Autor: Jesús Bandez

import pygame
from pygame.locals import *
from sys import exit
from random import randint

# Funciones lógicas
def cambiarJugador(turno:int) -> int:
	" Cambia el turno del jugador."

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

def consumo(
	tablero:[[int]], fila:int,
	columna:int, turno:int) -> "void":
	"Cambia las fichas de color al ser flanqueadas."

	consumidas = []
	for i in [[-1,0], [1,0], [0,1], [0,-1], [-1,-1], [-1,1], [1,1], [1,-1]]:
		j, posibles_consumidas, fin_de_linea = 1, [], False
		while j < 8 and not fin_de_linea:
			vertical = fila + j*i[0]
			horizontal = columna + j*i[1]
			if (0 <= vertical < 8 and 0 <= horizontal < 8 and 
					tablero[vertical][horizontal] == 2-turno):
				posibles_consumidas.append([vertical,horizontal])			
			elif  (0 <= vertical < 8 and 0 <= horizontal < 8 and 
					tablero[vertical][horizontal] == turno+1):
				consumidas = consumidas + posibles_consumidas				
				fin_de_linea = True
			elif  (0 <= vertical < 8 and 0 <= horizontal < 8 and 
					tablero[vertical][horizontal] == 0):
				fin_de_linea = True
			j = j+1

	for i in consumidas:
		tablero[i[0]][i[1]] = turno + 1	
	
def dibujarJugada(
	tablero:[[int]], fila:int, 
	columna:int, turno:int) -> "void":
	"Dibuja la última jugada válida "

	# Precondicion
	assert(0 <= fila < 8 and 0 <= columna < 8 and 0 <= turno < 2)
	tablero[fila][columna] = turno+1
	dibujarFichas(tablero)
	# Post condicion
	assert(tablero[fila][columna] == turno+1)  
	
def inicializarTablero() -> [[int]]:
	"Inicializa la matriz de juego"

	global boton_salir
	# Precondicion
	assert(True)
	tablero = [[0 for i in range(0,8)] for i in range(0,8)]
	tablero[3][3],tablero[4][4] = 1, 1
	tablero[3][4],tablero[4][3] = 2, 2
	ventana.blit(fondo, (0,0))
	mensaje = fuente.render("Salir", 1, (0,0,0))
	boton_salir = ventana.blit(mensaje, (700, 15))
	dibujarFichas(tablero)
	resultadoParcial(tablero)
	
	
	# Post condicion
	assert(all(all(tablero[i][j] == 0 for i in range(0,8) 
		if i != 3 and i != 4) for j in range(0,8)))	
	return tablero

def esValida(
	tablero:[[int]], fila:int, 
	columna:int, turno:int) -> bool: 
	"Indica si una jugada es válida"

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
			vertical = fila + j*i[0]
			horizontal = columna + j*i[1]
			if (j == 1 and 0 <= vertical < 8 and 0 <= horizontal < 8 and 
					tablero[vertical][horizontal] != 2-turno):
				fin_de_linea = True
			elif (j >= 1 and 0 <= vertical < 8 and 0 <= horizontal < 8 and
					tablero[vertical][horizontal] == 2-turno):
				contador = contador + 1
			elif (j > 1 and 0 <= vertical < 8 and 0 <= horizontal < 8 and 
					tablero[vertical][horizontal] == turno+1):
				flanqueada = True			
			elif (j > 1 and 0 <= vertical < 8 and 0 <= horizontal < 8 and 
					tablero[vertical][horizontal] == 0):
				fin_de_linea = True
			j = j + 1
		# Aumenta el contador de las cambiadas si la direccion está flanqueada
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

def obtenerJugada() -> [int]:
	"Traduce las coordenadas del mouse en subíndices de la matriz "

	global boton_salir 
	# Precondicion
	assert(True)

	coordenadas = (0,0)
	while coordenadas == (0,0):
		dibujarTablero()

		eventos = pygame.event.get()

		posDelMouse = pygame.mouse.get_pos()
	
		if boton_salir.collidepoint(posDelMouse):
			mensaje = fuente.render("Salir", 1, BLANCO)
		else:
			mensaje = fuente.render("Salir", 1, (0,0,0))
		boton_salir = ventana.blit(mensaje, (700, 15))

		if 200 <= posDelMouse[0] <= 600 and 50 <= posDelMouse[1] <= 450:
			left = (posDelMouse[0] - 200)//50
			top = (posDelMouse[1] - 50)//50
			
			remarcar_cuadro([left, top], VERDE ,eventos)					

		for event in eventos:
			if event.type == QUIT:
				confirmar_salida()			
			
			elif event.type == pygame.MOUSEBUTTONUP:				
				coordenadas = posDelMouse
				if (200 <= coordenadas[0] <= 600 
						and 50 <= coordenadas[1] <= 450):
					pass

				elif boton_salir.collidepoint(posDelMouse):
					confirmar_salida()
					coordenadas = (0,0)	
				else:
					# El mouse debe estar en el tablero
					coordenadas = (0,0)
		
		clock.tick(30)

		pygame.display.flip()
	
	jugada = [(coordenadas[1]-50)//50, (coordenadas[0]-200)//50]

	# Post condicion

	print(jugada)
	assert(0 <= jugada[0] < 8 and 0 <= jugada[1] < 8)
	return jugada 

def quedanFichas(tablero:[[int]]) -> bool:
	"Indica si aún quedan espacios vacíos en el tablero"

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
	assert(quedan == any(any(tablero[i][j]==0 for i in range(0,8)) 
		for j in range(0,8)))
	return quedan 

def puedeJugar(tablero:[[int]], turno:int) -> bool:
	"Evalúa si el turno puede hacer al menos una jugada válida"

	fila, puede = 0, False 
	direcciones = [
	[-1,0], [1,0], [0,1], [0,-1],
	[-1,-1], [-1,1], [1,1], [1,-1]
	]
	while fila < 8 and not puede:
		columna = 0
		while columna < 8 and not puede:
			if tablero[fila][columna] == turno+1:
				for i in direcciones:
					k, vecino, fin_de_linea = 1, True, False
					while k < 8 and vecino and not puede and not fin_de_linea:
						vertical = fila + k*i[0]
						horizontal = columna + k*i[1]
						if (k == 1 and 0 <= vertical < 8 and 0 <= horizontal < 8 and 
								tablero[vertical][horizontal] != 2-turno):
							vecino = False							
						elif (k == 1 and 0 <= vertical < 8 and 0 <= horizontal < 8 and 
								tablero[vertical][horizontal] == 2-turno):
							pass
						elif (k > 1 and 0 <= vertical < 8 and 0 <= horizontal < 8 and 
								tablero[vertical][horizontal] == 0):
							puede = True
						elif (k > 1 and 0 <= vertical < 8 and 0 <= horizontal < 8 and 
								tablero[vertical][horizontal] == turno+1):
							fin_de_linea = True							
						k = k+1

			columna = columna + 1
		fila = fila + 1	
	return puede 

def obtenerJugadaCPU():
	"""Retorna subindices de la matriz que sean una jugada valida y 
	remarca los cuadros que analiza """
	# Hay que arreglar esto
	
	direcciones = [
	[-1,0], [1,0], [0,1], [0,-1],
	[-1,-1], [-1,1], [1,1], [1,-1]
	]

	jugadas_validas = []
	origen = []

	renglon = 0 
	while renglon < 8:
		columna = 0
		while columna < 8:
			if tablero[renglon][columna] == turno+1:
				for i in direcciones:
					k, vecino, fin_de_linea = 1, True, False
					while k < 8 and vecino and not fin_de_linea:
						renglon_index = renglon + k*i[0]
						columna_index = columna + k*i[1]
						
						if (k == 1 and 0 <= renglon_index < 8 and 0 <= columna_index < 8 and 
								tablero[renglon_index][columna_index] != 2-turno):
							vecino = False							
						elif (k == 1 and 0 <= renglon_index < 8 and 0 <= columna_index < 8 and 
								tablero[renglon_index][columna_index] == 2-turno):
							pass
						elif (k > 1 and 0 <= renglon_index < 8 and 0 <= columna_index < 8 and 
								tablero[renglon_index][columna_index] == 0):
							origen.append([renglon, columna])
							jugadas_validas.append([renglon_index, columna_index])
							fin_de_linea = True	

						elif (k > 1 and 0 <= renglon_index < 8 and 0 <= columna_index < 8 and 
								tablero[renglon_index][columna_index] == turno+1):
							fin_de_linea = True							
						k = k+1

			columna = columna + 1
		renglon = renglon + 1	
	
	jugada_seleccionada = jugadas_validas[randint(0, len(jugadas_validas)-1)]
	

	for jugada in jugadas_validas:
		dibujarTablero()
		cuadro = [jugada[1], jugada[0]]
		remarcar_cuadro(cuadro, VERDE)
		pygame.display.flip()
		pygame.time.wait(1100//len(jugadas_validas))

	
	dibujarTablero()
	

	cuadro = [jugada_seleccionada[1], jugada_seleccionada[0]]
	remarcar_cuadro(cuadro, BLANCO)
	pygame.display.flip()
	pygame.time.wait(700)

	
	return jugada_seleccionada

# Funciones para la interfaz
def dibujarFichas(tablero:[[int]]) -> "void":
	"Dibuja las fichas sobre el tablero"

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
	
def nombresPuntaje(
	jugador_de_turno:int, nombreJugador1:str, 
	nombreJugador2:str) -> [str]: 
	"""Dibuja los nombres de los jugadores sobre su color de ficha
	y establece quien jugará con las negras y quien con las blancas
	"""

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
	
	return [negras, blancas]

def quienJuega(turno:int, orden:[str]) -> "void":
	"Mensaje de a quien le toca jugar"

	if turno == 0: 
		texto = "Ingrese jugada " + str(orden[1])
	elif turno == 1:
		texto = "Ingrese jugada " + str(orden[0])
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(tablon, (180,460))
	ventana.blit(mensaje, (180,460))
	
def error() -> "void":
	"Mensaje de jugada inválida" 

	texto = "Jugada inválida"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(tablon, (180,460))
	ventana.blit(mensaje, (180,460))
	pygame.display.flip()
	pygame.time.wait(800)

def resultadoParcial(tablero:[[int]]) -> "void":
	"Imprime la cantidad de fichas de cada color en el tablero"

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

def escribir(caracteres:[str] ,jugador:int) -> "void":
	"Escribe los nombres en pantalla a tiempo real cuando se piden "

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

def pedirNombre(jugador:int) -> str:
	"Permite a los jugadores escribir su nombre"

	caracteres = ""
	asignado = ""
	while asignado == "":
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_BACKSPACE:
					caracteres = caracteres[0:len(caracteres)-1]
				elif event.key == K_RETURN:
					if len(caracteres) > 0:
						caracteres = (caracteres[0] 
							+ caracteres[1:len(caracteres)].lower())
						asignado = caracteres

				elif event.key == K_SPACE or len(caracteres) > 6:
					pass
				else:						
					caracteres = caracteres + event.unicode					
			elif event.type == QUIT:
				confirmar_salida()

			escribir(caracteres, jugador)
	return caracteres

def jugarOtra() -> str:
	"Dice si los jugadores quieren jugar otra partida"

	ventana.blit(tabla, (0,0))
	texto = "¿Quieren jugar otra partida?"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (150,200))

	mensaje = fuente.render("Sí", 1, (0,0,0))
	opcion_Si = ventana.blit(mensaje, (250,300))

	mensaje = fuente.render("No", 1, (0,0,0))
	opcion_No = ventana.blit(mensaje, (450,300))

	pygame.display.flip()
	
	jugar_otra = ""
	while jugar_otra == "":
		ventana.blit(tabla, (0,0))
		texto = "¿Quieren jugar otra partida?"
		mensaje = fuente.render(texto, 1, (0,0,0))
		ventana.blit(mensaje, (150,200))

		if opcion_Si.collidepoint(pygame.mouse.get_pos()):		
			mensaje = fuente.render("Sí", 1, BLANCO)
		
		else:
			mensaje = fuente.render("Sí", 1, (0,0,0))

		opcion_Si = ventana.blit(mensaje, (250,300))


		if opcion_No.collidepoint(pygame.mouse.get_pos()):
			mensaje = fuente.render("No", 1, BLANCO)
		else:
			mensaje = fuente.render("No", 1, (0,0,0))

		opcion_No = ventana.blit(mensaje, (450,300))


		for event in pygame.event.get():
			if event.type == QUIT:
				confirmar_salida()

			elif event.type == pygame.MOUSEBUTTONUP:				
				
				if opcion_Si.collidepoint(pygame.mouse.get_pos()):
					jugar_otra = "sí"	

				elif opcion_No.collidepoint(pygame.mouse.get_pos()):
					jugar_otra = "no"

		pygame.display.flip()

	return jugar_otra									 

def mensajeVictoria(tablero:[[int]], orden:[int]) -> "void":
	"Muestra un mensaje de quien ha ganado la partida"

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

	pygame.time.wait(800)
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
	pygame.time.wait(2800)

def mensajeSaltoDeTurno(orden:[str], turno:int) -> "void":
	"Muestra un mensaje de a quien se la ha saltado el turno"
	pygame.time.wait(400)
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
	pygame.time.wait(1500)

def mensajeDosSaltosDeTurno() -> "void":
	"Advierte que se acabará la partida porque nadie pude jugar"

	ventana.blit(tablon, (180,460))
	texto = "¡Nadie puede jugar!"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (180, 460))
	texto = "La partida se ha acabado"
	mensaje = fuente.render(texto, 1, (0,0,0))
	ventana.blit(mensaje, (180, 500))
	pygame.display.flip()
	pygame.time.wait(1500)

def despedida() -> "void":
	"Mensaje de despedida"

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
	pygame.time.wait(3000)

def bienvenida() -> "void":
	"Mensaje de bienvenida"

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
				confirmar_salida()

def confirmar_salida():
	copia_ventana = ventana.copy()
	ventana.blit(tabla, (0,0))
	mensaje = fuente.render("¿Seguro de querer salir?", 1, NEGRO)
	ventana.blit(mensaje, (180, 250))
	mensaje = fuente.render("Sí", 1, (0,0,0))
	opcion_Si = ventana.blit(mensaje, (250,300))
	mensaje = fuente.render("No", 1, (190,190,190))
	opcion_No = ventana.blit(mensaje, (450,300))

	pygame.display.flip()
	
	while True:
		ventana.blit(tabla, (0,0))
		mensaje = fuente.render("¿Seguro de querer salir?", 1, NEGRO)
		ventana.blit(mensaje, (180, 250))

		if opcion_Si.collidepoint(pygame.mouse.get_pos()):
			mensaje = fuente.render("Sí", 1, BLANCO)
			
		
		else:
			mensaje = fuente.render("Sí", 1, (0,0,0))

		opcion_Si = ventana.blit(mensaje, (250,300))

		if opcion_No.collidepoint(pygame.mouse.get_pos()):
			mensaje = fuente.render("No", 1, BLANCO)
			
		else:
			mensaje = fuente.render("No", 1, (0,0,0))
		opcion_No = ventana.blit(mensaje, (450,300))		


		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

			elif event.type == pygame.MOUSEBUTTONUP:				
				
				if opcion_Si.collidepoint(pygame.mouse.get_pos()):					
					exit()


				elif opcion_No.collidepoint(pygame.mouse.get_pos()):
					ventana.blit(copia_ventana, (0,0))
					pygame.display.flip()
					return
		pygame.display.flip()

def seleccionar_modo():
	"Retorna que modo de juego se desea jugar. 1 para un jugador, 2 para dos"
	ventana.blit(tabla, (0,0))

	mensaje = fuente.render("Un jugador", 1, NEGRO)
	btn_un_jugador = ventana.blit(mensaje, (300, 150))

	mensaje = fuente.render("Dos jugadores", 1, NEGRO)
	btn_dos_jugadores = ventana.blit(mensaje, (300, 250))

	mensaje = fuente.render("Salir", 1, NEGRO)
	btn_salir = ventana.blit(mensaje, (300, 350))


	pygame.display.flip()

	while True:
		
		pos_mouse = pygame.mouse.get_pos()
		
		ventana.blit(tabla, (0,0))

		if btn_un_jugador.collidepoint(pos_mouse):
			mensaje = fuente.render("Un jugador", 1, BLANCO)
		else:
			mensaje = fuente.render("Un jugador", 1, NEGRO)

		ventana.blit(mensaje, (300, 150))

		if btn_dos_jugadores.collidepoint(pos_mouse):
			mensaje = fuente.render("Dos jugadores", 1, BLANCO)
		else:
			mensaje = fuente.render("Dos jugadores", 1, NEGRO)

		ventana.blit(mensaje, (300, 250))

		if btn_salir.collidepoint(pos_mouse):
			mensaje = fuente.render("Salir", 1, BLANCO)
		else:
			mensaje = fuente.render("Salir", 1, NEGRO)

		ventana.blit(mensaje, (300, 350))

		for event in pygame.event.get():
			if event.type == QUIT:
				confirmar_salida()

			elif event.type == MOUSEBUTTONUP:
				if btn_un_jugador.collidepoint(pos_mouse):
					return 1

				elif btn_dos_jugadores.collidepoint(pos_mouse):
					return 2

				elif btn_salir.collidepoint(pos_mouse):
					confirmar_salida()

		pygame.display.flip()

def remarcar_cuadro(pos_del_cuadro, color ,eventos=None):
	"""Recibe una posicion de la matriz y dibuja un cuadro en 
	el tablero en la posicion correspondiente"""

	# SE ESTA TOMANDO LA JUGADA AL REVES!

	left = pos_del_cuadro[0]*50 + 200
	top = pos_del_cuadro[1]*50 + 50
	
	

	if eventos != None:
		for event in eventos:
			if event.type == pygame.MOUSEBUTTONDOWN:					
				color = BLANCO				

	pygame.draw.rect(ventana, color,
		pygame.Rect(left+1, top+1, 47, 47), 2)

def dibujarTablero():
	ventana.blit(fondo, (0,0))
	dibujarFichas(tablero)
	resultadoParcial(tablero)
	quienJuega(turno, orden)
	nombresPuntaje(jugador_en_turno, nombreJugador1, nombreJugador2)

# Inicializacion
pygame.init()
ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Reversi")

clock = pygame.time.Clock()

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

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (220, 220, 220)
VERDE = (0, 255, 0)

# Inicio del juego
bienvenida()
modo_de_juego = seleccionar_modo()
nombreJugador1 = pedirNombre(1)

if modo_de_juego == 1:
	nombreJugador2 = "CPU"
else:
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
			# Se salta el turno del jugador si no puede jugar
			mensajeSaltoDeTurno(orden, turno)
			turno = cambiarJugador(turno)
			cambios_de_turno = cambios_de_turno + 1

		if cambios_de_turno == 2:
			# La partida se acaba si nadie puede jugar
			mensajeDosSaltosDeTurno()
			break

		if modo_de_juego == 2:
			jugada = obtenerJugada()

		elif modo_de_juego == 1:
			if turno == 0:
				jugada = obtenerJugada()
			elif turno == 1:
				jugada = obtenerJugadaCPU()

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