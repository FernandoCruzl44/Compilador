import ply.lex as lex

#Palabras reservadas

reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'begin': 'BEGIN',
    'end': 'END',
    'int': 'INT',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'for': 'FOR',
    'writeln': 'WRITELN',
    'true': 'TRUE',
    'false': 'FALSE',
    'or': 'OR',
    'and': 'AND',
    'not': 'NOT'
}

#Lista de tokens

tokens = [
    'ID',
    'CTE',

    'ASSIGNAR',
    'SUMA',
    'RESTA',
    'MULTIPLICAR',
    'DIVIDIR',

    'MEQ', #Menor que
    'MAQ', #Mayor que
    'MEI', #Menor o igual
    'MAI', #Mayor o igual
    'IGUAL',
    'DISTINTO',

    'INCREMENTO',
    'DECREMENTO',

    'IPAREN', #Parentesis izquierdo
    'DPAREN', #Parentesis derecho
    'ILLAVE', #Llave izquierda
    'DLLAVE', #Llave derecha
    'PUNTOYCOMA',
    'DOSPUNTOS',
    'COMMA'
] + list(reserved.values())

#Expresiones regulares para tokens simples
t_ASSIGNAR = r':='
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICAR = r'\*'
t_DIVIDIR = r'/'

t_MEQ = r'<'
t_MAQ = r'>'
t_MEI = r'<='
t_MAI = r'>='
t_IGUAL = r'=='
t_DISTINTO = r'!='

t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'
t_IPAREN = r'\('
t_DPAREN = r'\)'
t_ILLAVE = r'\{'
t_DLLAVE = r'\}'
t_PUNTOYCOMA = r';'
t_DOSPUNTOS = r':'
t_COMMA = r','


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verificar si es una palabra reservada
    return t

def t_CTE(t):
    r'\d+'
    t.value = int(t.value)
    return t

