import unittest
from numbering_patterns.source.linear_formula import LinearFormula

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
    def test_equivalent(self):

        test_data = [
            ('a',           'a',            True    ),
            ('2a',          'a+a',          True    ),
            ('a + b',       'b + a',        True    ),
            ('2a + b',      'b + a + a',    True    ),
            ('2a + b',      'a + b + a',    True    ),
            ('2a + b',      '2b + a',       False   ),
            ('a + 3',       'x + 3',        False   ),
            ('a + b',       '2a + 2b',      False   ),
            ('a + b',       'a - b',        False   ),
            ('a + b',       '-a - b',       False   ),
            (2,             '2',            True    ),
            ('a + 3b - 4c', 'x + 3y - 4z',  False   ),
        ]

        for info in test_data:
            formula_1 = LinearFormula(info[0])
            formula_2 = LinearFormula(info[1])

            self.assertEqual(formula_1.equivalent(info[1]), info[2])
            self.assertEqual(formula_1.equivalent(formula_2), info[2])
            self.assertEqual(formula_2.equivalent(info[0]), info[2])
            self.assertEqual(formula_2.equivalent(formula_1), info[2])

    def test_separate(self):

        test_data = [
            ('a+b',         'a',    1,  'b'),
            ('a+b+c',       'a+b',  1,  'c'),
            ('2a+2b',       'a+b',  2,  '0'),
            ('-a-b+c',      'a+b',  -1, 'c'),
            ('a+5',         '5',    1,  'a'),
            ('2a+2b+4c',    'a+2c', 2,  '2b'),
            ('-2a-2b+4c',   'a-2c', -2, '-2b'),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            result = formula.separate(info[1])
            self.assertEqual(result[0], info[2])
            self.assertTrue(LinearFormula(result[1]).equivalent(info[3]))

        test_data = [
            ('2a+3b+c',     'a+b'),
            ('2a+3b+4c',    'a+b+c'),
            ('2a+3b+4c',    'a+c'),
        ]

        for info in test_data:
            formula_1 = LinearFormula(info[0])
            formula_2 = LinearFormula(info[1])
            multiplier, formula_3 = formula_1.separate(formula_2)

            should_be_formula_1 = multiplier*formula_2 + formula_3
            self.assertTrue(formula_1.equivalent(should_be_formula_1))

    def test_get_bounds(self):

        test_data = [
            # formula                       upper bounds         upper bound
            #           lower bounds                    lower bound
            ('a',       {'a': 'b'},         {'a': 'c'}, 'b',     'c'        ),
            ('a+b',     {'a': 'b'},         {'a': 'c'}, '2b',    'c+b'      ),
            ('2a',      {'a': 'b'},         {'a': 'c'}, '2b',    '2c'       ),
            ('-a',      {'a': 'b'},         {'a': 'c'}, '-c',    '-b'       ),
            ('a+3b-4c', {'a': 'b', 'c': 2}, {'b': 'c'}, '4b-4c', 'a+3c-8'   ),
            ('a',       {'a': 1},           {'a': 2},   1,       2          ),
            ('a+b',     {'a': 1},           {'b': 2},   '1+b',   'a+2'      ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            lower_bounds = info[1]
            upper_bounds = info[2]
            expected_lower_bound = LinearFormula(info[3])
            expected_upper_bound = LinearFormula(info[4])

            result = formula.get_bounds(
                lower_bounds=lower_bounds,
                upper_bounds=upper_bounds,
            )

            actual_lower_bound = result[0]
            actual_upper_bound = result[1]

            self.assertEqual(
                actual_lower_bound.zip(), expected_lower_bound.zip())
            self.assertEqual(
                actual_upper_bound.zip(), expected_upper_bound.zip())

    def test_get_bounds_recursive(self):

        test_data = [
            ('a',                       # formula
             {'a': 'b', 'b': 'c'},      # lower bounds
             {'a': 'd', 'd': 'e'},      # upper bounds
             # lower bound      upper bound
             'c',               'e'),

            ('a+b',
             {'a': 'b', 'b': 'c'},
             {'a': 'd', 'd': 'e'},
             '2c', 'e+b'),

            ('a+b',
             {'a': 'd', 'd': 'e'},
             {'a': 'b', 'b': 'c'},
             'e+b', '2c'),

            ('a+b+c+d',
             {'a': 'b', 'b': 'c', 'c': 'd', 'd': 'e'},
             {'a': 'f', 'f': 'g', 'b': 'f', 'c': 'g'},
             '4e', '3g+d'),

            ('a+b+c+d',
             {'a': 'f', 'f': 'g', 'b': 'f', 'c': 'g'},
             {'a': 'b', 'b': 'c', 'c': 'd', 'd': 'e'},
             '3g+d', '4e'),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            lower_bounds = info[1]
            upper_bounds = info[2]
            expected_lower_bound = LinearFormula(info[3])
            expected_upper_bound = LinearFormula(info[4])

            result = formula.get_bounds(
                lower_bounds=lower_bounds,
                upper_bounds=upper_bounds,
                recursive=True
            )

            actual_lower_bound = result[0]
            actual_upper_bound = result[1]

            self.assertEqual(
                actual_lower_bound.zip(), expected_lower_bound.zip())
            self.assertEqual(
                actual_upper_bound.zip(), expected_upper_bound.zip())


if __name__ == '__main__':
    unittest.main()