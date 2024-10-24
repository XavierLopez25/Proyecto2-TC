
import unittest

from src.CFGToCNF.CFGToCNF import CFGtoCNFConverter

class TestCFGtoCNFConverter(unittest.TestCase):

    def test_valid_cfg_conversion_1(self):
        grammar = {
            "startSymbol": "S",
            "nonTerminals": ["S", "A"],
            "terminals": ["a", "b"],
            "productions": {
                "S": [["A", "a"]],
                "A": [["b"]]
            }
        }
        converter = CFGtoCNFConverter(grammar)
        cnf_grammar = converter.convert()
        self.assertIsNotNone(cnf_grammar)
        self.assertIn("productions", cnf_grammar)

    def test_valid_cfg_conversion_2(self):
        grammar = {
            "startSymbol": "S",
            "nonTerminals": ["S", "VP", "PP", "NP", "V", "P", "N", "Det"],
            "terminals": ["he", "she", "cooks", "drinks", "eats", "cuts", "in", "with", "cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon", "a", "the"],
            "productions": {
                "S": [["NP", "VP"]],
                "VP": [["V", "NP"], ["VP", "PP"]],
                "PP": [["P", "NP"]],
                "NP": [["Det", "N"], ["he"], ["she"]],
                "V": [["cooks"], ["drinks"], ["eats"], ["cuts"]],
                "P": [["in"], ["with"]],
                "N": [["cat"], ["dog"], ["beer"], ["cake"], ["juice"], ["meat"], ["soup"], ["fork"], ["knife"], ["oven"], ["spoon"]],
                "Det": [["a"], ["the"]]
            }
        }
        converter = CFGtoCNFConverter(grammar)
        cnf_grammar = converter.convert()
        self.assertIsNotNone(cnf_grammar)
        self.assertIn("productions", cnf_grammar)

    def test_invalid_cfg_conversion_invalid_lhs(self):
        grammar = {
            "startSymbol": "S",
            "nonTerminals": ["S", "A"],
            "terminals": ["a", "b"],
            "productions": {
                "S": [["A", "a"]],
                "A B": [["b"]]  # Invalid LHS
            }
        }
        converter = CFGtoCNFConverter(grammar)
        cnf_grammar = converter.convert()
        self.assertIsNone(cnf_grammar)

    def test_invalid_cfg_conversion_invalid_rhs(self):
        grammar = {
            "startSymbol": "S",
            "nonTerminals": ["S", "A"],
            "terminals": ["a", "b"],
            "productions": {
                "S": [["A", "a"]],
                "A": [["b", "C"]]  # Invalid RHS (C is not defined)
            }
        }
        converter = CFGtoCNFConverter(grammar)
        cnf_grammar = converter.convert()
        self.assertIsNone(cnf_grammar)


if __name__ == "__main__":
    unittest.main()
