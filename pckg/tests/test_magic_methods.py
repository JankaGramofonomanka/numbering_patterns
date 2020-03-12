import unittest
from pckg.source.linear_formula import LinearFormula

class TestMagicMethods(unittest.TestCase):

    #-TEST-MAGIC-METHODS------------------------------------------------------
    
    #-------------------------------------------------------------------------
    def test_str(self):

        test_data = [
            #init multipliers   init variables          expected string
            ([1, 3, -4],        ['a', 'b', 'c'],        'a + 3b - 4c'       ),
            ([1, 3, -4, 3],     ['a', 'b', 'c', 'a'],   'a + 3b - 4c + 3a'  ),
            ([1, 7, 0, -4],     ['a', 'b', 'c', 'd'],   'a + 7b + 0c - 4d'  ),
            ([-1, 4, 3, -4],    ['a', 'c', 'b', 'c'],   '-a + 4c + 3b - 4c' ),
            ([],                [],                     '0'                 ),
            ([1],               ['a'],                  'a'                 ),
            ([6],               [''],                   '6'                 ),
            ([1, 3, -34],       ['ab', 'cd', 'ef'],     'ab + 3cd - 34ef'   ),
        ]
        
        for info in test_data:
            formula = LinearFormula(info[0], info[1])
            self.assertEqual(str(formula), info[2])
    
    #-------------------------------------------------------------------------
    def test_eq(self):

        test_data = [
            #init multipliers   init variables
            ([1, 3, -4],        ['a', 'b', 'c']),
            ([],                []             ),
        ]

        for info in test_data:
            formula_1 = LinearFormula(info[0], info[1])
            formula_2 = LinearFormula(info[0], info[1])
            self.assertEqual(formula_1 == formula_2, True)
        
        test_data = [
            # init multipliers  init variables
            (([1, 3, -4],       ['a', 'b', 'c'] ),      # formula 1
             ([2, 5, -7],       ['e', 'f', 'g'] )   ),  # formula 2

            (([1, 1],           ['a', 'b']      ),      # formula 1
             ([1, 1],           ['b', 'a']      )   ),  # formula 2
            
            (([1, 4, 2],        ['a', 'b', 'a'] ),      # formula 1
             ([3, 4],           ['b', 'a']      )   ),  # formula 2
            
            (([1, 2],           ['', '']        ),      # formula 1
             ([2, 1],           ['', '']        )   ),  # formula 2
        ]

        for info in test_data:
            formula_1 = LinearFormula(*info[0])
            formula_2 = LinearFormula(*info[1])
            self.assertFalse(formula_1 == formula_2)
    
    #-------------------------------------------------------------------------
    def test_neg(self):

        test_data = [
            #formula                -formula
            ('a + 3b - 4c',         '-a - 3b + 4c'      ),
            ('a + 3b - 4c + 3a',    '-a - 3b + 4c - 3a' ),
            ('a + 7b - 0c',         '-a - 7b - 0c'      ),
            ('a + 7b - 0c',         '-a - 7b + 0c'      ),
            ('-a + 4c + 3b - 4c',   'a - 4c - 3b + 4c'  ),
            ('0',                   '0'                 ),
            ('a',                   '-a'                ),
            ('6',                   '-6'                ),
            ('ab + 3cd - 34ef',     '-ab - 3cd + 34ef'  ),
        ]
    
        for info in test_data:
            formula_1 = LinearFormula(info[0])
            formula_2 = LinearFormula(info[1])
            self.assertEqual(-formula_1, formula_2)
        
        test_data = [
            #formula                not equal to -formula
            ('a + 3b - 4c',         'a + 3b - 4c'       ),
            ('a + 3b - 4c + 3a',    '-4a - 3b + 4c'     ),
            ('-a + 4c + 3b - 4c',   'a - 3b'            ),
            ('ab + 3cd - 34ef',     '7g - 3d + 14f'  ),
        ]
    
        for info in test_data:
            formula_1 = LinearFormula(info[0])
            formula_2 = LinearFormula(info[1])
            self.assertNotEqual(-formula_1, formula_2)
    
    #-------------------------------------------------------------------------
    def test_add_sub(self):

        # correct results
        test_data = [
            #formula_1              formula_1 + formula_2
            #           formula_2                   formula_1 - formula 2
            ('a + 3b',  '-4c',      'a + 3b - 4c',  'a + 3b + 4c'   ),
            ('a + b',   'c',        'a + b + c',    'a + b - c'     ),
            ('a + 7b',  '0',        'a + 7b + 0',   'a + 7b + 0'    ),
            ('a + 7b',  '0c',       'a + 7b + 0c',  'a + 7b + 0c'   ),
            ('a',       'b - 4c',   'a + b -4c',    'a - b + 4c'    ),
            ('0',       '3c',       '0 + 3c',       '0 - 3c'        ),
            ('a',       'a',        'a + a',        'a - a'         ),
            ('6',       '3',        '6 + 3',        '6 - 3'         ),
            ('6',       3,          '6 + 3',        '6 - 3'         ),
        ]

        for info in test_data:
            
            formula_2 = LinearFormula(info[1])
            sum = LinearFormula(info[2])
            difference = LinearFormula(info[3])
            
            # +, -
            formula_1 = LinearFormula(info[0])
            # LinearFormula +- LinearFormula
            self.assertEqual(formula_1 + formula_2, sum)
            self.assertEqual(formula_1 - formula_2, difference)
            # LinearFormula +- str (int)
            self.assertEqual(formula_1 + info[1], sum)
            self.assertEqual(formula_1 - info[1], difference)

            # += LinearFormula
            formula_1 = LinearFormula(info[0])
            formula_1 += formula_2
            self.assertEqual(formula_1, sum)

            # -= LinearFormula
            formula_1 = LinearFormula(info[0])
            formula_1 -= formula_2
            self.assertEqual(formula_1, difference)

            # += str (int)
            formula_1 = LinearFormula(info[0])
            formula_1 += info[1]
            self.assertEqual(formula_1, sum)

            # -= str (int)
            formula_1 = LinearFormula(info[0])
            formula_1 -= info[1]
            self.assertEqual(formula_1, difference)

        # wrong results
        test_data = [
            #formula_1              not formula_1 + formula_2
            #           formula_2                   not formula_1 - formula 2
            ('a + 7b',  '0',        'a + 7b',       'a + 7b'    ),
            ('a + 7b',  '0c',       'a + 7b + 0',   'a + 7b + 0'),
            ('a + 7b',  '0c',       'a + 7b',       'a + 7b'    ),
            ('a',       'b - 4c',   'a + b + 4c',   'a - b - 4c'),
            ('0',       '3c',       '3c',           '-3c'       ),
            ('a',       'a',        '2a',           '0a'        ),
            ('a',       'a',        'aa',           '0'         ),
            ('6',       '3',        '9',            '3'         ),
        ]

        for info in test_data:
            
            formula_2 = LinearFormula(info[1])
            sum = LinearFormula(info[2])
            difference = LinearFormula(info[3])
            
            # +, -
            formula_1 = LinearFormula(info[0])
            # LinearFormula +- LinearFormula
            self.assertNotEqual(formula_1 + formula_2, sum)
            self.assertNotEqual(formula_1 - formula_2, difference)
            # LinearFormula +- str
            self.assertNotEqual(formula_1 + info[1], sum)
            self.assertNotEqual(formula_1 - info[1], difference)

            # += LinearFormula
            formula_1 = LinearFormula(info[0])
            formula_1 += formula_2
            self.assertNotEqual(formula_1, sum)

            # -= LinearFormula
            formula_1 = LinearFormula(info[0])
            formula_1 -= formula_2
            self.assertNotEqual(formula_1, difference)

            # += str
            formula_1 = LinearFormula(info[0])
            formula_1 += info[1]
            self.assertNotEqual(formula_1, sum)

            # -= str
            formula_1 = LinearFormula(info[0])
            formula_1 -= info[1]
            self.assertNotEqual(formula_1, difference)
        
        # errors
        test_data = [
            #formula_1  formula_2
            ('a + 7b',  [1, 2]),
            #('a + 7b',  {'c': 3, 'd': 2}),
            ('a + 7b',  (1, 'c')),
        ]

        for info in test_data:            
            # +, -
            formula_1 = LinearFormula(info[0])
            self.assertRaises(TypeError, formula_1.__add__, info[1])
            self.assertRaises(TypeError, formula_1.__sub__, info[1])

            # +=
            formula_1 = LinearFormula(info[0])
            self.assertRaises(TypeError, formula_1.__iadd__, info[1])

            # -=
            formula_1 = LinearFormula(info[0])
            self.assertRaises(TypeError, formula_1.__isub__, info[1])
    
    #-------------------------------------------------------------------------
    def test_mul(self):

        # correct results
        test_data = [
            #formula_1          expected result
            #           multipliter
            ('a + 3b',  2,      '2a + 6b'   ),
            ('a + 3b',  '2',    '2a + 6b'   ),
            ('a + 3b',  1,      'a + 3b'    ),
            ('a + 3b',  0,      '0a + 0b'   ),
            ('a + 3b',  -2,     '-2a - 6b'  ),
            ('a',       3,      '3a'        ),
            ('0',       3,      '0'         ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            expected = LinearFormula(info[2])
            # *
            self.assertEqual(formula * info[1], expected)
            self.assertEqual(info[1] * formula, expected)
            # *=
            formula *= info[1]
            self.assertEqual(formula, expected)
        
        # errors
        test_data = [
            #formula_1                              error
            #           multipliter
            ('a + 3b',  'c + 2d',                   ValueError  ),
            ('a + 3b',  LinearFormula('c + 2d'),    TypeError   ),
            ('a + 3b',  'c',                        ValueError  ),
            ('a + 3b',  '2c',                       ValueError  ),
            ('a + 3b',  LinearFormula('2'),         TypeError   ),
            ('a + 3b',  LinearFormula('2c'),        TypeError   ),
            ('a + 3b',  '-',                        ValueError  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            error = info[2]
            # *
            self.assertRaises(error, formula.__mul__, info[1])
            self.assertRaises(error, formula.__rmul__, info[1])
            # *=
            self.assertRaises(error, formula.__imul__, info[1])
    
    #-------------------------------------------------------------------------
    def test_truediv(self):

        test_data = [
            #formula_1              expected result
            #               divider
            ('4a + 2b',     2,      '2a + b'    ),
            ('4a + 2b',     '2',    '2a + b'    ),
            ('4a + 2b',     1,      '4a + 2b'   ),
            ('6a + 9b',     3,      '2a + 3b'   ),
            ('6a + 9b',     -3,     '-2a - 3b'  ),
            ('0a + 0b',     3,      '0a - 0b'   ),
            ('0',           3,      '0'         ),
            ('6',           3,      '2'         ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            expected = LinearFormula(info[2])
            # /
            self.assertEqual(formula / info[1], expected)
            # /=
            formula /= info[1]
            self.assertEqual(formula, expected)

        # errors
        test_data = [
            #formula_1                              error
            #           multipliter
            ('a + 3b',  'c + 2d',                   ValueError  ),
            ('a + 3b',  LinearFormula('c + 2d'),    TypeError   ),
            ('a + 3b',  'c',                        ValueError  ),
            ('a + 3b',  '2c',                       ValueError  ),
            ('a + 3b',  LinearFormula('2'),         TypeError   ),
            ('a + 3b',  LinearFormula('2c'),        TypeError   ),
            ('a + 3b',  '-',                        ValueError  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            error = info[2]
            # /
            self.assertRaises(error, formula.__truediv__, info[1])
            # /=
            self.assertRaises(error, formula.__itruediv__, info[1])
    
    #-------------------------------------------------------------------------
    def test_floordiv(self):
        
        test_data = [
            #formula_1              expected result
            #               divider
            ('5a + 3b',     2,      '2a + b'    ),
            ('5a + 3b',     '2',    '2a + b'    ),
            ('4a + 2b',     '2',    '2a + b'    ),
            ('4a + 2b',     1,      '4a + 2b'   ),
            ('6a + 9b',     3,      '2a + 3b'   ),
            ('6a + 9b',     2,      '3a + 4b'  ),
            ('0a + 0b',     3,      '0a - 0b'   ),
            ('0',           3,      '0'         ),
            ('7',           3,      '2'         ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            expected = LinearFormula(info[2])
            # //
            self.assertEqual(formula // info[1], expected)
            # //=
            formula //= info[1]
            self.assertEqual(formula, expected)

        # errors
        test_data = [
            #formula_1                              error
            #           multipliter
            ('a + 3b',  'c + 2d',                   ValueError  ),
            ('a + 3b',  LinearFormula('c + 2d'),    TypeError   ),
            ('a + 3b',  'c',                        ValueError  ),
            ('a + 3b',  '2c',                       ValueError  ),
            ('a + 3b',  LinearFormula('2'),         TypeError   ),
            ('a + 3b',  LinearFormula('2c'),        TypeError   ),
            ('a + 3b',  '-',                        ValueError  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            error = info[2]
            # //
            self.assertRaises(error, formula.__truediv__, info[1])
            # //=
            self.assertRaises(error, formula.__itruediv__, info[1])
    
    #-------------------------------------------------------------------------
    def test_mod(self):

        test_data = [
            #initial formula        n       expected result
            ('a + 3b - 4c',         2,      'a + b'         ),
            ('a + 3b - 4c',         '2',    'a + b'         ),
            ('a + 3b - 4c + 3a',    3,      'a + 2c'        ),
            ('a + 7b - 0c - 4d',    3,      'a + b + 2d'    ),
            ('-a + 4c + 3b - 4c',   5,      '4a + 3b'       ),
            ('a',                   4,      'a'             ),
            ('6',                   4,      '2'             ),
            ('ab + 3cd - 34ef',     10,     'ab + 3cd + 6ef'),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            expected = LinearFormula(info[2])
            # %
            self.assertEqual(formula % info[1], expected)
            # %=
            formula %= info[1]
            self.assertEqual(formula, expected)

        # errors
        test_data = [
            #formula_1                              error
            #           multipliter
            ('a + 3b',  'c + 2d',                   ValueError  ),
            ('a + 3b',  LinearFormula('c + 2d'),    TypeError   ),
            ('a + 3b',  'c',                        ValueError  ),
            ('a + 3b',  '2c',                       ValueError  ),
            ('a + 3b',  LinearFormula('2'),         TypeError   ),
            ('a + 3b',  LinearFormula('2c'),        TypeError   ),
            ('a + 3b',  '-',                        ValueError  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            error = info[2]
            # %
            self.assertRaises(error, formula.__truediv__, info[1])
            # %=
            self.assertRaises(error, formula.__itruediv__, info[1])
    
    #-------------------------------------------------------------------------
    def test_getitem(self):

        test_data = [
            #formula                key     expected result
            ('a + 3b - 4c',         2,      (-4, 'c')   ),
            ('a + 3b - 4c',         'c',    -4          ),
            ('a + 3b - 4c + 3a',    'a',    4           ),
            ('a + 7b - 0c - 4d',    'b',    7           ),
            ('-a + 4c + 3b - 4c',   0,      (-1, 'a')   ),
            ('ab + 3cd - 34ef',     2,      (-34, 'ef') ),
            ('ab + 3cd - 34ef',     'ef',   -34         ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            self.assertEqual(formula[info[1]], info[2])
        
        # errors
        test_data = [
            #formula                key     expected error
            ('a + 3b - 4c',         3,      IndexError  ),
            ('a + 3b - 4c',         'd',    KeyError),
            ('a + 3b - 4c + 3a',    '2',    KeyError),
            ('a + 7b',              (1, 2), KeyError),
            ('aa + 7bb - 3cc',      'a',    KeyError),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            error = info[2]
            self.assertRaises(error, formula.__getitem__, info[1])
    
    #-------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()