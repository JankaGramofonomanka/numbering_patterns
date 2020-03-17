import unittest
from numbering_patterns.source.linear_formula import LinearFormula

class TestInit(unittest.TestCase):

    #-TEST-INITIALIZATION-----------------------------------------------------

    #-------------------------------------------------------------------------
    def test_init_with_string(self):

        test_data = [
            #init string            expected        expected
            #                       multipliers     variables
            ('a + 3b - 4c',         [1, 3, -4],     ['a', 'b', 'c']     ),
            ('a+3b-4c+3a',          [1, 3, -4, 3],  ['a', 'b', 'c', 'a']),
            (' a  +7b-  0c -4d ',   [1, 7, 0, -4],  ['a', 'b', 'c', 'd']),
            ('-a + 4c + 3b - 4c',   [-1, 4, 3, -4], ['a', 'c', 'b', 'c']),
            ('',                    [],             []                  ),
            ('a',                   [1],            ['a']               ),
            ('6',                   [6],            ['']                ),
            ('ab + 3cd - 34ef',     [1, 3, -34],    ['ab', 'cd', 'ef']  ),
            ('x1 + 2x2 - 3x3',      [1, 2, -3],     ['x1', 'x2', 'x3']  ),
            ('x_1 + 2x_2',          [1, 2],         ['x_1', 'x_2']      ),
            ('x_13 + 234x_254',     [1, 234],       ['x_13', 'x_254']   ),
            ('3x1 + 2x2',           [3, 2],         ['x1', 'x2']        ),
            ('3x1 + x2 + x3',       [3, 1, 1],      ['x1', 'x2', 'x3']  ),
            ('3x1 + 1x2 + 1x3',     [3, 1, 1],      ['x1', 'x2', 'x3']  ),
            ('-x1 - 1x2 - x3',      [-1, -1, -1],   ['x1', 'x2', 'x3']  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            self.assertEqual(formula.multipliers, info[1])
            self.assertEqual(formula.variables, info[2])

    #-------------------------------------------------------------------------
    def test_init_with_dict(self):

        test_data = [
            #init dict
            {'a': 1, 'b': 3, 'c': -4},
        ]

        for init_data in test_data:
            formula = LinearFormula(init_data)
            self.assertEqual(formula.multipliers, list(init_data.values()))
            self.assertEqual(formula.variables, list(init_data.keys()))

    #-------------------------------------------------------------------------
    def test_init_with_int(self):

        test_data = [3, '3', 0, 23, '23']

        for init_data in test_data:
            formula = LinearFormula(init_data)
            self.assertEqual(formula.multipliers, [int(init_data)])
            self.assertEqual(formula.variables, [''])

    #-------------------------------------------------------------------------
    def test_init_with_lists(self):

        test_data = [
            #init multipliers   init variables
            ([1, 3, -4],        ['a', 'b', 'c']     ),
            ([1, 3, -4, 3],     ['a', 'b', 'c', 'a']),
            ([1, 7, 0, -4],     ['a', 'b', 'c', 'd']),
            ([-1, 4, 3, -4],    ['a', 'c', 'b', 'c']),
            ([],                []                  ),
            ([1],               ['a']               ),
            ([6],               ['']                ),
            ([1, 3, -34],       ['ab', 'cd', 'ef']  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0], info[1])
            self.assertEqual(formula.multipliers, info[0])
            self.assertEqual(formula.variables, info[1])
    
    #-------------------------------------------------------------------------
    def test_init_wrong(self):

        test_data = [
            (([1, 3, -4],       ['a', 'b', 'c'],    3   ),  TypeError   ),
            (('a + 3b - 4c',    7                       ),  TypeError   ),
            (('a + 3b - 4c',    ['a', 'b', 'c']         ),  TypeError   ),
            ((7,                7                       ),  TypeError   ),
            (([-1, 4, 3, -4],   'a + b + c'             ),  TypeError   ),
            (([1, 3, -4],       ['a', 'b']              ),  ValueError  ),
            (([1, 3],           ['a', 'b', 'c']         ),  ValueError  ),
        ]

        for info in test_data:
            args = info[0]
            error = info[1]
            self.assertRaises(error, LinearFormula, *args)
    
    #-------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()