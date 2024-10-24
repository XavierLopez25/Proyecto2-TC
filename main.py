import json
import re
from src.CFGToCNF.CFGToCNF import CFGtoCNFConverter

def main():
    # Nombre del archivo de entrada
    input_filename = 'grammars/CFG/cfg_grammar2.json'

    # Leer la gramática desde el archivo JSON
    with open(input_filename, 'r') as file:
        grammar = json.load(file)

    # Crear una instancia del convertidor y ejecutar la conversión
    converter = CFGtoCNFConverter(grammar)
    cnf_grammar = converter.convert()

    # Extraer el número del nombre del archivo de entrada
    match = re.search(r'\d+', input_filename)
    if match:
        number = match.group()
    else:
        number = ''

    # Construir el nombre del archivo de salida
    output_filename = f'cnf_grammar{number}.json'

    if cnf_grammar is not None:
        # Guardar la gramática CNF resultante en un nuevo archivo JSON
        with open(f'grammars/CNF/{output_filename}', 'w') as file:
            json.dump(cnf_grammar, file, indent=2)

        # Informar al usuario que el proceso ha finalizado
        print(f"\n\nLa gramática ha sido convertida a CNF y guardada en '{output_filename}'.\n\n")
    else:
        # Informar al usuario que la conversión no fue posible
        print("\nNo se pudo convertir la gramática a CNF porque no es una CFG válida.")


main()