cuadruplos = []

pila_operandos = []
pila_operadores = []
pila_saltos = []
pila_tipos = []

temp_contador = 0

def nuevo_temporal():
    global temp_contador
    temp_contador += 1
    return "t" + str(temp_contador)

#Esta funcion genera el cuadruplo y lo agrega a la lista de cuadruplos
def generar_cuadruplo(operador, operando1, operando2, resultado):
    cuadruplo = [operador, operando1, operando2, resultado]
    cuadruplos.append(cuadruplo)
    return len(cuadruplos)-1

#Esta funcion devuelve la posicion del siguiente cuadruplo es como un cont 
def sig_cuadruplo():
    return len(cuadruplos)

#Esta funcion rellena un cuadruplo con un salto, osea cambia el valor de un cuadruplo existente
#Se usa el GotoF, GotoV, y Goto para rellenar los saltos
def rellenar_salto(cuadruplo, salto):
    cuadruplos[cuadruplo][3] = salto


#Esto es para los operandos, metodos para meter y sacar de la pila de operandos
def meter_operandos(operando):
    pila_operandos.append(operando)

def sacar_operandos():
    if not pila_operandos:
        raise Exception("Error: No hay operandos en la pila")   
    return pila_operandos.pop()

def top_operando():
    if not pila_operandos:
        raise Exception("Error: No hay operandos en la pila")   
    return pila_operandos[-1]

#Esto es para los operadores, metodos para meter y sacar de la pila de operadores
def meter_operadores(operador):
    pila_operadores.append(operador)

def sacar_operadores():
    return pila_operadores.pop()

#Esto es para los saltos, metodos para meter y sacar de la pila de saltos
def meter_saltos(salto):
    pila_saltos.append(salto)

def sacar_saltos():
    return pila_saltos.pop()

#Esto es para los tipos, metodos para meter y sacar de la pila de tipos
def meter_tipos(tipo):
    pila_tipos.append(tipo)

def sacar_tipos():
    return pila_tipos.pop()
