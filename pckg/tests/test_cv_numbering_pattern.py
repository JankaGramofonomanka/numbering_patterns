import unittest
from pckg.source.cv_numbering_pattern import CentralVertexNumberingPattern
from pckg.source.ntr_sequence import NTermRecursionSequence
from pckg.source.linear_formula import LinearFormula

class TestCVNP(unittest.TestCase):

    def test_init(self):

        test_data = [
            # init args
            (4,     ('i', '2i'),    ('2i', 'i'),    3,      3       ),
            ('2n',  ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1'),
            (4,     ('i', '2i'),    ('2i', 'i') ),
        ]

        for info in test_data:
            pattern_1 = CentralVertexNumberingPattern(*info)
            args = list(info)
            args[1] = NTermRecursionSequence(*args[1])
            args[2] = NTermRecursionSequence(*args[2])
            pattern_2 = CentralVertexNumberingPattern(*args)

            self.assertEqual(pattern_1.center, LinearFormula(info[0]))
            self.assertEqual(pattern_2.center, LinearFormula(info[0]))
            left_seq = NTermRecursionSequence(*info[1])
            right_seq = NTermRecursionSequence(*info[2])
            self.assertEqual(pattern_1.left_seq, left_seq)
            self.assertEqual(pattern_2.left_seq, left_seq)
            self.assertEqual(pattern_1.right_seq, right_seq)
            self.assertEqual(pattern_2.right_seq, right_seq)

            if len(info) == 3:
                args.append('inf')
                args.append('inf')

            self.assertEqual(pattern_1.left_len, LinearFormula(args[3]))
            self.assertEqual(pattern_2.left_len, LinearFormula(args[3]))
            self.assertEqual(pattern_1.right_len, LinearFormula(args[4]))
            self.assertEqual(pattern_2.right_len, LinearFormula(args[4]))

    def test_eq(self):

        test_data = [
            # init args
            (4,     ('i', '2i'),    ('2i', 'i'),    3,      3       ),
            ('2n',  ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1'),
            (4,     ('i', '2i'),    ('2i', 'i') ),
        ]

        for args in test_data:
            pattern_1 = CentralVertexNumberingPattern(*args)
            pattern_2 = CentralVertexNumberingPattern(*args)

            self.assertEqual(pattern_1, pattern_2)

        test_data = [
            # init args
            ((4,    ('i', '2i'),    ('2i', 'i'), 3, 3),
             (4,    ('i', '2i'),    ('2i', 'i') )                       ),

            (('2',  ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1'),
             ('2n', ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1')   ),

            (('2',  ('i', '2i'),    ('2i', 'i') ),
             ('2n', ('i', '2i'),    ('2i', 'i') )                       ),

            ((4,    ('2i', 'i'),    ('i', '2i'), 3, 3),
             (4,    ('i', '2i'),    ('2i', 'i'), 3, 3)                  ),
        ]

        for info in test_data:
            pattern_1 = CentralVertexNumberingPattern(*info[0])
            pattern_2 = CentralVertexNumberingPattern(*info[1])
            self.assertNotEqual(pattern_1, pattern_2)

    def test_evaluate(self):

        test_data = [
            # init args/
            # /(index, value)
            ((4,    ('i', '2i'),    ('2i', 'i'), 3, 3),
             (0, 4),    (-1, 0),    (-2, 0),    (-3, 1),    (-4, 2),
             (1, 0),    (2, 0),     (3, 2),     (4, 1),     (5, 4)          ),

            (('2',  ('a + i', '2i', '6i'),      ('2i', 'i') ),
             (0, 2),    (1, 0),     (2, 0),     (3, 2),         (4, 1),
             (-1, 'a'), (-2, 0),    (-3, 0),    (-4, 'a + 1'),  (-5, 2)     ),

            ((4,    ('i',),         ('2i',), 3, 3),
             (0, 4),    (1, 0),     (2, 2),     (3, 4),     (4, 6),
             (-1, 0),   (-2, 1),    (-3, 2),    (-4, 3),    (-5, 4)         ),

            ((4,    ('i', 'i'),     ('2i', '2i'), 3, 3),
             (0, 4),    (1, 0),     (2, 0),     (3, 2),     (4, 2),
             (-1, 0),   (-2, 0),    (-3, 1),    (-4, 1),    (-5, 2)         ),

            (('2n', ('3', '2'),     ('a', 'i'), 3, 3),
             (0, '2n'), (1, 'a'),   (2, 0),     (3, 'a'),   (4, 1),
             (-1, 3),   (-2, 2),    (-3, 3),    (-4, 2),    (-5, 3)         ),
        ]

        for info in test_data:
            pattern = CentralVertexNumberingPattern(*info[0])
            for index, value in info[1:]:
                result = pattern.evaluate(index)
                expected_result = LinearFormula(value).zip()
                self.assertEqual(result, expected_result)

    def test_get_variables(self):

        # don't omit zeros
        test_data = [
            # init args                             variables in use
            ((4, ('i', '2i'), ('2i', 'i'), 3, 3),   {'i'}           ),
            (('2', ('a + i', '6i'), ('2i', 'i')),   {'a', 'i'}      ),
            ((4, ('i',), ('2b',), 3, 3),            {'i', 'b'}      ),
            (('a', ('b',), ('c',), 'd', 'e'),      {'a', 'b', 'c', 'd', 'e'}),
            (('a', ('a',), ('a',), 'a', 'a'),       {'a'}           ),
            (('2n', ('3', '2'), ('a', 'i'), 3, 3),  {'n', 'a', 'i'} ),
            (('0a', ('0b',), ('0c',), '0d', '0e'), {'a', 'b', 'c', 'd', 'e'}),
        ]

        for info in test_data:
            pattern = CentralVertexNumberingPattern(*info[0])
            self.assertEqual(pattern.get_variables(), info[1])

        # omit zeros
        test_data = [
            # init args                             variables in use
            (('0a', ('b',), ('c',), 'd', 'e'),      {'b', 'c', 'd', 'e'}),
            (('a', ('0b',), ('c',), 'd', 'e'),      {'a', 'c', 'd', 'e'}),
            (('a', ('b',), ('0c',), 'd', 'e'),      {'a', 'b', 'd', 'e'}),
            (('a', ('b',), ('c',), '0d', 'e'),      {'a', 'b', 'c', 'e'}),
            (('a', ('b',), ('c',), 'd', '0e'),      {'a', 'b', 'c', 'd'}),

            (('0a', ('a',), (1,), 1, 1),            {'a'}               ),
            ((1, ('0a',), ('a',), 1, 1),            {'a'}               ),
            ((1, (1,), ('0a',), 'a', 1),            {'a'}               ),
            ((1, (1,), (1,), '0a', 'a'),            {'a'}               ),

            (('a', ('0a',), (1,), 1, 1),            {'a'}               ),
            ((1, ('a',), ('0a',), 1, 1),            {'a'}               ),
            ((1, (1,), ('a',), '0a', 1),            {'a'}               ),
            ((1, (1,), (1,), 'a', '0a'),            {'a'}               ),

            (('0a', ('0b',), ('0c',), '0d', '0e'),  set({})             ),
        ]

        for info in test_data:
            pattern = CentralVertexNumberingPattern(*info[0])
            self.assertEqual(pattern.get_variables(omit_zeros=True), info[1])

    def test_copy(self):
        pattern = CentralVertexNumberingPattern(4, ('i', '2i'), ('2i', 'i'))
        copy_of_pattern = pattern.copy()
        self.assertEqual(pattern, copy_of_pattern)

        copy_of_pattern.center = LinearFormula(5)
        self.assertNotEqual(pattern, copy_of_pattern)

    def test_zip(self):

        test_data = [
            # init formulas/
            # /zipped formulas
            (('i+i',    ('i+i', 'i+i'), ('i+i', 'i+i'), 'i+i',  'i+i'   ),
             ('2i',     ('2i', '2i'),   ('2i', '2i'),   '2i',   '2i'    )),

            (('i-i',    ('a-2a',),      ('i', 'i'),     'i+2i', '2c-c+i'),
             ('',       ('-a',),        ('i', 'i'),     '3i',   'c+i'   )),
        ]

        for info in test_data:
            pattern = CentralVertexNumberingPattern(*info[0])
            pattern.zip(inplace=True)

            expected = CentralVertexNumberingPattern(*info[1])
            self.assertEqual(pattern, expected)

    def test_substitute(self):

        test_data = [
            # {variable: substitute}/
            # /init formulas/
            # /formulas after substitution
            ({'a': 'b'},
             ('a', ('a', 'a'), ('a', 'a'), 'a',  'a'),
             ('b', ('b', 'b'), ('b', 'b'), 'b',  'b')),

            ({'b': 'a', 'a': 'b'},
             ('a', ('b', 'a'), ('b', 'a'), 'b', 'a'),
             ('b', ('a', 'b'), ('a', 'b'), 'a', 'b')),

            ({'i': 2, 'j': 'i'},
             ('a+j', ('i+a', 'i-j'), ('i+j', 'i-a'), 'a-j', 'a'),
             ('a+i', ('2+a', '2-i'), ('2+i', '2-a'), 'a-i', 'a')),

        ]

        for info in test_data:
            pattern = CentralVertexNumberingPattern(*info[1])
            pattern.substitute(**info[0], inplace=True)
            expected = CentralVertexNumberingPattern(*info[2])
            self.assertEqual(pattern, expected)

    def test_reverse(self):

        test_data = [
            # init formulas/
            # /reversed
            (('i', ('i', '2i'), ('2i', 'i'), 3,  4),
             ('i', ('2i', 'i'), ('i', '2i'), 4,  3)),

            (('a', ('i', '2i'),         ('3i', '2i', 'i'),  'b', 'a'),
             ('a', ('3i', '2i', 'i'),   ('i', '2i'),        'a', 'b')),

            (('2n', ('i', 'i-j'),   ('i+j', 'i-1'), '3c'        ),
             ('2n', ('i+j', 'i-1'), ('i', 'i-j'),   'inf',  '3c')),
        ]

        for info in test_data:
            pattern = CentralVertexNumberingPattern(*info[0])
            expected = CentralVertexNumberingPattern(*info[1])

            pattern.reverse(inplace=True)
            self.assertEqual(pattern, expected)