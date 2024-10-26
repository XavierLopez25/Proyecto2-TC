def CNFtoCYKConverter(cnf_grammar, w):
    n = len(w)
    if n == 0:
        return False

    table = [[set() for _ in range(n)] for _ in range(n)]
    productions = cnf_grammar["productions"]

    for i in range(n):
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] == w[i]:
                    table[i][i].add(lhs)
                    print(f"Agregando {lhs} a table[{i}][{i}] porque deriva {w[i]}")

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for lhs, rhs_list in productions.items():
                    for rhs in rhs_list:
                        if len(rhs) == 2:
                            B, C = rhs
                            if B in table[i][k] and C in table[k + 1][j]:
                                table[i][j].add(lhs)
                                print(
                                    f"Agregando {lhs} a table[{i}][{j}] porque {B} está en table[{i}][{k}] y {C} en table[{k + 1}][{j}]")

    print("\nTabla CYK Completa:")
    for row in table:
        print(row)

    return cnf_grammar["startSymbol"] in table[0][n - 1]