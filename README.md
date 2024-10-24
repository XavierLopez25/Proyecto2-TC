# Proyecto #2 - Teoría de la Computación

## Propósito del programa
- Inserte propósito acá 

## ¿Cómo utilizar el programa?

### grammars/CFG:
- Aquí se colocarán las gramáticas en formato JSON, este es un ejemplo:

```json
{
  "productions": {
    "S": [["NP", "VP"]],
    "VP": [["V", "NP"], ["VP", "PP"]],
    "PP": [["P", "NP"]],
    "NP": [["Det", "N"], ["he"], ["she"]],
    "V": [["cooks"], ["drinks"], ["eats"], ["cuts"]],
    "P": [["in"], ["with"]],
    "N": [["cat"], ["dog"], ["beer"], ["cake"], ["juice"], ["meat"], ["soup"], ["fork"], ["knife"], ["oven"], ["spoon"]],
    "Det": [["a"], ["the"]]
  },
  "terminals": ["he", "she", "cooks", "drinks", "eats", "cuts", "in", "with", "cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon", "a", "the"],
  "nonTerminals": ["S", "VP", "PP", "NP", "V", "P", "N", "Det"]
}
```
- Nota: Cuando se encuentra un no terminal, por ejemplo ```S``` con asignación de ```[["NP", "VP"]]```, quiere decir que: ```S -> NP VP```. Ahora cuando se encuentra un no terminal como ```N``` con asignación de ```[["cat"], ["dog"], ["beer"], ...]```m quiere decir que: ```N -> cat | dog | beer | ...```

### main.py:
- Para poder utilizar este programa es necesario que se ingrese una _Context Free Grammar (Gramática Libre de Contexto)_
- Esta se debe de cambiar en este archivo, en la variable llamada ```input_filename```.
- La gramática de entrada debe de encontrarse en ```grammars/CFG/cfg_grammarX.json```.
- La gramática en CNF transformada se encontrará en ```grammars/CNF/cnf_grammarX.json```.

### CFGToCNF.py:
- Este archivo se encarga de identificar en primera instancia si la gramática ingresada en formato JSON, es de libre contexto o no.
- Si la gramática es aceptada se realizará el proceso de conversión y se guardará en un archivo.

### Agregar aquí descripciones para los demás archivos

## Integrantes:

- Diego Valenzuela
- Gerson Ramírez
- Nahomy Castro
- Xavier López
