def CNFtoCYKConverter(cnf_grammar, w):
    n = len(w)
    if n == 0:
        return cnf_grammar["startSymbol"] in cnf_grammar.get("epsilon", set())

    # Inicializar la tabla CYK
    table = [[set() for _ in range(n)] for _ in range(n)]
    productions = cnf_grammar["productions"]

    # Rellenar la tabla para las subcadenas de longitud 1 (los terminales)
    for i in range(n):
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] == w[i]:
                    table[i][i].add(lhs)

    # Rellenar la tabla para subcadenas de longitud > 1
    for l in range(2, n + 1):  # Longitud de la subcadena
        for i in range(n - l + 1):  # Inicio de la subcadena
            j = i + l - 1  # Fin de la subcadena
            for k in range(i, j):  # División de la subcadena
                for lhs, rhs_list in productions.items():
                    for rhs in rhs_list:
                        if len(rhs) == 2:
                            B, C = rhs
                            if B in table[i][k] and C in table[k + 1][j]:
                                table[i][j].add(lhs)

    # Verificar si el símbolo inicial está en la posición [0][n-1]
    return cnf_grammar["startSymbol"] in table[0][n - 1]

