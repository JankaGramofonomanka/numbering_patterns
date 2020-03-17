import unittest
from numbering_patterns.source.case import Case, MyCase
from numbering_patterns.source.linear_formula import LinearFormula
from numbering_patterns.source.cv_numbering import CentralVertexNumbering


class TestCase(unittest.TestCase):

    def test_init(self):

        test_data = [
            {'n': '2k', 'k': '2t + 1'},
            {'n': 3},
            {'p': 'a + 1', 't': 2},
            {'f': '4t + 1', 't': 67},
        ]

        for kwargs in test_data:
            case = Case(**kwargs)
            self.assertEqual(case.variables.keys(), kwargs.keys())
            for key, value in kwargs.items():
                self.assertEqual(
                    case.variables[key], LinearFormula(kwargs[key]))



class TestMyCase(unittest.TestCase):

    def test_init(self):

        test_data = [
            # n                 up_right        low_right
            #           up_left         low_left        other variables
            ('4k+10',   'k+2',  'k+2',  'k+2',  'k+2',  {}                  ),
            ('4k+10',   'k+3',  'k+1',  'k',    'k+4',  {'k': '2t+1'}       ),
            ('4k+10',   '3t+2', 't+5',  '2t+5', '2t',   {'k': '2t+1'}       ),
            ('4k+10',   'k+1',  '2t+4', 'k+2',  'k+2',  {'k': '2t+1'}       ),
            ('6k+6',    9,      6,      5,      8,      {'k': 't+1', 't': 3}),
            (28,        'k',    'k+5',  'k+3',  'k-2',  {'k': 5}            ),
        ]

        upper_pattern = CentralVertexNumbering(
            '2n', ('i', '2i'), ('i+1', '3i-2', 5))
        lower_pattern = CentralVertexNumbering(
            '2n-3', ('i', '2i', '4i-3'), ('i+1', '3i-2'))
        for info in test_data:

            case = MyCase(
                info[0],
                upper_pattern.set_lengths(info[1], info[2]),
                lower_pattern.set_lengths(info[3], info[4]),
                **info[5]
            )

            self.assertEqual(case.variables['n'], LinearFormula(info[0]))
            for key, value in info[5].items():
                self.assertEqual(
                    case.variables[key], LinearFormula(info[5][key]))

        test_data = [
            # n up_left         low_left        low_left
            #           up_right        low_right       other variables
            ('4k+8',    'k+26', 'k+98', '56',   '23',   {}              ),
            ('4k+8',    'a',    'b',    'c',    'd',    {'k': '2t+1'}   ),
            ('4k+8',    2,      1,      3,      2,      {'k': '2t+1'}   ),
            (23,        2,      1,      3,      2,      {'k': '2t+1'}   ),
            ('6k+4',    9,      6,      5,      3,      {'k': 't+1'}    ),
        ]

        for info in test_data:
            self.assertRaises(
                ValueError, MyCase, info[0],
                upper_pattern.set_lengths(info[1], info[2]),
                lower_pattern.set_lengths(info[3], info[4]),
                **info[5]
            )
