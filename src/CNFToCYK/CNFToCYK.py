def CNFtoCYKConverter(cnf_grammar, w):
    """
    Implementa el algoritmo CYK para verificar si una cadena w es parte del lenguaje
    generado por la gramática cnf_grammar.

    :param cnf_grammar: Gramática en Forma Normal de Chomsky (CNF)
    :param w: Cadena de entrada (lista de terminales)
    :return: True si w es aceptada por la gramática, False en caso contrario
    """
    n = len(w)  # Longitud de la cadena de entrada

    # Manejar el caso de cadena vacía
    if n == 0:
        return False

    # Crear una tabla 2D para el algoritmo CYK
    table = [[set() for _ in range(n)] for _ in range(n)]

    # Obtener las producciones en formato CNF
    productions = cnf_grammar["productions"]

    # Rellenar la diagonal (producciones unitarias) con terminales
    for i in range(n):
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] == w[i]:  # Si la producción es un terminal
                    table[i][i].add(lhs)
                    print(f"Agregando {lhs} a table[{i}][{i}] porque deriva {w[i]}")

    # Rellenar la tabla usando programación dinámica para combinaciones de subcadenas
    for length in range(2, n + 1):  # Tamaño de subcadena
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                # Iterar sobre todas las producciones y verificar combinaciones de B y C
                for lhs, rhs_list in productions.items():
                    for rhs in rhs_list:
                        if len(rhs) == 2:  # Producción binaria
                            B, C = rhs
                            if B in table[i][k] and C in table[k + 1][j]:
                                table[i][j].add(lhs)
                                print(
                                    f"Agregando {lhs} a table[{i}][{j}] porque {B} está en table[{i}][{k}] y {C} en table[{k + 1}][{j}]")

    # Depuración final: Imprimir la tabla completa para confirmar la estructura final
    print("\nTabla CYK Completa:")
    for row in table:
        print(row)

    # Verificar si el símbolo inicial está en la celda superior derecha [0, n-1]
    return cnf_grammar["startSymbol"] in table[0][n - 1]