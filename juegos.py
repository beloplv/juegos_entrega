''' Para elegir entre archivo de texto y archivo binario me tengo que fijar
en dos cuestiones:
		1.con que aplicacion van a acceder
		2.la estructura del dato que va a contener el archivo

1.Como no se desde que aplicacion van a acceder al archivo eleji
json porque es un formato muy popular y utilizado, me permite
independizarme de cualquier lenguaje y tecnologia que este utilizando
(json es estandar, y no depende de python). Ademas de ser flexible
es seguro y muy facil de utilizar.
2.La estructa que eleji para guardar los datos es un diccionario, que
contiene otro diccionario. Esta estructura se encuadra en un formato
que permite json (definidos como objetos: clave-valor).
El ejercicio decia que tenia que guardar en un archivo, el nombre del jugador
y a los juegos que jugo, entonces defini como clave el nombre, al cual le
agregue apellido (para que sea menos posible la repeticion de la clave) y el
valor seria otro diccionario que contiene como claves los juegos que jugo
(que pueden ser: ahorcado,ta-te-ti y otello) y como valor un numero que
referencia las veces que lo jugo.

Por ejemplo    --->        {'anabel': {'Ahorcado':5,'Otello':1,'Ta-te-ti':2}}
otro ejemplo   --->        {'anabel': {Ta-te-ti:3}}

Explicandolo a detelle ...

Me guardo el nombre del jugador en una variable y lo paso a minuscula (porque si
escribi el mismo nombre pero en mayuscula, me lo tomaria como otra clave).
Utilizo una lista que se llama lista_juegos a la cual le voy agregando los
juegos que jugo. En un principio vendria a ser algo como:
lista_juegos= ['ahorcado','ta-te-ti','ahorcado','otello','ta-te-ti']
Despues ordeno la lista alfabeticamente y luego para contabilizar cuantas
veces aparecen los juegos utilizo el modulo collections(funcion counter)
y siguiendo con el mismo ejemplo, quedaria asi:
{'ahorcado':2,'otello':1,'ta-te-ti':2}
*En caso de que el archivo no exista, creo el archivo y guardo el dato
*En caso de que el archivo exista:
	*deserializo los datos y me fijo si la clave(nombre del jugador) existe:
				*si la clave no existe: guardo el dato
				*si la clave existe: tomo el diccionario de esa clave(nombre
				 del jugador) y tambien utilizo la funcion counter, sumo los
				 dos diccionarios y guardo los datos.
				 ejemplo ---> dic1={'ahorcado':5,'ta-te-ti':1}
				              dic2={'ta-te-ti':2}
							  dic1+=dic2
							  dic1={'ahorcado':5,'ta-te-ti':3}
Finalmente inicializo la lista en vacio, para el siguiente jugador.
'''

import json
import hangman
import reversegam
import PySimpleGUI as sg
import tictactoeModificado
from os.path import isfile
from collections import Counter

nombre_archivo = 'jugadores.json'
datos = {}
lista_juegos =[]
lista_box=('Ahorcado','Ta-te-ti','Otello')


def extraer_datos():
	with open('jugadores.json', 'r') as archivo:
		info = json.load(archivo)
	return info

def guardar_datos (nombre_archivo,datos):
	with open(nombre_archivo,'w') as archivo:
		json.dump(datos,archivo)

def cargar_datos (nombre_archivo,nombre,lista_juegos,datos):
	lista_juegos.sort()
	cnt = Counter(lista_juegos)
	if isfile(nombre_archivo):
		datos=extraer_datos()
		if nombre in datos.keys():
			cnt2= Counter (datos[nombre])
			cnt2 += cnt
			datos[nombre] = cnt2
		else:
			datos[nombre] = cnt
	else:
		datos[nombre] = cnt
	guardar_datos(nombre_archivo,datos)

layout =[[sg.Text('Nombre y Apellido'),sg.InputText(),sg.Button('Read')],
		[sg.Text('¿A que juego quiere jugar?')],
		[sg.Listbox(values=lista_box, size=(30, 3)),sg.Button('Ok')],
	    [sg.Button('Guardar'), sg.Button('Salir')]]

sg.ChangeLookAndFeel('Dark2')
window = sg.Window('Bienvenido').Layout(layout)
while True:
	event, values = window.Read()
	if event is None or event == 'Salir':
		break
	elif event is 'Read':
		nombre= values[0].lower()
	elif event is 'Ok':
		juego_elegido=values[1]
		if juego_elegido == ['Ahorcado']:
			lista_juegos.append('Ahorcado')
			hangman.main()
		elif juego_elegido == ['Ta-te-ti']:
			lista_juegos.append('Ta-te-ti')
			tictactoeModificado.main()
		elif juego_elegido == ['Otello']:
			lista_juegos.append('Otello')
			reversegam.main()
	elif event is 'Guardar':
		if nombre == '':
			sg.Popup('Falta agregar un nombre')
		else:
			cargar_datos(nombre_archivo,nombre,lista_juegos,datos)
			lista_juegos=[]
			sg.Popup('Los datos se guardaron')
window.Close()