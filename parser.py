# se importa la librería de Yacc
import ply.yacc as yacc

# se importa la lista de tokes definida en lexer.py
from lexer import tokens


# DEFINICION DE REGLAS GRAMATICALES
# P -> Programa
def p_programa(p):
    '''
        programa : PROGRAM ID ILLAVE variables bloque DLLAVE
    '''

# V -> Variables
def p_V_variables(p):
    '''
        variables : VAR ids DOSPUNTOS TypeOf PUNTOYCOMA 
                    | empty
    '''

# ids -> Identificadores
def p_ids(p):
    '''
        ids :   ID 
                | ids COMA ID
    '''

# TypeOf -> Tipo de dato
def p_TypeOf(p):
    '''
        TypeOf :    INT 
                    | FLOAT 
                    | BOOL
                    | STRING
    '''

# B -> Bloque
#DUDA BUSCAR COMO HACER RETURNS
def p_B_bloque(p):
    '''
        bloque : BEGIN PUNTOYCOMA estatutos END PUNTOYCOMA
    '''

# S -> Estatutos
def p_S_estatuto(p):
    '''
        estatuto :  asignar 
                    | if 
                    | while 
                    | for 
                    | writeln
                    | incremento PUNTOYCOMA
    '''

def p_estatutos(p):
    '''
        estatutos : estatuto estatutos 
                    | empty
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
        valor : CTE 
                | ID
                | STRING
    '''

# IF -> Estatuto if
def p_IF_if(p):
    '''
    if : IF IPAREN expresion DPAREN THEN ILLAVE estatutos DLLAVE
       | IF IPAREN expresion DPAREN THEN ILLAVE estatutos DLLAVE ELSE ILLAVE estatutos DLLAVE
    '''

# WHILE -> Estatuto while
def p_WHILE_while(p):
    '''
        while : WHILE IPAREN expresion DPAREN DO ILLAVE estatutos DLLAVE 
    '''

def p_incremento(p):
    '''
    incremento : ID INCREMENTO
               | ID DECREMENTO
               | asignar
    '''

# FOR -> Estatuto for
def p_FOR_for(p):
    '''
        for : FOR IPAREN asignar expresion PUNTOYCOMA incremento DPAREN ILLAVE estatutos DLLAVE
    '''

# E -> Expresion
def p_E_expresion(p):
    '''
        expresion : expresionS MEQ expresionS 
                    | expresionS MAQ expresionS 
                    | expresionS MEI expresionS 
                    | expresionS MAI expresionS 
                    | expresionS IGUAL expresionS 
                    | expresionS DISTINTO expresionS
                    | expresionS 
    '''

def p_ES_expresionS(p):
    '''
        expresionS :    expresionS SUMA termino 
                        | expresionS RESTA termino 
                        | expresionS OR termino 
                        | termino
    '''


# DUDA AQUI
def p_T_termino(p):
    '''
        termino :   termino MULTIPLICAR factor 
                    | termino DIVIDIR factor 
                    | termino AND factor 
                    | factor
    '''

#DUDA AQUI
def p_factor(p):
    '''
    factor : ID
           | CTE
           | IPAREN expresion DPAREN
           | TRUE
           | FALSE
           | NOT factor
    '''



# DUDA QUE HAREMOS CON OP Y OPERANDOR
# para deteccion/manejo de errores
def p_error(p):
    if p:
        print(f"Error de sintaxis en el token '{p.value}' (línea {p.lineno})")
    else:
        print("Error de sintaxis al final del archivo")

# para manejo de empty
def p_empty(p):
    'empty :'
    pass



parser = yacc.yacc()

#CASO DE PRUEBA FOR
# if __name__ == '__main__':
#     data = '''
#     program main{
# 	var i,n,x : int;
# 	begin;
# 		writeln("factorial for");
# 		x:=1;
# 		n:=5;	
# 		for (i:=1;i<n;i++){
# 			x := x * i;
# 		}
# 		writeln(x);
# 	end;
# }
#     '''

# CASO DE PRUEBA IF
# if __name__ == '__main__':
#     data = '''
#     program main{
# 	var a,b,x,y,i : int;
# 	begin;	
# 		writeln("prueba if");

# 		a := 5;
# 		b :=  a + 3;
# 		x := b +5;
# 		y := x + a;

# 		if( a>b) then
# 		{
# 			i := a*5+(b+4);
# 			writeln("caso true");
# 			writeln(a);
# 		}else
# 		{
# 			if(y<x) then
# 			{
# 				i := x * (b * y);
# 				writeln(x);
# 				writeln("if anidado");
# 			}else
# 			{
# 				writeln("ultimo caso");
# 			}
# 		}
# 		writeln(i);
# 	end;
# }
#     '''

#CASO DE PRUEBA WHILE
if __name__ == '__main__':
    data = '''
    program main{
	var i,n,x : int;
	begin;
		writeln("factorial while");
		n := 5;
		x := 1;
		while (n>=1) do
		{
			x := x * n;
			n--;
		}
		writeln(x);
	end;
}
    '''

    result = parser.parse(data)
    print("Parseo exitoso:", result)
