import unittest
from pckg.source.linear_formula import LinearFormula

class TestOther(unittest.TestCase):

    #-TEST-OTHER--------------------------------------------------------------
    
    #-------------------------------------------------------------------------
    def test_length(self):

        test_data = [
            #formula               length
            ('a + 3b - 4c',             3),
            ('a + b - c',               3),
            ('1 + 2 - 3',               3),
            ('a + 3b - 4c + 3a',        4),
            ('a + 7b - 0c - 4d + 1',    5),
            ('-a + 4c',                 2),
            ('',                        0),
            ('a',                       1),
            ('6',                       1),
            ('ab + 3cd - 34ef',         3),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            self.assertEqual(formula.length(), info[1])
    
    #-------------------------------------------------------------------------
    def test_copy(self):
        formula = LinearFormula('a + b + 4c')
        copy_of_formula = formula.copy()
        copy_of_formula.add_segment(3, 'd', inplace=True)
        self.assertNotEqual(formula, copy_of_formula)

    #-------------------------------------------------------------------------
    def test_get_segment(self):

        test_data = [
            #initial formula            expected segment
            #                   index
            ('a + 3b - 4c',     1,      (3, 'b')    ),
            ('a + 3b - 4c',     2,      (-4, 'c')   ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            segment = formula.get_segment(info[1])
            self.assertEqual(segment, info[2])

    #-------------------------------------------------------------------------
    def test_evaluate(self):

        test_data = [
            #formula            values                      expected result
            ('1',               {'a': 5},                   1   ),
            ('1',               {},                         1   ),
            ('a',               {'a': 5},                   5   ),
            ('a + b + c',       {'a': 1, 'b': 1, 'c': 1},   3   ),
            ('a + b',           {'a': 1, 'b': 1, 'c': 1},   2   ),
            ('a + 3b - 4c',     {'a': 1, 'b': 1, 'c': 1},   0   ),
            ('a + 3b - 4c',     {'a': 2, 'b': 2, 'c': 3},   -4  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            value = formula.evaluate(**info[1])
            self.assertEqual(value, info[2])

        #errors    
        test_data = [
            #formula            values                      expected result
            ('a',               {},                         TypeError   ),
            ('a + b + c',       {'a': 1, 'b': 1},           TypeError   ),
            ('a + 3b - 4c',     {'a': 1, 'c': 1},           TypeError   ),
            ('a + 3b - 4c',     {'a': 2, 'b': 2, 'd': 3},   TypeError   ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            self.assertRaises(info[2], formula.evaluate, **info[1])

    #-------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()