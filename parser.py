# ANALISIS SINTACTICO + GENERACION DE CUADRUPLOS

# se importa la librería de Yacc
import ply.yacc as yacc

# se importa la lista de tokes definida en lexer.py
from lexer import tokens

# se importan las funciones definidas en cuadruplos.py
from cuadruplos import *  

# se importan las funciones definidas en semantica.py
# importar funciones para revisar semantica
from semantica import *

from interpretador import *


# guardar los Ids que vayan apareciendo para luego ver sus tipos
ids_pendientes = []

# se guarda el ultimo valor resultante de la expresion
ultimo_tipo_expr = [None]


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

    # se revisa que si coincida con la estructura de la gramatica de variables
    # varibales (p0), VAR (p1), ids (p2), DOSPUNTOS (p3), TypeOf(p4), PUNTOYCOMA (p5)
    if len(p) == 6:
        tipo = p[4] # pq es el elemento numero 4
        for nombre in ids_pendientes:
            registrar_variable(nombre, tipo)
        ids_pendientes.clear()  # para poder hacer la sig


# ids -> Identificadores
def p_ids(p):
    '''
        ids :   ID 
                | ids COMA ID
    '''
    if len(p) == 2:
        ids_pendientes.append(p[1])
    else:
        ids_pendientes.append(p[3])

# TypeOf -> Tipo de dato
def p_TypeOf(p):
    '''
        TypeOf :    INT 
                    | FLOAT 
                    | BOOL
                    | STRING
    '''
    p[0] = p[1] # para que en variable si lo tome

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
                    | incremento_puntocoma
    '''

def p_estatutos(p):
    '''
        estatutos : estatuto estatutos 
                    | empty
    '''


# A_base --> asignacion base como apoyo para fors
def p_asignar_base(p):
    '''
        asignar_base : ID ASSIGNAR expresion
    '''

    tipo_var = obtener_tipo_variable(p[1])
    tipo_expr = p[3]
    verificar_operacion(tipo_var, tipo_expr, ':=')

    valor = sacar_operandos()
    generar_cuadruplo(':=', valor, None, p[1]) # P[1] es el primer simbolo (ID en este caso)
    p[0] = p[1] # guarda el ID para el for

# A -> Estatuto Asignacion
def p_A_asignacion(p):
    '''
        asignar : asignar_base PUNTOYCOMA
    '''


# W -> Estatuto Writeln
def p_W_writeln(p):
    '''
        writeln : WRITELN IPAREN valor DPAREN PUNTOYCOMA
    '''
    arg = p[3]
    if isinstance(arg, str) and arg not in tabla_simbolos:
        arg = f'"{arg}"'  # Si es un string literal sin comillas, se le agregan comillas para que se imprima correctamente
    generar_cuadruplo('WRITELN', None, None, arg )

def p_Val_valor(p):
    '''
        valor : CTE 
                | ID
                | STRING
    '''
    # Si es id se checa la tabla de simbolos
    if isinstance(p[1], str) and p[1] in tabla_simbolos:
        obtener_tipo_variable(p[1])
    
    p[0] = p[1]

# IF -> Estatuto if
def p_IF_if(p):
    '''
        if : IF IPAREN expresion DPAREN marca_gotoF THEN ILLAVE estatutos DLLAVE
           | IF IPAREN expresion DPAREN marca_gotoF THEN ILLAVE estatutos DLLAVE marca_goto ELSE ILLAVE estatutos DLLAVE
    '''

    #checar si hay elses
    if len(p) == 10:
        # No hay else --> GotoF
        rellenar_salto(sacar_saltos(), sig_cuadruplo())
    else:
        # hay else --> Goto
        rellenar_salto(sacar_saltos(), sig_cuadruplo())
 
def p_marca_gotoF(p):
    '''marca_gotoF : empty'''

    if ultimo_tipo_expr[0] != 'bool':
        raise Exception (
            f"Error Semántico: La condición del IF debe ser bool, se obtuvo '{ultimo_tipo_expr[0]}'"
        )

    condicion = sacar_operandos()
    salto_falso = generar_cuadruplo('GotoF', condicion, None, None)
    meter_saltos(salto_falso)
 
def p_marca_goto(p):
    '''marca_goto : empty'''
    salto_true = generar_cuadruplo('Goto', None, None, None)
    rellenar_salto(sacar_saltos(), sig_cuadruplo())
    meter_saltos(salto_true)

# WHILE -> Estatuto while
def p_WHILE_while(p):
    '''
        while : WHILE marca_inicio IPAREN expresion marca_gotoF DPAREN DO ILLAVE estatutos DLLAVE
    '''
    
    salto_falso  = sacar_saltos()
    inicio_loop  = sacar_saltos() 
    # Regresa al inicio
    generar_cuadruplo('Goto', None, None, inicio_loop)
    # Rellena el GotoF 
    rellenar_salto(salto_falso, sig_cuadruplo())
 
def p_marca_inicio(p):
    '''marca_inicio : empty'''
    # Guarda la posición antes de evaluar la condición
    meter_saltos(sig_cuadruplo())


# FOR -> Estatuto for
def p_FOR_for(p):
    '''
        for : FOR IPAREN asignar_base PUNTOYCOMA marca_inicio expresion marca_gotoF PUNTOYCOMA incremento_expr DPAREN ILLAVE estatutos DLLAVE
    '''
    salto_falso = sacar_saltos()
    inicio_cond = sacar_saltos()
 
    # Cuadruplo incremento/decremento
    var, op = p[9]
    if op == '++':
        generar_cuadruplo('+', var, 1, var)
    elif op == '--':
        generar_cuadruplo('-', var, 1, var)
        
    # Si op es None significa que en asignar_base se generó su cuádruplo
 
    generar_cuadruplo('Goto', None, None, inicio_cond)
    # Rellena el GotoF para salir del for
    rellenar_salto(salto_falso, sig_cuadruplo())

def p_incremento_expr(p):
    '''
    incremento_expr : ID INCREMENTO
               | ID DECREMENTO
               | asignar_base
    '''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        # asignar_base ya hizo su cuádruplo
        # regresa (id, None)
        p[0] = (p[1], None)

def p_incremento_puntocoma(p):
    '''
        incremento_puntocoma : ID INCREMENTO PUNTOYCOMA
                        | ID DECREMENTO PUNTOYCOMA
    '''
    var = p[1]
    op  = p[2]
    if op == '++':
        generar_cuadruplo('+', var, 1, var)
    else:
        generar_cuadruplo('-', var, 1, var)

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
    if len(p) == 4:
        tipo2 = p[3]
        tipo1 = p[1]
        tipo_res = verificar_operacion(tipo1, tipo2, p[2])


        op2 = sacar_operandos()
        op1 = sacar_operandos()
        temp = nuevo_temporal()
        generar_cuadruplo(p[2], op1, op2, temp)

        registrar_tipo_temporal(temp, tipo_res)
        meter_operandos(temp)
        p[0] = tipo_res
        ultimo_tipo_expr[0] = tipo_res

    else:
        p[0] = p[1]
        ultimo_tipo_expr[0] = p[1]

def p_ES_expresionS(p):
    '''
        expresionS :    expresionS SUMA termino 
                        | expresionS RESTA termino 
                        | expresionS OR termino 
                        | termino
    '''
    if len(p) == 4:
        tipo2 = p[3]
        tipo1 = p[1]

        tipo_res = verificar_operacion(tipo1, tipo2, p[2])

        op2 = sacar_operandos()
        op1 = sacar_operandos()
        temp = nuevo_temporal()
        generar_cuadruplo(p[2], op1, op2, temp)

        registrar_tipo_temporal(temp, tipo_res)
        p[0] = tipo_res

        meter_operandos(temp)

    else:
        p[0] = p[1]




def p_T_termino(p):
    '''
        termino :   termino MULTIPLICAR factor 
                    | termino DIVIDIR factor 
                    | termino AND factor 
                    | factor
    '''
    if len(p) == 4:
        tipo2 = p[3]
        tipo1 = p[1]

        tipo_res = verificar_operacion(tipo1, tipo2, p[2])

        op2 = sacar_operandos()
        op1 = sacar_operandos()
        temp = nuevo_temporal()
        generar_cuadruplo(p[2], op1, op2, temp)

        registrar_tipo_temporal(temp, tipo_res)
        meter_operandos(temp)
        p[0] = tipo_res
    else:
        p[0] = p[1]

# se dividen los factores para facilidad para hacer los cuadruplos
def p_factor_id(p):
    '''
    factor : ID
    '''
    tipo = obtener_tipo_variable(p[1])
    meter_operandos(p[1])
    p[0] = tipo

def p_factor_cte(p):
    '''
    factor : CTE
    '''
    meter_operandos(p[1])
    p[0] = obtener_tipo_operando(p[1])

def p_factor_true(p):
    '''
    factor : TRUE
    '''
    meter_operandos(True)
    p[0] = 'bool'

def p_factor_false(p):
    '''
    factor : FALSE
    '''
    meter_operandos(False)
    p[0] = 'bool'

def p_factor_grupo(p):
    '''
    factor : IPAREN expresion DPAREN
    '''
    p[0] = p[2]
    pass # el resultado ya esta en la pila 

def p_factor_not(p):
    '''
    factor : NOT factor
    '''
    tipo_op = p[2]
    tipo_res = verificar_operacion(tipo_op, None, 'not')

    operando = sacar_operandos()
    temp = nuevo_temporal()
    generar_cuadruplo('NOT', operando, None, temp)

    registrar_tipo_temporal(temp, tipo_res)

    meter_operandos(temp)

    p[0] = tipo_res


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
if __name__ == '__main__':
     data = '''
     program main{
 	var a,b,x,y,i : int;
 	begin;	
 		writeln("prueba if");

 		a := 5;
 		b :=  a + 3;
 		x := b +5;
 		y := x + a;

 		if( a>b) then
 		{
 			i := a*5+(b+4);
 			writeln("caso true");
 			writeln(a);
 		}else
 		{
 			if(y<x) then
 			{
 				i := x * (b * y);
 				writeln(x);
 				writeln("if anidado");
 			}else
 			{
 				writeln("ultimo caso");
 			}
 		}
 		writeln(i);
 	end;
 }
     '''

#CASO DE PRUEBA WHILE
# if __name__ == '__main__':
#     data = '''
#     program main{
# 	var i,n,x : int;
# 	begin;
# 		writeln("factorial while");
# 		n := 5;
# 		x := 1;
# 		while (n>=1) do
# 		{
# 			x := x * n;
# 			n--;
# 		}
# 		writeln(x);
# 	end;
# }
#     '''


# CASO PRUEBA ERRORES
# if __name__ == '__main__':
#     data = '''
#     program main{
#         var a,b,x,y,i,j : int;
#         begin;
#             writeln("prueba semantica");

#             a := 5;
#             b :=  a + 3;
#             x := b +5;
#             y := x + a;

#             if ( ( a>b) and (a*5+(b+4)) ) then
#             {
#                 i := a*5+(b+4);
#                 writeln("caso true");
#                 writeln(a);
#             }else
#             {
#                 if(y<x) then
#                 {
#                     i := x * (b * y);
#                     writeln(x);
#                     writeln("if anidado");
#                 }else
#                 {
#                     writeln("ultimo caso");
#                 }
#             }

#             writeln(i);
#         end;
#     }
#     '''

result = parser.parse(data)
print("Parseo exitoso:", result)

print("\nTabla de símbolos:")
for var, tipo in tabla_simbolos.items():
    print(f"  {var} : {tipo}")

print("\nTipos de temporales:")
for temp, tipo in tipo_temporales.items():
    print(f"  {temp} : {tipo}")

print("\nCuádruplos generados:")
for i, cuad in enumerate(cuadruplos):
    print(i, cuad)

print("\n--- Ejecución de la máquina virtual ---")
interpretar()