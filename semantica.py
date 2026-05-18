# ANALISIS SEMANTICO
# Tabla de simbolos para ver errores y Cubo semantico para validacion de tipos

tabla_simbolos = {}

# (Tipo1, Tipo2, Operador) : Tipo_Resultado
cubo_semantico = {
    # SUMA
    ('int', 'int', '+'): 'int',
    ('float', 'float', '+'): 'float',
    ('int', 'float', '+'): 'float',
    ('float', 'int', '+'): 'float',
    ('string', 'string', '+'): 'string', # concatenación
    
    # RESTA
    ('int', 'int', '-'): 'int',
    ('float', 'float', '-'): 'float',
    ('int', 'float', '-'): 'float',
    ('float', 'int', '-'): 'float',

    # MULTIPLICACION
    ('int', 'int', '*'): 'int',
    ('float', 'float', '*'): 'float',
    ('int', 'float', '*'): 'float',
    ('float', 'int', '*'): 'float',

    # DIVISION
    ('int', 'int', '/'): 'float', 
    ('float', 'float', '/'): 'float',
    ('int', 'float', '/'): 'float',
    ('float', 'int', '/'): 'float',

    # ASIGNACION (:=)
    # Lado izquierdo (variable), Lado derecho (valor)
    ('int', 'int', ':='): 'int',
    ('float', 'float', ':='): 'float',
    ('float', 'int', ':='): 'float', # Podemos guardar int en float
    ('bool', 'bool', ':='): 'bool',
    ('string', 'string', ':='): 'string',

    # COMPARACIONES (<, >, <=, >=, ==, !=)
    ('int', 'int', '<'): 'bool',
    ('float', 'float', '<'): 'bool',
    ('int', 'float', '<'): 'bool',
    ('float', 'int', '<'): 'bool',

    ('int', 'int', '>'): 'bool',
    ('float', 'float', '>'): 'bool',
    ('int', 'float', '>'): 'bool',
    ('float', 'int', '>'): 'bool',
    
    ('int', 'int', '<='): 'bool',
    ('float', 'float', '<='): 'bool',
    ('int', 'float', '<='): 'bool',
    ('float', 'int', '<='): 'bool',
    
    ('int', 'int', '>='): 'bool',
    ('float', 'float', '>='): 'bool',
    ('int', 'float', '>='): 'bool',
    ('float', 'int', '>='): 'bool',
    
    ('int', 'int', '=='): 'bool',
    ('float', 'float', '=='): 'bool',
    ('int', 'float', '=='): 'bool',
    ('float', 'int', '=='): 'bool',
    ('bool', 'bool', '=='): 'bool',
    ('string', 'string', '=='): 'bool',
    
    ('int', 'int', '!='): 'bool',
    ('float', 'float', '!='): 'bool',
    ('int', 'float', '!='): 'bool',
    ('float', 'int', '!='): 'bool',
    ('bool', 'bool', '!='): 'bool',
    ('string', 'string', '!='): 'bool',

    # OPERADORES LÓGICOS (and, or)
    ('bool', 'bool', 'and'): 'bool',
    ('bool', 'bool', 'or'): 'bool',
    
    # UNARIOS (not) - Lo representamos como tipo2 = None
    ('bool', None, 'not'): 'bool',
}

#Esta funcion recibe los dos tipos y el operador, regresa el tipo resultante o 'error'
#si es invalido
def consultar_cubo(tipo1, tipo2, operador):
   
    return cubo_semantico.get((tipo1, tipo2, operador), 'error')

#Guarda la variable en la tabla de simbolos y lanza un error si ya existe
def registrar_variable(nombre, tipo):

    if nombre in tabla_simbolos:
        raise Exception(f"Error Semántico: La variable '{nombre}' ya fue declarada previamente.")
    tabla_simbolos[nombre] = tipo

#Esta funcion busca el tipo de la variable en la tabla de simbolos y lanza un error si no existe
def obtener_tipo_variable(nombre):
    if nombre not in tabla_simbolos:
        raise Exception(f"Error Semántico: La variable '{nombre}' no ha sido declarada.")
    return tabla_simbolos[nombre]