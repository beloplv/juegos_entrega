import json
from os.path import isfile

def mostrar ():
    if isfile('jugadores.json'):
        archivo=open('jugadores.json')
        datos=json.load(archivo)
        print(json.dumps(datos, sort_keys= True, indent=4))
        archivo.close()
    else:
        print('no hay datos')


if __name__ == '__main__':
    mostrar()