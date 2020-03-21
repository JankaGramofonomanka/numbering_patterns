import unittest
from numbering_patterns.source.linear_formula import LinearFormula

class TestModifiers(unittest.TestCase):

    #-TEST-MODIFIERS----------------------------------------------------------
    
    #-------------------------------------------------------------------------
    def test_inplace(self):

        test_data = [
            (LinearFormula.add_segment,     [3, 'f']                        ),
            (LinearFormula.insert_segment,  [3, 'f', 2]                     ),
            (LinearFormula.remove_segment,  [3]                             ),
            (LinearFormula.substitute,      {'b': LinearFormula('x + 3')}   ),
            (LinearFormula.zip,             []                              ),
            (LinearFormula.modulo,          [2]                             ),
        ]

        for function, args in test_data:
            formula = LinearFormula('a + 3b - 4c + 3a')
            control_formula = LinearFormula('a + 3b - 4c + 3a')
            self.assertEqual(formula, control_formula)

            if type(args) == dict:
                function(formula, **args)
            else:
                function(formula, *args)
            self.assertEqual(formula, control_formula)

            if type(args) == dict:
                function(formula, **args, inplace=True)
            else:
                function(formula, *args, inplace=True)
            self.assertNotEqual(formula, control_formula)

    #-------------------------------------------------------------------------
    def test_add_segment(self):

        test_data = [
            #initial         multiplier  expected result
            #formula             variable
            ('a + 3b - 4c', (3,  'g'),   'a + 3b - 4c + 3g'  ),
            ('a + 3b - 4c', (-3, 'g'),   'a + 3b - 4c - 3g'  ),
            ('0',           (3,  'g'),   '0 + 3g'            ),
            ('0',           (-3, 'g'),   '0 - 3g'            ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.add_segment(*info[1], inplace=True)
            self.assertEqual(str(formula), info[2])

    #-------------------------------------------------------------------------
    def test_insert_segment(self):

        test_data = [
            #initial             multiplier      expected result
            #formula                 variable
            #                             index
            ('a + 3b - 4c',     (5,  'g', 1),   'a + 5g + 3b - 4c'  ),
            ('a + 3b - 4c',     (-5, 'g', 1),   'a - 5g + 3b - 4c'  ),
            ('a + 3b - 4c',     (5,  'g', 0),   '5g + a + 3b - 4c'  ),
            ('a + 3b - 4c',     (-5, 'g', 0),   '-5g + a + 3b - 4c' ),
            ('-a + 3b - 4c',    (5,  'g', 0),   '5g - a + 3b - 4c'  ),
            ('a + 3b - 4c',     (-5, 'g', 3),   'a + 3b - 4c - 5g'  ),
            ('0',               (3,  'g', 0),   '3g + 0'            ),
            #('',                (3,  'g', 1),   'err'               ),
        ]   

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.insert_segment(*info[1], inplace=True)
            self.assertEqual(str(formula), info[2])

    #-------------------------------------------------------------------------
    def test_remove_segment(self):

        test_data = [
            #initial formula            formula after removal
            #                   index
            ('a + 3b - 4c',     1,      'a - 4c'),
            ('a + 3b - 4c',     2,      'a + 3b'),
            ('a',               0,      '0'     ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.remove_segment(info[1], inplace=True)
            self.assertEqual(str(formula), info[2])

    #-------------------------------------------------------------------------
    def test_substitute(self):

        test_data = [
            #initial formula            substitute formula
            #                   variable to         expected result
            #                   substitute
            ('a + 3b - 4c',     {'a':   'x + 2'},   'x + 2 + 3b - 4c'       ),
            ('a + b - c',       {'a':   '2'},       '2 + b - c'             ),
            ('1 + 2 - 3',       {'a':   'x + 2'},   '1 + 2 - 3'             ),
            ('a + 3b + 3a',     {'a':   'x + 2'},   'x + 2 + 3b + 3x + 6'   ),
            ('a + 7b - 4d',     {'b':   'x + 2'},   'a + 7x + 14 - 4d'      ),
            ('-a + 4c',         {'c':   'x + 2'},   '-a + 4x + 8'           ),
            ('',                {'a':   'x + 2'},   '0'                     ),
            ('a',               {'a':   'x + 2'},   'x + 2'                 ),
            ('6a + 3b',         {'c':   'x + 2'},   '6a + 3b'               ),
            ('a + 3b - 4c',     {'a':   'aaa'},     'aaa + 3b - 4c'         ),
            ('a + 3b - 4c',     {'a':   'a + 2'},   'a + 2 + 3b - 4c'       ),
            ('a + 3b - 4c',     {'a':   'a'},       'a + 3b - 4c'           ),

            #substitute multiple variables at once
            #initial formula                                result
            #               {variable: substitute}
            ('a + 3b - 4c', {'a': 'x', 'b': 'y', 'c': 'z'}, 'x + 3y - 4z'   ),
            ('a + 3b',      {'a': 'x + 2', 'b': 'y - 1'},   'x + 2 + 3y - 3'),
            ('a',           {'a': 'x + 2', 'b': 'y - 1'},   'x + 2'         ),
            ('a + 2b',      {'a': 'b', 'b': 'a'},           'b + 2a'        ),
            ('a + 2b',      {'a': 'b + y', 'b': 'a'},       'b + y + 2a'    ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])

            init_data = info[1]
            formula_2 = formula.substitute(**init_data)
            self.assertEqual(str(formula_2), info[2])

            for key in init_data.keys():
                init_data[key] = LinearFormula(init_data[key])
            formula_2 = formula.substitute(**init_data)
            self.assertEqual(str(formula_2), info[2])

    #-------------------------------------------------------------------------
    def test_substitute_recursive(self):

        test_data = [
            # init formula                                  result
            #       {variable: substitute}
            ('a',   {'a': 'b', 'b': 'c'},                   'c'     ),
            ('a+b', {'a': 'b', 'b': 'c'},                   '2c'    ),
            ('a+b', {'a': 'c', 'b': 'c', 'c': 'd'},         '2d'    ),
            ('a+b', {'a': 'k+1', 'b': 'k-2'},               '2k-1'  ),
            ('a+b', {'a': 'k+1', 'b': 'k-2', 'k': '3t+1'},  '6t+1'  ),
            ('a+b', {'k': 'a', 't': 'b'},                   'a+b'   ),
            ('a',   {'c': 'd', 'b': 'c', 'a': 'b'},         'd'     ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.substitute(**info[1], recursive=True, inplace=True)

            self.assertEqual(formula.zip(), LinearFormula(info[2]).zip())

        # errors, (to do)
        test_data = [
            # ('a+b', {'a': 'c', 'b': 'c', 'c': 'a'}),
            # ('a+b', {'a': 'b', 'b': 'a'}          ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            self.assertRaises(ValueError, formula.substitute, **info[2])


    #-------------------------------------------------------------------------
    def test_zip(self):

        test_data = [
            #initial formula        zipped formula
            ('a + 3b - 4c',         'a + 3b - 4c'       ),
            ('a + 3b - 4c + 3a',    '4a + 3b - 4c'      ),
            ('a + 7b - 0c - 4d',    'a + 7b - 4d'       ),
            ('-a + 4c + 3b - 4c',   '-a + 3b'           ),
            ('',                    '0'                 ),
            ('a',                   'a'                 ),
            ('6',                   '6'                 ),
            ('ab + 3cd - 34ef',     'ab + 3cd - 34ef'   ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.zip(inplace=True)
            self.assertEqual(str(formula), info[1])
    
    #-------------------------------------------------------------------------
    def test_modulo(self):

        test_data = [
            #initial formula        n   expected result
            ('a + 3b - 4c',         2,  'a + b'         ),
            ('a + 3b - 4c + 3a',    3,  'a + 2c'        ),
            ('a + 7b - 0c - 4d',    3,  'a + b + 2d'    ),
            ('-a + 4c + 3b - 4c',   5,  '4a + 3b'       ),
            ('a',                   4,  'a'             ),
            ('6',                   4,  '2'             ),
            ('ab + 3cd - 34ef',     10, 'ab + 3cd + 6ef'),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.modulo(info[1], inplace=True)
            self.assertEqual(str(formula), info[2])

    #-------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()