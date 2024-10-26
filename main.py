import json
import re
import time 
from src.CFGToCNF.CFGToCNF import CFGtoCNFConverter
from src.CNFToCYK.CNFToCYK import CNFtoCYKConverter

def main():
    # Nombre del archivo de entrada (CFG)
    input_filename = 'grammars/CFG/cfg_grammar1.json'

    # Leer la gramática desde el archivo JSON
    with open(input_filename, 'r') as file:
        grammar = json.load(file)

    # Crear una instancia del convertidor y ejecutar la conversión a CNF
    converter = CFGtoCNFConverter(grammar)
    cnf_grammar = converter.convert()

    # Extraer el número del nombre del archivo de entrada
    match = re.search(r'\d+', input_filename)
    if match:
        number = match.group()
    else:
        number = ''

    # Construir el nombre del archivo de salida para la gramática CNF
    output_filename = f'cnf_grammar{number}.json'

    if cnf_grammar is not None:
        # Guardar la gramática CNF resultante en un nuevo archivo JSON
        with open(f'grammars/CNF/{output_filename}', 'w') as file:
            json.dump(cnf_grammar, file, indent=2)

        # Informar al usuario que el proceso ha finalizado
        print(f"\n\nLa gramática ha sido convertida a CNF y guardada en '{output_filename}'.\n\n")

        # Cargar la gramática CNF para usarla en el algoritmo CYK
        cnf_input_filename = f'grammars/CNF/{output_filename}'
        with open(cnf_input_filename, 'r') as file:
            cnf_grammar = json.load(file)

        # Definir una cadena de entrada
        w = ["she", "eats", "a", "cake"]

        start_time = time.time()  
        # Ejecutar el algoritmo CYK para verificar si la cadena pertenece al lenguaje
        resultado = CNFtoCYKConverter(cnf_grammar, w)
        end_time = time.time()  
        execution_time = end_time - start_time  

        # Mostrar el resultado de la validación
        if resultado:
            print(f"La cadena '{' '.join(w)}' SÍ pertenece al lenguaje generado por la gramática.\n")
        else:
            print(f"La cadena '{' '.join(w)}' NO pertenece al lenguaje generado por la gramática.\n")

        # Guardar el resultado del algoritmo CYK en un archivo JSON
        cyk_output_filename = f'cyk_result_{number}.json'
        cyk_result = {
            "cadena": " ".join(w),
            "resultado": "SI" if resultado else "NO"
        }
        with open(f'grammars/CYK/{cyk_output_filename}', 'w') as file:
            json.dump(cyk_result, file, indent=2)

        print(f"El resultado del análisis CYK se ha guardado en '{cyk_output_filename}'.")

    else:
        # Informar al usuario que la conversión no fue posible
        print("\nNo se pudo convertir la gramática a CNF porque no es una CFG válida.")
        
    print(f"Tiempo de validación con el algoritmo CYK: {execution_time:.4f} segundos.\n")

main()