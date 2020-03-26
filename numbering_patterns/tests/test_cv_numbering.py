import unittest
from numbering_patterns.source.cv_numbering import CentralVertexNumbering
from numbering_patterns.source.ntr_sequence import NTermRecursionSequence
from numbering_patterns.source.linear_formula import LinearFormula
from numbering_patterns.source.linear_relation import LinearRelation

class TestCVN(unittest.TestCase):


    #-INIT--------------------------------------------------------------------

    def test_init(self):

        test_data = [
            # init args
            (4,     ('i', '2i'),    ('2i', 'i'),    3,      3       ),
            ('2n',  ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1'),
            (4,     ('i', '2i'),    ('2i', 'i')),
        ]

        for info in test_data:

            # pass sequences as strings
            pattern_1 = CentralVertexNumbering(*info)

            # pass sequences as <NTermRecursionSequence>
            args = list(info)
            args[1] = NTermRecursionSequence(*info[1])
            args[2] = NTermRecursionSequence(*info[2])
            pattern_2 = CentralVertexNumbering(*args)

            # init with kwargs
            kwargs = {}
            kwargs['center'] = info[0]
            kwargs['left_seq'] = info[1]
            kwargs['right_seq'] = info[2]
            if len(info) > 3:
                kwargs['l_len'] = info[3]
                kwargs['r_len'] = info[4]

            pattern_3 = CentralVertexNumbering(**kwargs)

            for pattern in [pattern_1, pattern_2, pattern_3]:
                self.assertEqual(pattern.center, LinearFormula(info[0]))

                left_seq = NTermRecursionSequence(*info[1])
                right_seq = NTermRecursionSequence(*info[2])
                self.assertEqual(pattern.left_seq, left_seq)
                self.assertEqual(pattern.right_seq, right_seq)

                if len(info) > 3:
                    self.assertEqual(pattern.left_len, LinearFormula(info[3]))
                    self.assertEqual(
                        pattern.right_len, LinearFormula(info[4]))
                else:
                    self.assertEqual(pattern.left_len, LinearFormula('inf'))
                    self.assertEqual(pattern.right_len, LinearFormula('inf'))

    def test_invalid_init(self):

        # default <ntuple_index>
        test_data = [
            # init args
            ('i',   ('i', '2i'),    ('2i', 'i'),    3,      3   ),
            (4,     ('i', '2i'),    ('2i', 'i'),    '2i',   3   ),
            (4,     ('i', '2i'),    ('2i', 'i'),    3,      '2i'),
            ('i',   ('j', '2j'),    ('2j', 'j'),    3,      3   ),
            (4,     ('j', '2j'),    ('2j', 'j'),    '2i',   3   ),
            (4,     ('j', '2j'),    ('2j', 'j'),    3,      '2i'),
        ]

        for args in test_data:
            self.assertRaises(ValueError, CentralVertexNumbering, *args)

        # custom <ntuple_index>
        test_data = [
            # init args
            ('j',   ('i', '2i'),    ('2i', 'i'),    3,      3   ),
            (4,     ('i', '2i'),    ('2i', 'i'),    '2j',   3   ),
            (4,     ('i', '2i'),    ('2i', 'i'),    3,      '2j'),
            ('j',   ('j', '2j'),    ('2j', 'j'),    3,      3   ),
            (4,     ('j', '2j'),    ('2j', 'j'),    '2j',   3   ),
            (4,     ('j', '2j'),    ('2j', 'j'),    3,      '2j'),
        ]

        for args in test_data:
            new_args = list(args)
            new_args[1] = NTermRecursionSequence(*args[1], ntuple_index='j')
            new_args[2] = NTermRecursionSequence(*args[2], ntuple_index='j')
            self.assertRaises(ValueError, CentralVertexNumbering, *new_args)

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def test_str(self):

        test_data = [
            # init args/
            # /string
            ((4,    ('i', '2i'),        ('2i', 'i'),    3,      3       ),
             'CVN(3|2i, i|<-{}|4|{}->|2i, i|3)'),

            (('2n', ('i', '2j', '3i'),  ('2i', 'j'),    '2k',   '2k + 1'),
             'CVN(2k|3i, 2j, i|<-{}|2n|{}->|2i, j|2k + 1)'),

            ((4,    ('i',),             ('2i', 'i')),
             'CVN(inf|i|<-{}|4|{}->|2i, i|inf)'),

        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[0])
            self.assertEqual(str(pattern), info[1].format('i', 'i'))

            args = list(info[0])
            args[1] = NTermRecursionSequence(*info[0][1], ntuple_index='p')
            args[2] = NTermRecursionSequence(*info[0][2], ntuple_index='q')
            pattern = CentralVertexNumbering(*args)
            self.assertEqual(str(pattern), info[1].format('p', 'q'))

    def test_eq(self):

        # equal
        test_data = [
            # init args
            (4,     ('i', '2i'),    ('2i', 'i'),    3,      3       ),
            ('2n',  ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1'),
            (4,     ('i', '2i'),    ('2i', 'i') ),
        ]

        for args in test_data:
            pattern_1 = CentralVertexNumbering(*args)
            pattern_2 = CentralVertexNumbering(*args)

            self.assertEqual(pattern_1, pattern_2)

        # not equal
        test_data = [
            # init args
            ((4,    ('i', '2i'),    ('2i', 'i'), 3, 3),     # pattern 1
             (4,    ('i', '2i'),    ('2i', 'i'))),          # pattern 2

            (('2',  ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1'),
             ('2n', ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1')),

            (('2',  ('i', '2i'),    ('2i', 'i')),
             ('2n', ('i', '2i'),    ('2i', 'i'))),

            ((4,    ('2i', 'i'),    ('i', '2i'), 3, 3),
             (4,    ('i', '2i'),    ('2i', 'i'), 3, 3)),
        ]

        for info in test_data:
            pattern_1 = CentralVertexNumbering(*info[0])
            pattern_2 = CentralVertexNumbering(*info[1])
            self.assertNotEqual(pattern_1, pattern_2)

    #-------------------------------------------------------------------------


    #-MODIFIERS---------------------------------------------------------------

    def test_zip(self):

        test_data = [
            # init formulas/
            # /zipped formulas
            (('a+a',    ('i+i', 'i+i'), ('i+i', 'i+i'), 'a+a',  'a+a'   ),
             ('2a',     ('2i', '2i'),   ('2i', '2i'),   '2a',   '2a'    )),

            (('b-b',    ('a-2a',),      ('i', 'i'),     'b+2b', '2c-c+b'),
             ('',       ('-a',),        ('i', 'i'),     '3b',   'c+b'   )),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[0])
            pattern.zip(inplace=True)

            expected = CentralVertexNumbering(*info[1])
            self.assertEqual(pattern, expected)

    def test_substitute(self):

        # substitute all
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

        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[1])
            pattern.substitute(**info[0], inplace=True)
            expected = CentralVertexNumbering(*info[2])
            self.assertEqual(pattern, expected)

        # only substitute in sequences
        test_data = [
            # {variable: substitute}/
            # /init formulas/
            # /formulas after substitution
            ({'i': 2, 'j': 'i'},
             ('a+j', ('i+a', 'i-j'), ('i+j', 'i-a'), 'a-j', 'a'),
             ('a+j', ('2+a', '2-i'), ('2+i', '2-a'), 'a-j', 'a')),

            ({'j': 'i'},
             ('j', ('j', 'j'), ('j', 'j'), 'j', 'j'),
             ('j', ('i', 'i'), ('i', 'i'), 'j', 'j')),

            ({'a': 'b'},
             ('a', ('a', 'a'), ('a', 'a'), 'a', 'a'),
             ('a', ('b', 'b'), ('b', 'b'), 'a', 'a')),

            ({'a': 'b'},
             ('a', (3, 4), (5, 6), 'a', 'a'),
             ('a', (3, 4), (5, 6), 'a', 'a')),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[1])
            pattern.substitute(**info[0], inplace=True, only_sequences=True)
            expected = CentralVertexNumbering(*info[2])
            self.assertEqual(pattern, expected)

        # errors with default <ntuple_index>
        test_data = [
            # {variable: substitute}/
            # /init formulas
            ({'i': 2, 'j': 'i'},
             ('a+j',    ('i+a', 'i-j'), ('i+j', 'i-a'), 'a-j', 'a'  )),

            ({'j': 'i'},
             ('j',      ('j', 'j'),     ('j', 'j'),     'j',    'j' )),

            ({'j': 'i'},
             (3,        ('j', 'j'),     ('j', 'j'),     4,      5   )),

        ]

        for info in test_data:
            seq = CentralVertexNumbering(*info[1])
            self.assertRaises(ValueError, seq.substitute, **info[0])

        # errors with custom <ntuple_index>
        test_data = [
            # {variable: substitute}/
            # /init formulas
            ({'j': 2, 'i': 'j'},
             ('a+i',    ('i+a', 'i-j'), ('i+j', 'i-a'), 'a-i', 'a'  )),

            ({'i': 'j'},
             ('i',      ('i', 'i'),     ('i', 'i'),     'i',    'i' )),

            ({'i': 'j'},
             (3,        ('i', 'i'),     ('i', 'i'),     4,      5   )),
        ]

        for info in test_data:
            args = list(info[1])
            args[1] = NTermRecursionSequence(*info[1][1], ntuple_index='j')
            args[2] = NTermRecursionSequence(*info[1][2], ntuple_index='j')
            seq = CentralVertexNumbering(*args)
            self.assertRaises(ValueError, seq.substitute, **info[0])

    def test_substitute_recursive(self):

        test_data = [
            # {variable: substitute}/
            # /init formulas/
            # /result
            ({'a': 'b', 'b': 'c'},
             ('a', ('a', 'b', 'c'), ('c', 'a', 'b'), 'b', 'c'),
             ('c', ('c', 'c', 'c'), ('c', 'c', 'c'), 'c', 'c')),

            ({'a': 'b', 'b': 'c'},
             ('a', ('a+b', 'b+a'),  ('2a+b', '2b+a'),   'a-b',  'a-2b'),
             ('c', ('2c', '2c'),    ('3c', '3c'),       '0',    '-c')),

            ({'a': 'c', 'b': 'c', 'c': 'd'},
             ('a', ('a+b', 'b+a'),  ('2a+b', '2b+a'),   'a-b',  'a-2b'),
             ('d', ('2d', '2d'),    ('3d', '3d'),       '0',    '-d')),

            ({'a': 'c', 'b': 'c', 'c': 'd'},
             ('a', ('a+b', 'b+a'),  ('2a+b', '2b+a')),
             ('d', ('2d', '2d'),    ('3d', '3d'))),

            ({'n': 'k', 'k': 't', 't': 1},
             ('2n', ('i', '2i+k'),  ('2n', 'n+2'),  'k',    'k+1'),
             (2,    ('i', '2i+1'),  (2, 3),         1,      2)),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[1])
            pattern.substitute(**info[0], recursive=True, inplace=True)
            pattern.zip(inplace=True)

            expected = CentralVertexNumbering(*info[2]).zip()

            self.assertEqual(pattern, expected)

    def test_reverse(self):

        test_data = [
            # init formulas/
            # /reversed
            (('a', ('i', '2i'), ('2i', 'i'), 3,  4),
             ('a', ('2i', 'i'), ('i', '2i'), 4,  3)),

            (('a', ('i', '2i'),         ('3i', '2i', 'i'),  'b', 'a'),
             ('a', ('3i', '2i', 'i'),   ('i', '2i'),        'a', 'b')),

            (('2n', ('i', 'i-j'),   ('i+j', 'i-1'), '3c'        ),
             ('2n', ('i+j', 'i-1'), ('i', 'i-j'),   'inf',  '3c')),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[0])
            expected = CentralVertexNumbering(*info[1])

            pattern.reverse(inplace=True)
            self.assertEqual(pattern, expected)

    def test_set_lengths(self):

        test_data = [
            # init args
            (4,     ('i', '2i'),    ('2i', 'i'),    3,      3       ),
            ('2n',  ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1'),
            (4,     ('i', '2i'),    ('2i', 'i')),
        ]

        lengths = [
            (5, 8), ('2k', '3k'), ('2n', 7),
            (LinearFormula(3), LinearFormula(6))
        ]

        for args in test_data:
            pattern = CentralVertexNumbering(*args)

            for l_len, r_len in lengths:
                pattern.set_lengths(l_len, r_len, inplace=True)
                self.assertEqual(pattern.left_len, LinearFormula(l_len))
                self.assertEqual(pattern.right_len, LinearFormula(r_len))

    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    def test_copy(self):
        pattern = CentralVertexNumbering(4, ('i', '2i'), ('2i', 'i'))

        # copy
        copy_of_pattern = pattern.copy()
        self.assertEqual(pattern, copy_of_pattern)

        # modify the copy
        copy_of_pattern.center = LinearFormula(5)
        self.assertNotEqual(pattern, copy_of_pattern)

        # copy again and modify the copy's attribute
        copy_of_pattern = pattern.copy()
        copy_of_pattern.left_seq.formulas[0] += '3c'
        self.assertNotEqual(pattern, copy_of_pattern)

    def test_evaluate(self):

        test_data = [
            # init args/
            # /(index, value)/
            # /(index, value) cd.
            ((4, ('i', '2i'), ('2i', 'i'), 3, 3),
             (0, 4),    (-1, 0),    (-2, 0),    (-3, 1),    (-4, 2),
             (1, 0),    (2, 0),     (3, 2),     (4, 1),     (5, 4)),

            (('2', ('a + i', '2i', '6i'), ('2i', 'i')),
             (0, 2),    (1, 0),     (2, 0),     (3, 2),         (4, 1),
             (-1, 'a'), (-2, 0),    (-3, 0),    (-4, 'a + 1'),  (-5, 2)),

            ((4, ('i',), ('2i',), 3, 3),
             (0, 4),    (1, 0),     (2, 2),     (3, 4),     (4, 6),
             (-1, 0),   (-2, 1),    (-3, 2),    (-4, 3),    (-5, 4)),

            ((4, ('i', 'i'), ('2i', '2i'), 3, 3),
             (0, 4),    (1, 0),     (2, 0),     (3, 2),     (4, 2),
             (-1, 0),   (-2, 0),    (-3, 1),    (-4, 1),    (-5, 2)),

            (('2n', ('3', '2'), ('a', 'i'), 3, 3),
             (0, '2n'), (1, 'a'),   (2, 0),     (3, 'a'),   (4, 1),
             (-1, 3),   (-2, 2),    (-3, 3),    (-4, 2),    (-5, 3)),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[0])
            for index, value in info[1:]:
                result = pattern.evaluate(index)
                expected_result = LinearFormula(value).zip()
                self.assertEqual(result, expected_result)

    def test_get_variables(self):

        test_data = [
            # init args                            variables in use
            ((4, ('i', '2i'), ('2i', 'i'), 3, 3),  {'i'}                    ),
            (('2', ('a + i', '6i'), ('2i', 'i')),  {'a', 'i'}               ),
            ((4, ('i',), ('2b',), 3, 3),           {'i', 'b'}               ),
            (('a', ('b',), ('c',), 'd', 'e'),      {'a', 'b', 'c', 'd', 'e'}),
            (('a', ('a',), ('a',), 'a', 'a'),      {'a'}                    ),
            (('2n', ('3', '2'), ('a', 'i'), 3, 3), {'n', 'a', 'i'}          ),
            (('0a', ('0b',), ('0c',), '0d', '0e'), {'a', 'b', 'c', 'd', 'e'}),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[0])

            # don't omit anything
            self.assertEqual(pattern.get_variables(), info[1])

            # omit local variables
            self.assertEqual(
                pattern.get_variables(global_only=True), info[1] - {'i'})

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

            (('0a', ('0b',), ('0c',), '0d', '0e'),  set()               ),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[0])
            self.assertEqual(pattern.get_variables(omit_zeros=True), info[1])

    def test_ntuple_index_inequality(self):

        test_data = [
            # n     length
            (3,     'l',
             # no_formula\no_last_formula
             (('3i <= l-1', '3i <= l-2', '3i <= l-3'),
              ('3i <= l-4', '3i <= l-2', '3i <= l-3'),
              ('3i <= l-4', '3i <= l-5', '3i <= l-3'),)),
            # n     length
            (3,     'l',
             # no_formula\no_last_formula
             (('3i+1 <= l',     '3i+1 <= l-1',  '3i+1 <= l-2'),
              ('3i+2 <= l-2',   '3i+2 <= l',    '3i+2 <= l-1'),
              ('3i+3 <= l-1',   '3i+3 <= l-2',  '3i+3 <= l'),)),
            # n     length
            (4,     'l',
             # no_formula\no_last_formula
             (('4i+1 <= l',   '4i+1 <= l-1', '4i+1 <= l-2', '4i+1 <= l-3'),
              ('4i+2 <= l-3', '4i+2 <= l',   '4i+2 <= l-1', '4i+2 <= l-2'),
              ('4i+3 <= l-2', '4i+3 <= l-3', '4i+3 <= l',   '4i+3 <= l-1'),
              ('4i+4 <= l-1', '4i+4 <= l-2', '4i+4 <= l-3', '4i+4 <= l'),)),
        ]

        for info in test_data:
            n = info[0]
            length = info[1]
            pattern = CentralVertexNumbering(1, n*[1], n*[1], length, length)
            for no_f in range(n):
                for no_last_f in range(n):

                    expected = LinearRelation(info[2][no_f][no_last_f])
                    actual = pattern.get_ntuple_index_inequality(
                        side='left',
                        no_formula=no_f,
                        no_last_formula=no_last_f
                    )
                    self.assertTrue(expected.equivalent(actual))
                    actual = pattern.get_ntuple_index_inequality(
                        side='right',
                        no_formula=no_f,
                        no_last_formula=no_last_f
                    )
                    self.assertTrue(expected.equivalent(actual))

        test_data = [
            # n     inequalities
            #   length
            (3, 3,  ('i <= 0', 'i <= 0', 'i <= 0')),
            (3, 4,  ('i <= 1', 'i <= 0', 'i <= 0')),
            (3, 5,  ('i <= 1', 'i <= 1', 'i <= 0')),
            (3, 6,  ('i <= 1', 'i <= 1', 'i <= 1')),
            (3, 7,  ('i <= 2', 'i <= 1', 'i <= 1')),
            (4, 4,  ('i <= 0', 'i <= 0', 'i <= 0', 'i <= 0')),
            (4, 6,  ('i <= 1', 'i <= 1', 'i <= 0', 'i <= 0')),
            (4, 9,  ('i <= 2', 'i <= 1', 'i <= 1', 'i <= 1')),
            (5, 12, ('i <= 2', 'i <= 2', 'i <= 1', 'i <= 1', 'i <= 1')),
        ]

        for info in test_data:
            n = info[0]
            length = info[1]
            pattern = CentralVertexNumbering(1, n*[1], n*[1], length, length)
            for no_f in range(n):
                no_last_f = (length - 1) % n
                expected = LinearRelation(info[2][no_f])
                actual = pattern.get_ntuple_index_inequality(
                    side='left',
                    no_formula=no_f,
                    no_last_formula=no_last_f
                )
                self.assertTrue(expected.equivalent(actual))
                actual = pattern.get_ntuple_index_inequality(
                    side='right',
                    no_formula=no_f,
                    no_last_formula=no_last_f
                )
                self.assertTrue(expected.equivalent(actual))

    def test_get_edges(self):

        test_data = [
            ((1, (1, 1, 1), (1, 1)),
             (2, 2, [2, 2, 2], [2, 2])),

            (('a', ('i', 'i+1', 'i+2'), ('i-1', 'i-2')),
             ('a', 'a-1', ['2i+1', '2i+3', '2i+3'], ['2i-3', '2i-2'])),
        ]

        for info in test_data:

            # test with default ntuple index
            pattern = CentralVertexNumbering(*info[0])

            center_left = LinearFormula(info[1][0])
            center_right = LinearFormula(info[1][1])

            left = [LinearFormula(string).zip() for string in info[1][2]]
            right = [LinearFormula(string).zip() for string in info[1][3]]

            result = pattern.get_edges()

            self.assertEqual(result['center left'], center_left)
            self.assertEqual(result['center right'], center_right)
            self.assertEqual(result['left'], left)
            self.assertEqual(result['right'], right)

            # test with custom ntuple indices
            formulas = []
            for formula in info[0][1]:
                formulas.append(LinearFormula(formula).substitute(i='p'))
            left_seq = NTermRecursionSequence(*formulas, ntuple_index='p')

            formulas = []
            for formula in info[0][2]:
                formulas.append(LinearFormula(formula).substitute(i='q'))
            right_seq = NTermRecursionSequence(*formulas, ntuple_index='q')

            pattern = CentralVertexNumbering(info[0][0], left_seq, right_seq)

            for i in range(len(left)):
                left[i].substitute(i='p', inplace=True)

            for i in range(len(right)):
                right[i].substitute(i='q', inplace=True)

            result = pattern.get_edges()
            self.assertEqual(result['center left'], center_left)
            self.assertEqual(result['center right'], center_right)
            self.assertEqual(result['left'], left)
            self.assertEqual(result['right'], right)

    #-------------------------------------------------------------------------
