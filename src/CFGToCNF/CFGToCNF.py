import json
import copy

class CFGtoCNFConverter:
    def __init__(self, grammar):
        # Inicialización de la clase con los componentes de la gramática
        self.terminals = set(grammar["terminals"])  # Conjunto de terminales
        self.non_terminals = set(grammar["nonTerminals"])  # Conjunto de no terminales
        self.start_symbol = grammar.get("startSymbol", "S")  # Símbolo inicial
        self.productions = grammar["productions"]  # Producciones originales
        self.new_productions = {}  # Producciones modificadas durante la conversión
        self.counter = 0  # Contador para generar nuevos símbolos no terminales únicos

    def is_cfg(self):
        """
        Verifica si la gramática es una Gramática Libre de Contexto (CFG).
        Retorna True si es una CFG, False en caso contrario.
        """
        # Verificar que todos los LHS son símbolos no terminales individuales
        for lhs in self.productions:
            # Comprobar que el LHS es un símbolo definido en los no terminales
            if lhs not in self.non_terminals:
                print(f"Error: El símbolo '{lhs}' en el LHS no está en los no terminales.")
                return False
            # Comprobar que el LHS es un único símbolo (no una cadena de símbolos)
            if len(lhs.strip().split()) != 1:
                print(f"Error: El LHS '{lhs}' no es un único símbolo.")
                return False

            # Verificar que las producciones son listas de listas
            if not isinstance(self.productions[lhs], list):
                print(f"Error: Las producciones de '{lhs}' deben ser una lista.")
                return False
            for production in self.productions[lhs]:
                if not isinstance(production, list):
                    print(f"Error: La producción '{production}' de '{lhs}' debe ser una lista de símbolos.")
                    return False
                # Verificar que los símbolos en el RHS están definidos
                for symbol in production:
                    if symbol not in self.non_terminals and symbol not in self.terminals and symbol != "ε":
                        print(f"Error: El símbolo '{symbol}' en la producción de '{lhs}' no está definido en terminales o no terminales.")
                        return False
        # Si todas las comprobaciones pasan, es una CFG
        return True


    def convert(self):
        # Verificar si la gramática es una CFG antes de convertir
        if not self.is_cfg():
            print("\nLa gramática proporcionada no es una Gramática Libre de Contexto (CFG).")
            return None

        # Método principal que ejecuta todos los pasos de la conversión
        self.remove_start_symbol_from_rhs()  # Paso 1
        self.remove_null_productions()       # Paso 2
        self.remove_unit_productions()       # Paso 3
        self.remove_useless_symbols()        # Paso 4 (opcional)
        self.convert_to_cnf()                # Paso 5
        return {
            "startSymbol": self.start_symbol,
            "nonTerminals": list(self.non_terminals),
            "terminals": list(self.terminals),
            "productions": self.new_productions
        }

    def remove_start_symbol_from_rhs(self):
        """
        Paso 1: Eliminar el símbolo inicial del lado derecho de las producciones.
        Si el símbolo inicial aparece en el RHS de alguna producción, se crea
        un nuevo símbolo inicial y se agrega una producción que deriva al antiguo
        símbolo inicial.
        """
        # Verificar si el símbolo inicial aparece en el lado derecho de alguna producción
        start_in_rhs = any(
            self.start_symbol in production for productions in self.productions.values() for production in productions
        )
        if start_in_rhs:
            # Crear un nuevo símbolo inicial que no esté en el conjunto de no terminales
            new_start = "S0"
            while new_start in self.non_terminals:
                new_start = f"S{self.counter}"
                self.counter += 1
            # Agregar el nuevo símbolo inicial al conjunto de no terminales
            self.non_terminals.add(new_start)
            # Agregar una producción que deriva al antiguo símbolo inicial
            self.productions[new_start] = [[self.start_symbol]]
            # Actualizar el símbolo inicial
            self.start_symbol = new_start
        # Hacer una copia de las producciones para trabajar en ellas
        self.new_productions = copy.deepcopy(self.productions)

    def remove_null_productions(self):
        """
        Paso 2: Eliminar producciones nulas (ε-productions).
        Identificar los símbolos que pueden derivar a ε y actualizar las
        producciones para eliminar las producciones nulas, agregando nuevas
        producciones sin estos símbolos.
        """
        # Encontrar los símbolos que producen ε directamente
        nullables = set()
        for nt in self.non_terminals:
            for production in self.new_productions.get(nt, []):
                if production == ["ε"] or production == []:
                    nullables.add(nt)

        # Propagar la nulabilidad a otros símbolos
        changed = True
        while changed:
            changed = False
            for nt in self.non_terminals:
                for production in self.new_productions.get(nt, []):
                    if all(symbol in nullables for symbol in production):
                        if nt not in nullables:
                            nullables.add(nt)
                            changed = True

        # Eliminar las producciones nulas y generar nuevas combinaciones
        updated_productions = {}
        for nt in self.non_terminals:
            updated_rules = []
            for production in self.new_productions.get(nt, []):
                if production != ["ε"] and production != []:
                    # Obtener todas las combinaciones posibles sin los símbolos anulables
                    combinations = self.get_nullable_combinations(production, nullables)
                    updated_rules.extend(combinations)
            # Eliminar duplicados y actualizar las producciones
            updated_productions[nt] = [
                list(p) for p in set(tuple(r) for r in updated_rules)
            ]
        self.new_productions = updated_productions

    def get_nullable_combinations(self, production, nullables):
        """
        Método auxiliar para obtener todas las combinaciones posibles de una
        producción excluyendo los símbolos anulables.
        """
        from itertools import combinations

        positions = [i for i, symbol in enumerate(production) if symbol in nullables]
        combinations_list = []

        # Generar todas las combinaciones posibles de exclusión de símbolos anulables
        for i in range(len(positions) + 1):
            for indices in combinations(positions, i):
                new_prod = [
                    symbol for j, symbol in enumerate(production) if j not in indices
                ]
                if new_prod:
                    combinations_list.append(new_prod)
        if not combinations_list:
            combinations_list.append(production)
        return combinations_list

    def remove_unit_productions(self):
        """
        Paso 3: Eliminar producciones unitarias (A -> B donde A y B son no terminales).
        Se reemplazan por las producciones de B.
        """
        # Encontrar todas las producciones unitarias
        unit_pairs = set()
        for nt in self.non_terminals:
            for production in self.new_productions.get(nt, []):
                if len(production) == 1 and production[0] in self.non_terminals:
                    unit_pairs.add((nt, production[0]))

        # Calcular el cierre transitivo de las producciones unitarias
        changed = True
        while changed:
            changed = False
            new_pairs = set()
            for (a, b) in unit_pairs:
                for (c, d) in unit_pairs:
                    if b == c and (a, d) not in unit_pairs:
                        new_pairs.add((a, d))
                        changed = True
            unit_pairs.update(new_pairs)

        # Reemplazar las producciones unitarias por las producciones correspondientes
        updated_productions = {}
        for nt in self.non_terminals:
            # Mantener las producciones que no son unitarias
            updated_rules = [
                p
                for p in self.new_productions.get(nt, [])
                if not (len(p) == 1 and p[0] in self.non_terminals)
            ]
            # Agregar las producciones de los no terminales alcanzables
            unit_targets = [b for (a, b) in unit_pairs if a == nt]
            for target in unit_targets:
                for production in self.new_productions.get(target, []):
                    if production != [nt]:
                        updated_rules.append(production)
            # Eliminar duplicados y actualizar las producciones
            updated_productions[nt] = [
                list(p) for p in set(tuple(r) for r in updated_rules)
            ]
        self.new_productions = updated_productions

    def remove_useless_symbols(self):
        """
        Paso 4: Eliminar símbolos inútiles.
        Este paso puede ser complejo; para simplificar, asumimos que todos los símbolos
        son útiles y no implementamos este paso. Sin embargo, en una implementación
        completa, deberías eliminar los símbolos que no generan cadenas de terminales
        o que no son alcanzables desde el símbolo inicial.
        """
        pass  # Se puede implementar según sea necesario

    def convert_to_cnf(self):
        """
        Paso 5: Convertir las producciones a la Forma Normal de Chomsky.
        Se aseguran que todas las producciones tengan una longitud de RHS de 2 o menos,
        y que los terminales no aparezcan en producciones con RHS de longitud mayor a 1.
        """
        # Reemplazar terminales en RHS de longitud > 1 con no terminales
        terminal_map = {}
        # Crear una copia de los no terminales para la iteración
        non_terminals_copy = list(self.non_terminals)
        for nt in non_terminals_copy:
            updated_rules = []
            for production in self.new_productions.get(nt, []):
                # Si la producción es de longitud 1 y es un terminal, se mantiene
                if len(production) == 1 and production[0] in self.terminals:
                    updated_rules.append(production)
                else:
                    # Reemplazar terminales por no terminales nuevos
                    new_prod = []
                    for symbol in production:
                        if symbol in self.terminals:
                            if symbol not in terminal_map:
                                # Crear un nuevo no terminal para el terminal
                                new_nt = self.get_new_non_terminal()
                                self.non_terminals.add(new_nt)
                                self.new_productions[new_nt] = [[symbol]]
                                terminal_map[symbol] = new_nt
                            new_prod.append(terminal_map[symbol])
                        else:
                            new_prod.append(symbol)
                    updated_rules.append(new_prod)
            self.new_productions[nt] = updated_rules

        # Convertir producciones con RHS de longitud > 2 a producciones binarias
        updated_productions = {}
        # Crear una copia actualizada de los no terminales para la iteración
        non_terminals_copy = list(self.non_terminals)
        for nt in non_terminals_copy:
            updated_rules = []
            for production in self.new_productions.get(nt, []):
                # Mientras la producción tenga más de 2 símbolos, descomponerla
                while len(production) > 2:
                    first, rest = production[0], production[1:]
                    new_nt = self.get_new_non_terminal()
                    self.non_terminals.add(new_nt)
                    self.new_productions[new_nt] = [rest]
                    production = [first, new_nt]
                updated_rules.append(production)
            updated_productions[nt] = updated_rules
        self.new_productions = updated_productions

    def get_new_non_terminal(self):
        """
        Método auxiliar para generar nuevos símbolos no terminales únicos.
        """
        while True:
            new_nt = f"X{self.counter}"
            self.counter += 1
            if new_nt not in self.non_terminals:
                return new_nt
