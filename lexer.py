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
    'COMA'
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
t_COMA = r','

t_ignore = ' \t'  # Ignorar espacios y tabulaciones

#Funciona para que cada vez que se encuentra un salto de linea, se incremente el numero de linea del lexer
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


#Funcion para manejar errores lexicos, pero funciona en conjunto con el t_newline
#Ya que cuando se encuentra un token que no es valido lo marca pero el t_newline con su incremento
# de linea hace que el error se marque en la linea correcta, si no se tuviera el t_newline el error se marcaria en la linea 1 siempre
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verificar si es una palabra reservada
    return t


def t_CTE(t):
    r'\d+'
    t.value = int(t.value)
    return t


lexer = lex.lex()

# if __name__ == '__main__':
#     data = '''
#     program main {
#         var a,b,x,y,i : int;
#         begin
#             x := 1;
#             for (i := 1; i < n; i++) {
#                 x := x * i;
#             }
#             writeln(x);
#         end
#     }
#     '''

#     lexer.input(data)

#     for tok in lexer:
#         print(tok)

