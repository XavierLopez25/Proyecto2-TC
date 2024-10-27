import unittest
from CYKToParseTree import build_parse_tree, visualize_parse_tree


class TestParseTree(unittest.TestCase):

    def setUp(self):
        # Configuración de ejemplo para una gramática en CNF
        self.cnf_grammar = {
            "startSymbol": "S",
            "productions": {
                "S": [["NP", "VP"]],
                "NP": [["Det", "N"]],
                "VP": [["V", "NP"]],
                "Det": [["a"]],
                "N": [["dog"]],
                "V": [["sees"]]
            }
        }
        # Configurar una tabla CYK de ejemplo
        self.table = [
            [[{"symbol": "Det", "children": [{"symbol": "a", "children": []}]}], [], []],
            [[], [{"symbol": "N", "children": [{"symbol": "dog", "children": []}]}], []],
            [[], [], [{"symbol": "V", "children": [{"symbol": "sees", "children": []}]}]],
            [[], [], []]
        ]
        # Ajustar la tabla para que contenga el símbolo de inicio en la posición correcta
        self.table[0][2] = [{"symbol": "S", "children": [self.table[0][0][0], self.table[2][2][0]]}]

    def test_build_parse_tree_valid(self):
        # Este test debería pasar si la tabla está correctamente configurada y la función maneja bien los datos
        parse_tree = build_parse_tree(self.table, self.cnf_grammar, ["a", "dog", "sees"])
        self.assertIsNotNone(parse_tree)
        self.assertEqual(parse_tree['symbol'], 'S')

    def test_build_parse_tree_invalid(self):
        # Test para verificar el manejo de una tabla CYK sin el símbolo de inicio
        self.table[0][2] = []  # Simular una tabla sin el símbolo de inicio en la posición correcta
        parse_tree = build_parse_tree(self.table, self.cnf_grammar, ["a", "dog", "sees"])
        self.assertIsNone(parse_tree)

    def test_visualize_parse_tree(self):
        # Asegurarse de que el árbol se construye antes de visualizarlo
        parse_tree = build_parse_tree(self.table, self.cnf_grammar, ["a", "dog", "sees"])
        self.assertIsNotNone(parse_tree)  # Verifica primero que el árbol no sea None
        graph = visualize_parse_tree(parse_tree)
        self.assertIsNotNone(graph)
        self.assertIn('S', graph.source)
        self.assertIn('sees', graph.source)

    def test_empty_input(self):
        # Test para verificar cadenas vacías
        parse_tree = build_parse_tree([], self.cnf_grammar, [])
        self.assertIsNone(parse_tree)

    def test_incorrect_cyk_table_structure(self):
        # Tabla CYK con estructura incorrecta o inesperada
        broken_table = [[[]], [{"symbol": "S", "children": []}]]  # Estructura incorrecta
        parse_tree = build_parse_tree(broken_table, self.cnf_grammar, ["the", "dog"])
        self.assertIsNone(parse_tree)

    def test_invalid_data_types(self):
        # Probar con tipos de datos incorrectos en la entrada
        incorrect_data = [123, None, "sees"]  # Tipo de datos incorrecto int y None
        parse_tree = build_parse_tree(self.table, self.cnf_grammar, incorrect_data)
        self.assertIsNone(parse_tree)

if __name__ == '__main__':
    unittest.main()
