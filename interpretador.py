#Aqui se hara la maquina virtual para resolver los cuadruplos generados por el parser, 
# se usara una pila para manejar los operandos y operadores

from cuadruplos import cuadruplos

def interpretar():
    memoria = {}  # Memoria para almacenar variables y sus valores
    cuadruplo_index = 0 #Apunta al cuadruplo actual

    def obtener_valor(val):
        if val is None:
            return None
        if isinstance(val, (int, float, bool)):
            return val
        if isinstance(val,str) and val in memoria:
            return memoria[val]
        return val  # Si no es una variable, se asume que es un literal
    
    while cuadruplo_index < len(cuadruplos):
        operador, operando1, operando2, resultado = cuadruplos[cuadruplo_index]
        
        if operador == ':=':
            memoria[resultado] = obtener_valor(operando1)

        elif operador == 'Goto':
            cuadruplo_index = resultado
            continue
        elif operador == 'GotoF':
            if not obtener_valor(operando1):
                cuadruplo_index = resultado
                continue
        elif operador == 'GotoV':
            if obtener_valor(operando1):
                cuadruplo_index = resultado
                continue
        elif operador in ('+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=', 'and', 'or'):
            val1 = obtener_valor(operando1)
            val2 = obtener_valor(operando2)
            if operador == '+':
                memoria[resultado] = val1 + val2
            elif operador == '-':
                memoria[resultado] = val1 - val2
            elif operador == '*':
                memoria[resultado] = val1 * val2
            elif operador == '/':
                memoria[resultado] = val1 / val2
            elif operador == '==':
                memoria[resultado] = val1 == val2
            elif operador == '!=':
                memoria[resultado] = val1 != val2
            elif operador == '<':
                memoria[resultado] = val1 < val2
            elif operador == '>':
                memoria[resultado] = val1 > val2
            elif operador == '<=':
                memoria[resultado] = val1 <= val2
            elif operador == '>=':
                memoria[resultado] = val1 >= val2
            elif operador == 'and':
                memoria[resultado] = val1 and val2
            elif operador == 'or':
                memoria[resultado] = val1 or val2
        
        elif operador == 'NOT':
            memoria[resultado] = not obtener_valor(operando1)
        elif operador == 'WRITELN':
            print(obtener_valor(resultado))
        else:
            raise Exception(f"Error: Operador '{operador}' no reconocido en la interpretación.")
        
        cuadruplo_index += 1


interpretar()

