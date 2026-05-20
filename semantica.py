# ANALISIS SEMANTICO
# Tabla de simbolos para ver errores y Cubo semantico para validacion de tipos

tabla_simbolos = {}

#Esto esta sujeto a revision
# (Tipo1, Tipo2, Operador) : Tipo_Resultado
# se definen los tipos de variables que pueden participar en operaciones
cubo_semantico = {
    # SUMA
    ('int', 'int', '+'): 'int',
    ('float', 'float', '+'): 'float',
    ('int', 'float', '+'): 'float',
    ('float', 'int', '+'): 'float',
    ('string', 'string', '+'): 'string', # solo concatenación 
    
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
    
    #De este etngo duda
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

# Tabla de tipos para temporales (t1, t2, ...)
tipo_temporales = {}

def registrar_tipo_temporal(nombre_temp, tipo):
    tipo_temporales[nombre_temp] = tipo

def obtener_tipo_temporal(nombre_temp):
    if nombre_temp not in tipo_temporales:
        raise Exception(f"Error Semántico: Temporal '{nombre_temp}' sin tipo registrado.")
    return tipo_temporales[nombre_temp]

# Infiere el tipo de un literal (CTE, TRUE, FALSE, STRING)
# Esto es para los valores que ya están en el código, ej. si viene un 6 o un hola que sepa identificar al tipo de variable que se refiere
def obtener_tipo_literal(valor):
    if isinstance(valor, bool):   # bool ANTES de int, porque bool es subclase de int en Python
        return 'bool'
    elif isinstance(valor, int):
        return 'int'
    elif isinstance(valor, float):
        return 'float'
    elif isinstance(valor, str):
        return 'string'
    else:
        raise Exception(f"Error Semántico: Literal '{valor}' de tipo desconocido.")

# Resuelve el tipo de cualquier operando: variable, temporal o literal
def obtener_tipo_operando(operando):
    if isinstance(operando, str):
        if operando in tabla_simbolos:
            return obtener_tipo_variable(operando)
        elif operando in tipo_temporales:
            return obtener_tipo_temporal(operando)
        else:
            # Es un string literal (ej. "hola")
            return 'string'
    else:
        return obtener_tipo_literal(operando)

# Valida con el cubo y regresa el tipo resultado, o lanza error
def verificar_operacion(tipo1, tipo2, operador):
    resultado = consultar_cubo(tipo1, tipo2, operador)
    if resultado == 'error':
        raise Exception(
            f"Error Semántico: Operación inválida — '{tipo1}' {operador} '{tipo2}'"
        )
    return resultado