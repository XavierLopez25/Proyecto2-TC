import json
import re
import os
import time
from src.CFGToCNF.CFGToCNF import CFGtoCNFConverter
from src.CNFToCYK.CNFToCYK import CNFtoCYKConverter
from src.CYKToParseTree import CYKToParseTree

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

        print("+-" * 40, end='+\n')
        print(f"\nLa gramática ha sido convertida a CNF y guardada en '{output_filename}'.\n")
        print("+-" * 40, end='+')

        # Cargar la gramática CNF para usarla en el algoritmo CYK
        cnf_input_filename = f'grammars/CNF/{output_filename}'
        with open(cnf_input_filename, 'r') as file:
            cnf_grammar = json.load(file)

        # Solicitar la cadena de entrada al usuario
        w = input("\n\nIngrese una cadena (separada por espacios): ").split()

        os.system('clear')

        # Medir el tiempo de todo el proceso de validación
        start_time = time.perf_counter()

        # Ejecutar el algoritmo CYK para verificar si la cadena pertenece al lenguaje
        table, is_valid = CNFtoCYKConverter(cnf_grammar, w)

        # Mostrar el resultado de la validación
        if is_valid:
            print("+-" * 40, end='+\n')
            print(f"\nLa cadena '{' '.join(w)}' SÍ pertenece al lenguaje generado por la gramática. ✅\n")
            print("+-" * 40, end='+\n')

            # Guardar el resultado del algoritmo CYK en un archivo JSON
            cyk_output_filename = f'cyk_result_{number}.json'
            cyk_result = {
                "cadena": " ".join(w),
                "resultado": "SI"
            }
            with open(f'grammars/CYK/{cyk_output_filename}', 'w') as file:
                json.dump(cyk_result, file, indent=2)

            print(f"\nEl resultado del análisis CYK se ha guardado en '{cyk_output_filename}'.\n")
            print("+-" * 40, end='+\n')

            print("\n La tabla del CYK es: \n")
            print(table)
        
            print("+-" * 40, end='+\n')

            # Construir el árbol de análisis si la cadena pertenece al lenguaje
            parse_tree = CYKToParseTree.build_parse_tree(table, cnf_grammar, w)
            if parse_tree:
                output_dir = 'grammars/ParseTreeCYK'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                parse_tree_output_filename = f'parse_tree_result{number}'
                print("\nÁrbol de análisis encontrado.")
                print("-" * 81)
                tree_graph = CYKToParseTree.visualize_parse_tree(parse_tree)
                tree_graph.render(os.path.join(output_dir, parse_tree_output_filename), format='png', view=True)
                print(" ")
            else:
                print("\n No se pudo construir un árbol de análisis.")
        else:
            print("+-" * 40, end='+\n')
            print(f"\nLa cadena '{' '.join(w)}' NO pertenece al lenguaje generado por la gramática. ❌\n")
            print("+-" * 40, end='+\n')
            return 

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print("+-" * 40, end='+\n')
        print(f"\n ⌛️ Tiempo de ejecución total: {execution_time:.8f} segundos.\n")
        print("+-" * 40, end='+\n')

    else:
        print("\nNo se pudo convertir la gramática a CNF porque no es una CFG válida.")

if __name__ == "__main__":
    main()
