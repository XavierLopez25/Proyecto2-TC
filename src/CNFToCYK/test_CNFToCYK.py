import unittest
from src.CNFToCYK.CNFToCYK import CNFtoCYKConverter

class TestCNFtoCYKAlgorithm(unittest.TestCase):

    def setUp(self):
        # Gramática en Forma Normal de Chomsky (CNF) para las pruebas
        self.cnf_grammar = {
            "startSymbol": "S",
            "nonTerminals": ["S", "VP", "NP_Subj", "NP_Obj", "V", "Det", "N", "P", "PP", "NP"],
            "terminals": ["he", "she", "him", "her", "cooks", "drinks", "eats", "cuts", "in", "with", "a", "the",
                          "cake", "dog", "cat", "beer"],
            "productions": {
                "S": [["NP_Subj", "VP"]],
                "VP": [["V", "NP_Obj"], ["VP", "PP"], ["V"]],
                "PP": [["P", "NP"]],
                "NP_Subj": [["he"], ["she"], ["NP"]],
                "NP_Obj": [["Det", "N"], ["N"]],
                "NP": [["Det", "N"], ["N"]],
                "V": [["cooks"], ["drinks"], ["eats"], ["cuts"]],
                "P": [["in"], ["with"]],
                "N": [["cat"], ["dog"], ["beer"], ["cake"]],
                "Det": [["a"], ["the"]]
            }
        }

    def test_valid_sentence_1(self):
        # Cadena válida que debería ser aceptada por la gramática
        sentence = ["she", "eats", "a", "cake"]
        _, is_valid = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertTrue(is_valid)

    def test_valid_sentence_2(self):
        # Otra cadena válida que debería ser aceptada por la gramática
        sentence = ["he", "drinks", "the", "beer"]
        _, is_valid = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertTrue(is_valid)

    def test_invalid_sentence_1(self):
        # Cadena inválida que no debería ser aceptada por la gramática
        sentence = ["she", "eats", "he"]
        _, is_valid = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertFalse(is_valid)

    def test_invalid_sentence_2(self):
        # Otra cadena inválida que no debería ser aceptada por la gramática
        sentence = ["he", "eats", "with", "cake"]
        _, is_valid = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertFalse(is_valid)

    def test_empty_sentence(self):
        # Prueba con una cadena vacía; resultado esperado depende de la gramática
        sentence = []
        _, is_valid = CNFtoCYKConverter(self.cnf_grammar, sentence)
        self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
