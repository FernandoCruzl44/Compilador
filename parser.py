import ply.yacc as yacc
from lexer import tokens


# P -> Programa
def p_programa(p):
    '''
        PROGRAM ID ILLAVE variables bloque DLLAVE
    '''

# V -> Variables
def p_V_variables(p):
    '''
        variables : VAR ids DOSPUNTOS TypeOf PUNTOYCOMA | empty
    '''

# ids -> Identificadores
def p_ids(p):
    '''
        ids : ID | ids COMA ID
    '''

# TypeOf -> Tipo de dato
def p_TypeOf(p):
    '''
        TypeOf : INT | FLOAT | BOOL
    '''

# B -> Bloque
def p_B_bloque(p):
    '''
        bloque : BEGIN PUNTOYCOMA estatutos END PUNTOYCOMA
    '''

# S -> Estatutos
def p_S_estatuto(p):
    '''
        estatuto: asignar | if | while | for | writeln
    '''

def p_estatutos(p):
    '''
        estatutos : estatuto estatutos | estatuto
    '''

# A -> Estatuto Asignacion
def p_A_asignacion(p):
    '''
        asignar : ID ASSIGNAR expresion PUNTOYCOMA
    '''

# W -> Estatuto Writeln
def p_W_writeln(p):
    '''
        writeln : WRITELN IPAREN valor DPAREN PUNTOYCOMA
    '''

def p_Val_valor(p):
    '''
        valor : CTE | ID
    '''

# IF -> Estatuto if
def p_IF_if(p):
    '''
        if : IF IPAREN expresion DPAREN THEN expresion ELSE estatutos | IF IPAREN expresion DPAREN THEN expresion
    '''

# WHILE -> Estatuto while
def p_WHILE_while(p):
    '''
        while : WHILE IPAREN expresion DPAREN DO ILLAVE estatutos DLLAVE PUNTOYCOMA
    '''

# FOR -> Estatuto for
def p_FOR_for(p):
    '''
        for : FOR IPAREN asignar PUNTOYCOMA expresion PUNTOYCOMA expresion DPAREN ILLAVE expresion DLLAVE
    '''

# E -> Expresion
def p_E_expresion(p):
    '''
        expresion : expresionS MEQ expresionS | expresionS MAQ expresionS | expresionS MEI expresionS | expresionS MAI expresionS | expresionS IGUAL expresionS | expresionS 
    '''

def p_ES_expresionS(p):
    '''
        expresionS : expresionS SUMA termino | expresionS RESTA termino | expresionS OR termino | termino
    '''

def p_T_termino(p):
    '''
        termino : termino MULTIPLICAR factor | termino DIVIDIR factor | termino AND factor | factor
    '''