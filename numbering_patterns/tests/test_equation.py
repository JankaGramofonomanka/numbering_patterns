import unittest
from numbering_patterns.source.linear_formula import LinearFormula
from numbering_patterns.source.equation import LinearEquation


class TestLinearEquation(unittest.TestCase):


    #-INIT--------------------------------------------------------------------

    def test_init_with_formulas(self):

        # init with formulas
        test_data = [
            # left          right
            ('a + b - 3c',  '-b + a + c - 4c + 2b'  ),
            ('a',           'b'             ),
        ]

        for info in test_data:
            if len(info) == 2:
                relation = '=='
                kwargs = {}
            else:
                relation = info[2]
                kwargs = {'relation': info[2]}

            args = (info[0], info[1])

            rel = LinearEquation(*args, **kwargs)
            left = LinearFormula(info[0])
            right = LinearFormula(info[1])

            self.assertEqual(rel.left, left)
            self.assertEqual(rel.right, right)
            self.assertEqual(rel.relation, relation)

            rel = LinearEquation(left, right)
            self.assertEqual(rel.left, left)
            self.assertEqual(rel.right, right)
            self.assertEqual(rel.relation, relation)

    def test_init_with_string(self):

        # init with string
        test_data = [
            # init string               left        right           relation
            ('a+b-3c = -b+a+c-4c+2b',   'a+b-3c',   '-b+a+c-4c+2b', '=='),
            ('a = b',                   'a',        'b',            '=='),
            ('a == b',                  'a',        'b',            '=='),
            ('a + b - 3c == 2c',        'a+b-3c',   '2c',           '=='),
            ('a + b - 3c <= 2c',        'a+b-3c',   '2c',           '<='),
            ('a + b - 3c >= 2c',        'a+b-3c',   '2c',           '>='),
            ('a + b - 3c < 2c',         'a+b-3c',   '2c',           '<' ),
            ('a + b - 3c > 2c',         'a+b-3c',   '2c',           '>' ),
        ]

        for info in test_data:
            rel = LinearEquation(info[0])
            left = LinearFormula(info[1])
            right = LinearFormula(info[2])
            relation = info[3]

            self.assertEqual(rel.left, left)
            self.assertEqual(rel.right, right)
            self.assertEqual(rel.relation, relation)

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def test_str(self):

        test_data = [
            # left      right       relation    string
            ('a+b-3c',  '-b+a+c',   '==',       'a + b - 3c == -b + a + c'),
            ('a',       'b',        '==',       'a == b'),
            ('a',       'b',        '<=',       'a <= b'),
            ('a',       'b',        '>=',       'a >= b'),
            ('a',       'b',        '<',        'a < b'),
            ('a',       'b',        '>',        'a > b'),
        ]

        for info in test_data:
            rel = LinearEquation(info[0], info[1], relation=info[2])
            self.assertEqual(str(rel), info[3])

    def test_eq(self):

        test_data = [
            'a + b == a + b',
            'c + d == 2c',
            'c + d <= 2c',
            'c + d >= 2c',
            'c + d < 2c',
            'c + d > 2c',
        ]

        for args in test_data:
            rel_1 = LinearEquation(args)
            rel_2 = LinearEquation(args)
            self.assertEqual(rel_1, rel_2)

        # not equal
        test_data = [
            # equation 1        equation 2
            ('a + b == c + d',  'a + b - c == d'),
            ('a + b == a + b',  'a + b - a - b == 0'),
            ('a + b == a + b',  'b - b == 0'),
            ('a + b == 2a',     'b - a == 0'),
            ('a + b == 2a',     'a + b <= 2a'),
            ('a + b <= 2a',     'a + b == 2a'),
            ('a + b >= 2a',     'a + b == 2a'),
            ('a + b == 2a',     'a + b < 2a'),
            ('a + b == 2a',     'a + b > 2a'),
            ('a + b > 2a',      'a + b == 2a'),
            ('a + b <= 2a',     'a + b >= 2a'),
            ('a + b >= 2a',     'a + b <= 2a'),
            ('a + b <= 2a',     'a + b < 2a'),
            ('a + b > 2a',      'a + b >= 2a'),

        ]

        for info in test_data:
            rel_1 = LinearEquation(info[0])
            rel_2 = LinearEquation(info[1])
            self.assertNotEqual(rel_1, rel_2)

    def test_neg(self):

        test_data = [
            # equation          -equation
            ('a + b == a + b',  '-a - b == -a + -b'),
            ('c + d == 2c',     '-c - d == -2c'),
            ('a + b == a - b',  '-a - b == -a + b'),
            ('a + b <= a - b',  '-a - b >= -a + b'),
            ('a + b >= a - b',  '-a - b <= -a + b'),
            ('a + b < a - b',   '-a - b > -a + b'),
            ('a + b > a - b',   '-a - b < -a + b'),
        ]

        for info in test_data:
            rel = LinearEquation(info[0])
            minus_rel = LinearEquation(info[1])
            self.assertEqual(-rel, minus_rel)

    def test_add_sub_number(self):

        test_data = [
            # equation/                 number
            # /equation + number/
            # /equation - number
            ('a + b == c + d',          '2c',
             'a + b + 2c == c + d + 2c',
             'a + b - 2c == c + d - 2c'),

            ('a + b == a + b',          'e',
             'a + b + e == a + b + e',
             'a + b - e == a + b - e'),

            ('a + b > a + b',          1,
             'a + b + 1 > a + b + 1',
             'a + b - 1 > a + b - 1'),

            ('a + b == a + b',          LinearFormula('a + 3b'),
             'a + b + a + 3b == a + b + a + 3b',
             'a + b - a - 3b == a + b - a - 3b'),

            ('a + b <= a + b',           'a + 3b',
             'a + b + a + 3b <= a + b + a + 3b',
             'a + b - a - 3b <= a + b - a - 3b'),

            ('a + b <= c + d',          '2c',
             'a + b + 2c <= c + d + 2c',
             'a + b - 2c <= c + d - 2c'),

            ('a + b >= c + d',          '2c',
             'a + b + 2c >= c + d + 2c',
             'a + b - 2c >= c + d - 2c'),

            ('a + b < c + d',           '2c',
             'a + b + 2c < c + d + 2c',
             'a + b - 2c < c + d - 2c'),

            ('a + b > c + d',           '2c',
             'a + b + 2c > c + d + 2c',
             'a + b - 2c > c + d - 2c'),
        ]

        for info in test_data:
            rel = LinearEquation(info[0])
            rel_plus = LinearEquation(info[2])
            rel_minus = LinearEquation(info[3])

            self.assertEqual(rel + info[1], rel_plus)
            self.assertEqual(rel - info[1], rel_minus)

            rel += info[1]
            self.assertEqual(rel, rel_plus)

            rel = LinearEquation(info[0])
            rel -= info[1]
            self.assertEqual(rel, rel_minus)

    def test_add_sub_equation(self):

        # TODO: add different relations
        test_data = [
            # equation 1        equation 2
            ('a == c',          'b == d',
             'a + b == c + d',            # sum
             'a - b == c - d'),           # difference

            ('a == b',          'a == b',
             'a + a == b + b',
             'a - a == b - b'),

            ('a <= b',          'a <= b',
             'a + a <= b + b',
             'a - a <= b - b'),

            ('a >= b',          'a >= b',
             'a + a >= b + b',
             'a - a >= b - b'),

            ('a < b',           'a < b',
             'a + a < b + b',
             'a - a < b - b'),

            ('a > b',           'a > b',
             'a + a > b + b',
             'a - a > b - b'),
        ]

        for info in test_data:
            rel_1 = LinearEquation(info[0])
            rel_2 = LinearEquation(info[1])
            rel_sum = LinearEquation(info[2])
            rel_diff = LinearEquation(info[3])

            self.assertEqual(rel_1 + rel_2, rel_sum)
            self.assertEqual(rel_1 - rel_2, rel_diff)

            rel_1 += rel_2
            self.assertEqual(rel_1, rel_sum)

            rel_1 = LinearEquation(info[0])
            rel_1 -= rel_2
            self.assertEqual(rel_1, rel_diff)

    def test_mul(self):

        test_data = [
            # equation          num     equation * num
            ('a + b == c + d',  '2',    '2a + 2b == 2c + 2d'    ),
            ('a + b == a + b',  2,      '2a + 2b == 2a + 2b'    ),
            ('a + b == a + b',  5,      '5a + 5b == 5a + 5b'    ),
            ('a + b <= c + d',  2,      '2a + 2b <= 2c + 2d'    ),
            ('a + b >= c + d',  2,      '2a + 2b >= 2c + 2d'    ),
            ('a + b < c + d',   2,      '2a + 2b < 2c + 2d'     ),
            ('a + b > c + d',   2,      '2a + 2b > 2c + 2d'     ),
            ('a + b <= c + d',  -2,     '-2a - 2b >= -2c - 2d'  ),
            ('a + b >= c + d',  -2,     '-2a - 2b <= -2c - 2d'  ),
            ('a + b < c + d',   -2,     '-2a - 2b > -2c - 2d'   ),
            ('a + b > c + d',   -2,     '-2a - 2b < -2c - 2d'   ),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            eq_mul = LinearEquation(info[2])
            self.assertEqual(eq * info[1], eq_mul)

            eq *= info[1]
            self.assertEqual(eq, eq_mul)

    def test_truediv(self):
        test_data = [
            # equation                  num     equation / num
            ('2a + 2b == 2c + 2d',      '2',    'a + b == c + d'        ),
            ('2a + 4b == 6a + 8b',      2,      'a + 2b == 3a + 4b'     ),
            ('3a + 6b == 9a + 12b',     3,      'a + 2b == 3a + 4b'     ),
            ('3a + 6b <= 9a + 12b',     3,      'a + 2b <= 3a + 4b'     ),
            ('3a + 6b >= 9a + 12b',     3,      'a + 2b >= 3a + 4b'     ),
            ('3a + 6b < 9a + 12b',      3,      'a + 2b < 3a + 4b'      ),
            ('3a + 6b > 9a + 12b',      3,      'a + 2b > 3a + 4b'      ),
            ('3a + 6b <= 9a + 12b',     -3,     '-a - 2b >= -3a - 4b'   ),
            ('3a + 6b >= 9a + 12b',     -3,     '-a - 2b <= -3a - 4b'   ),
            ('3a + 6b < 9a + 12b',      -3,     '-a - 2b > -3a - 4b'    ),
            ('3a + 6b > 9a + 12b',      -3,     '-a - 2b < -3a - 4b'    ),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            eq_div = LinearEquation(info[2])
            self.assertEqual(eq / info[1], eq_div)

            eq /= info[1]
            self.assertEqual(eq, eq_div)

    def test_mod(self):

        test_data = [
            ('2a+3b == 4c-2d', 2, 'b == 0'),
            ('2a+3b == 4c-2d', 3, '2a == c+d'),
            ('2a+3b == 4c-2d', 1, '0 == 0'),
            ('2a+3b == 4c-2d', 4, '2a+3b == 2d'),
            ('2a+3b-4c+2d == 0', 3, '2a+2c+2d == 0'),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            eq_mod = LinearEquation(info[2])
            self.assertEqual(eq % info[1], eq_mod.zip())

            eq %= info[1]
            self.assertEqual(eq, eq_mod.zip())

    #-------------------------------------------------------------------------


    #-MODIFIERS---------------------------------------------------------------

    def test_substitute(self):

        test_data = [
            # equation/                 {variable: substitute}
            # /result
            ('a + b == c + d',          {'a': 2, 'c': 3},
             '2 + b == 3 + d'),

            ('a + b == b + a',          {'a': 'b', 'b': 'a'},
             'b + a == a + b'),

            ('a + b == b + 1',          {'a': 'b', 'b': 'c'},
             'b + c == c + 1'),

            ('a + b == c + b',          {'a': '2a', 'b': 'd + 2'},
             '2a + d + 2 == c + d + 2'),

            ('a + b <= b + 1',          {'a': 'b', 'b': 'c'},
             'b + c <= c + 1'),

            ('a + b >= b + 1',          {'a': 'b', 'b': 'c'},
             'b + c >= c + 1'),

            ('a + b < b + 1',           {'a': 'b', 'b': 'c'},
             'b + c < c + 1'),

            ('a + b > b + 1',           {'a': 'b', 'b': 'c'},
             'b + c > c + 1'),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            expected_result = LinearEquation(info[2])
            eq.substitute(**info[1], inplace=True)
            self.assertEqual(eq, expected_result)

    def test_substitute_recursive(self):

        test_data = [
            # equation/                 {variable: substitute}
            # /result
            ('a + b == c + d',          {'a': 2, 'c': 3},
             '2 + b == 3 + d'),

            ('a + b == b + a',          {'a': 'b', 'b': 'c'},
             '2c == 2c'),

            ('a + b == b + 1',          {'a': 'b', 'b': 'c'},
             '2c == c + 1'),

            ('a + b == c + b',          {'c': 'd', 'b': 'c', 'a': 'b'},
             '2d == 2d'),

            ('a + b <= b + a',          {'a': 'b', 'b': 'c'},
             '2c <= 2c'),

            ('a + b >= b + a',          {'a': 'b', 'b': 'c'},
             '2c >= 2c'),

            ('a + b < b + a',           {'a': 'b', 'b': 'c'},
             '2c < 2c'),

            ('a + b > b + a',           {'a': 'b', 'b': 'c'},
             '2c > 2c'),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            expected_result = LinearEquation(info[2])
            eq.substitute(**info[1], recursive=True, inplace=True)
            self.assertEqual(eq.zip(), expected_result.zip())

    def test_zip(self):

        test_data = [
            # equation          zipped equation
            ('a+a == a',        '2a == a'       ),
            ('a == a',          'a == a'        ),
            #('a-a == b+b',      '0 == 2b'       ),
            ('a-a+1 == b+b',    '1 == 2b'       ),
            ('a+b+a == b-a+b',  '2a+b == 2b-a'  ),
            ('a+b+a <= b-a+b',  '2a+b <= 2b-a'  ),
            ('a+b+a >= b-a+b',  '2a+b >= 2b-a'  ),
            ('a+b+a < b-a+b',   '2a+b < 2b-a'   ),
            ('a+b+a > b-a+b',   '2a+b > 2b-a'   ),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            zipped = LinearEquation(info[1])
            self.assertEqual(eq.zip(), zipped)

    def test_modulo(self):

        test_data = [
            ('2a+3b == 4c-2d', 2, 'b == 0'),
            ('2a+3b == 4c-2d', 3, '2a == c+d'),
            ('2a+3b == 4c-2d', 1, '0 == 0'),
            ('2a+3b == 4c-2d', 4, '2a+3b == 2d'),
            ('2a+3b-4c+2d == 0', 3, '2a+2c+2d == 0'),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            eq_mod = LinearEquation(info[2])
            eq.modulo(info[1], inplace=True)
            self.assertEqual(eq, eq_mod.zip())

    def test_reverse(self):

        test_data = [
            # equation      reversed equation
            ('a == b',      'b == a'),
            ('a+b == b-d',  'b-d == a+b'),
            ('a+b+c == b',  'b == a+b+c'),
            ('a+b+c <= b',  'b >= a+b+c'),
            ('a+b+c >= b',  'b <= a+b+c'),
            ('a+b+c < b',   'b > a+b+c'),
            ('a+b+c > b',   'b < a+b+c'),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            eq_rev = LinearEquation(info[1])
            self.assertEqual(eq.reverse(), eq_rev)

    def test_solve(self):

        test_data = [
            ('a+b == 2b-c', 'a-b+c == 0'),
            ('a == b',      'a-b == 0'  ),
            ('a-a==b',      '-b == 0'   ),
            ('a+b <= 2b-c', 'a-b+c <= 0'),
            ('a+b >= 2b-c', 'a-b+c >= 0'),
            ('a+b < 2b-c',  'a-b+c < 0' ),
            ('a+b > 2b-c',  'a-b+c > 0' ),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            solved = LinearEquation(info[1])
            eq.solve(inplace=True)
            self.assertEqual(eq, solved)

    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    # TODO: adjust to other relations
    def test_copy(self):

        eq = LinearEquation('a == b')
        copy_of_eq = eq.copy()
        self.assertEqual(eq, copy_of_eq)

        copy_of_eq.left += 15
        self.assertNotEqual(eq, copy_of_eq)

    # TODO: adjust to other relations
    def test_evaluate(self):

        test_data = [
            ('a+b == c-d', {'a': 1, 'b': 1, 'c': 1, 'd': 1},
             '2 == 0'),
            ('a+b == c-d', {'a': 1, 'b': 3, 'c': 2, 'd': -2},
             '4 == 4'),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            evaluation = LinearEquation(info[2])
            self.assertEqual(eq.evaluate(**info[1]), evaluation)

    # TODO: adjust to other relations
    def test_get_variables(self):

        test_data = [
            ('a == b',          {'a', 'b'}, {'a', 'b'}  ),
            ('a == b - 0b',     {'a', 'b'}, {'a', 'b'}  ),
            ('a == a - 0b',     {'a', 'b'}, {'a'}       ),
            ('a+b == b',        {'a', 'b'}, {'a', 'b'}  ),
            ('a+b == 0b-a',     {'a', 'b'}, {'a', 'b'}  ),
            ('0a+b == b+0a',    {'a', 'b'}, {'b'}       ),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            self.assertEqual(eq.get_variables(), info[1])
            self.assertEqual(eq.get_variables(omit_zeros=True), info[2])

    # TODO: adjust to other relations
    def test_status(self):

        test_data = [
            # equation      status
            ('a == b',      'unknown'),
            ('a == a',      'true'),
            ('0 == 1',      'false'),
            ('a == a+1',    'false'),
            ('2a == a+a',   'true'),
            ('a-b == a-b',  'true'),
            ('a+b == a+2b', 'unknown'),
        ]

        for info in test_data:
            eq = LinearEquation(info[0])
            self.assertEqual(eq.status(), info[1])








