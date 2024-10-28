def CNFtoCYKConverter(cnf_grammar, w):
    n = len(w)
    if n == 0:
        return [], False  # Retorna tabla vacía y falso


    # Inicializar la tabla CYK
    table = [[[] for _ in range(n)] for _ in range(n)]
    productions = cnf_grammar["productions"]

    # Rellenar la tabla para las subcadenas de longitud 1 (los terminales)
    for i in range(n):
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] == w[i]:
                    table[i][i].append({"symbol": lhs, "children": [{"symbol": rhs[0], "children": []}]})

    # Rellenar la tabla para subcadenas de longitud > 1
    for l in range(2, n + 1):  # Longitud de la subcadena
        for i in range(n - l + 1):  # Inicio de la subcadena
            j = i + l - 1  # Fin de la subcadena
            for k in range(i, j):  # División de la subcadena
                for lhs, rhs_list in productions.items():
                    for rhs in rhs_list:
                        if len(rhs) == 2:
                            B, C = rhs
                            left = [entry for entry in table[i][k] if entry["symbol"] == B]
                            right = [entry for entry in table[k+1][j] if entry["symbol"] == C]
                            for left_entry in left:
                                for right_entry in right:
                                    table[i][j].append({"symbol": lhs, "children": [left_entry, right_entry]})

    # Verificar si el símbolo inicial está en la posición [0][n-1]
    contains_start_symbol = any(entry["symbol"] == cnf_grammar["startSymbol"] for entry in table[0][n-1])
    return table, contains_start_symbol
