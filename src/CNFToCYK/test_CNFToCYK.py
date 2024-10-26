import unittest
from src.CNFToCYK.CNFToCYK import CNFtoCYKConverter

class TestCNFtoCYKAlgorithm(unittest.TestCase):

    def setUp(self):
        # Gramática en Forma Normal de Chomsky (CNF) para las pruebas
        self.cnf_grammar = {
            "startSymbol": "S",
            "nonTerminals": ["S", "VP", "NP", "V", "Det", "N", "P", "PP"],
            "terminals": ["he", "she", "cooks", "drinks", "eats", "in", "with", "cake"],
            "productions": {
                "S": [["NP", "VP"]],
                "VP": [["V", "NP"], ["VP", "PP"]],
                "PP": [["P", "NP"]],
                "NP": [["Det", "N"], ["he"], ["she"]],
                "V": [["cooks"], ["drinks"], ["eats"]],
                "P": [["in"], ["with"]],
                "N": [["cake"]]
            }
        }

    def test_valid_sentence_1(self):
        # Cadena válida que debería ser aceptada por la gramática
        sentence = ["she", "eats", "cake"]
        result = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertTrue(result)

    def test_valid_sentence_2(self):
        # Otra cadena válida que debería ser aceptada por la gramática
        sentence = ["he", "drinks", "cake"]
        result = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertTrue(result)

    def test_invalid_sentence_1(self):
        # Cadena inválida que no debería ser aceptada por la gramática
        sentence = ["she", "eats", "he"]
        result = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertFalse(result)

    def test_invalid_sentence_2(self):
        # Otra cadena inválida que no debería ser aceptada por la gramática
        sentence = ["he", "eats", "with", "cake"]
        result = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertFalse(result)

    def test_empty_sentence(self):
        # Prueba con una cadena vacía; resultado esperado depende de la gramática
        sentence = []
        result = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
