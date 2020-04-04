import unittest
from ..source.cv_numbering import CentralVertexNumbering
from ..source.ntr_sequence import NTermRecursionSequence
from ..source.linear_formula import LinearFormula
from ..source.linear_relation import LinearRelation

class TestCVN(unittest.TestCase):


    #-INIT--------------------------------------------------------------------

    def test_init(self):

        # init with formulas and sequences
        center = LinearFormula('a + b')
        left_seq = NTermRecursionSequence('i', '2i', '3', length='4k')
        right_seq = NTermRecursionSequence('-4i', '2i', 'i+1', length='6k+2')

        pattern = CentralVertexNumbering(center, left_seq, right_seq)
        self.assertEqual(pattern.center, center)
        self.assertEqual(pattern.left_seq, left_seq)
        self.assertEqual(pattern.right_seq, right_seq)
        self.assertEqual(pattern.ntuple_index, 'i')
        self.assertEqual(pattern.ntuple_index, pattern.left_seq.ntuple_index)
        self.assertEqual(pattern.ntuple_index, pattern.right_seq.ntuple_index)

        # overwrite lengths and the 'ntuple index'
        pattern = CentralVertexNumbering(
            center, left_seq, right_seq,
            ntuple_index='j',
            left_len='5l+4',
            right_len='7l'
        )
        self.assertEqual(pattern.center, center)
        for i in range(3):
            self.assertEqual(
                pattern.left_seq.formulas[i],
                left_seq.formulas[i].substitute(i='j')
            )
            self.assertEqual(
                pattern.right_seq.formulas[i],
                right_seq.formulas[i].substitute(i='j')
            )

        self.assertEqual(pattern.ntuple_index, 'j')
        self.assertEqual(pattern.left_seq.length, LinearFormula('5l+4'))
        self.assertEqual(pattern.right_seq.length, LinearFormula('7l'))

        # different 'ntuple indices'
        pattern = CentralVertexNumbering(
            center, left_seq, right_seq.set_ntuple_index('j'))

        self.assertEqual(pattern.left_seq, left_seq)
        self.assertEqual(pattern.right_seq, right_seq)
        self.assertEqual(pattern.ntuple_index, 'i')
        self.assertEqual(pattern.left_seq.ntuple_index, 'i')
        self.assertEqual(pattern.right_seq.ntuple_index, 'i')

        # init with strings
        pattern = CentralVertexNumbering(
            'a + b', ('i', '2i', '3'), ('-4i', '2i', 'i+1'))

        self.assertEqual(pattern.center, LinearFormula('a + b'))
        self.assertEqual(
            pattern.left_seq, NTermRecursionSequence('i', '2i', '3'))
        self.assertEqual(
            pattern.right_seq, NTermRecursionSequence('-4i', '2i', 'i+1'))

        self.assertEqual(pattern.ntuple_index, 'i')
        self.assertEqual(pattern.left_seq.ntuple_index, 'i')
        self.assertEqual(pattern.right_seq.ntuple_index, 'i')

        # init with another pattern
        pattern = CentralVertexNumbering(
            'a + b', ('i', '2i', '3'), ('-4i', '2i', 'i+1'),
            ntuple_index='j', left_len='4k', right_len='5k'
        )

        pattern_2 = CentralVertexNumbering(pattern)
        self.assertEqual(pattern.center, pattern_2.center)
        self.assertEqual(pattern.left_seq, pattern_2.left_seq)
        self.assertEqual(pattern.right_seq, pattern_2.right_seq)
        self.assertEqual(pattern.ntuple_index, pattern_2.ntuple_index)




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
            self.assertRaises(
                ValueError, CentralVertexNumbering,
                *args[:3], left_len=args[3], right_len=args[4])

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
            new_args = list(args[:3])
            new_args[1] = NTermRecursionSequence(*args[1], ntuple_index='j')
            new_args[2] = NTermRecursionSequence(*args[2], ntuple_index='j')
            self.assertRaises(
                ValueError, CentralVertexNumbering,
                *new_args, left_len=args[3], right_len=args[4])

        # invalid ntuple_indices
        left_seq = NTermRecursionSequence('2i', 'i', '4i')
        right_seq = NTermRecursionSequence(
            '3j', 'j+i', '4j-3i', ntuple_index='j')
        self.assertRaises(
            ValueError, CentralVertexNumbering, 'a', left_seq, right_seq)

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def test_str(self):

        test_data = [

            ((4,    ('i', '2i'),        ('2i', 'i')),       # init args
             {'left_len': 3,    'right_len': 3},            # init kwargs
             'CVN(3<-|2i, i|<-i|4|i->|2i, i|->3)'),         # string

            (('2n', ('i', '2i', '3i'),  ('2i', 'i')),
             {'left_len': '2k', 'right_len': '2k + 1'},
             'CVN(2k<-|3i, 2i, i|<-i|2n|i->|2i, i|->2k + 1)'),

            (('2n', ('i', '2i', '3i'),  ('2i', 'i')),
             {'left_len': '2k', 'right_len': '2k + 1',  'ntuple_index': 'j'},
             'CVN(2k<-|3j, 2j, j|<-j|2n|j->|2j, j|->2k + 1)'),

            ((4,    ('i',),             ('2i', 'i')),
             {},
             'CVN(inf<-|i|<-i|4|i->|2i, i|->inf)'),

            ((4,    ('i',),             ('2i', 'i')),
             {'ntuple_index': 'j'},
             'CVN(inf<-|j|<-j|4|j->|2j, j|->inf)'),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(*info[0], **info[1])
            self.assertEqual(str(pattern), info[2])

    def test_eq(self):

        # equal
        test_data = [
            # custom lengths
            ((4,    ('i', '2i'),    ('2i', 'i')),       # init args
             {'left_len': 3,    'right_len': 3}),       # init kwargs

            (('2n', ('i', '2i'),    ('2i', 'i')),
             {'left_len': '2k', 'right_len': '2k + 1'}),

            # default everything
            ((4,    ('i', '2i'),    ('2i', 'i')),
             {}),

            # custom ntuple index
            ((4,    ('i', '2i'),    ('2i', 'i')),
             {'ntuple_index': 'j'}),

            # custom everythong
            ((4,    ('i', '2i'),    ('2i', 'i')),
             {'left_len': '2k', 'right_len': '2k + 1', 'ntuple_index': 'j'}),
        ]

        for info in test_data:
            pattern_1 = CentralVertexNumbering(*info[0], **info[1])
            pattern_2 = CentralVertexNumbering(*info[0], **info[1])

            self.assertEqual(pattern_1, pattern_2)

        # not equal
        test_data = [

            # different lengths
            ((4,    ('i', '2i'),    ('2i', 'i')),   # pattern 1 init args
             (4,    ('i', '2i'),    ('2i', 'i')),   # pattern 2 init args
             {'left_len': 3,    'right_len': 3},    # pattern 1 init kwargs
             {}),                                   # pattern 2 init kwargs

            # different left length
            ((4, ('i', '2i'), ('2i', 'i')),
             (4, ('i', '2i'), ('2i', 'i')),
             {'left_len': 3, 'right_len': 3},
             {'left_len': '3k', 'right_len': 3}),

            # different right length
            ((4, ('i', '2i'), ('2i', 'i')),
             (4, ('i', '2i'), ('2i', 'i')),
             {'left_len': 3, 'right_len': 3},
             {'left_len': 3, 'right_len': '3k'}),

            # different centers (with lengths)
            (('2',  ('i', '2i'),    ('2i', 'i')),
             ('2n', ('i', '2i'),    ('2i', 'i')),
             {'left_len': '2k', 'right_len': '2k + 1'},
             {'left_len': '2k', 'right_len': '2k + 1'}),

            # different centers (no lengths)
            (('2',  ('i', '2i'),    ('2i', 'i')),
             ('2n', ('i', '2i'),    ('2i', 'i')),
             {}, {}),

            # different left sequnce
            ((4,    ('2i', 'i'),    ('i', '2i')),
             (4,    ('i', '2i'),    ('i', '2i')),
             {}, {}),

            # different right sequnces
            ((4, ('2i', 'i'), ('i', '2i')),
             (4, ('2i', 'i'), ('2i', 'i')),
             {}, {}),

            # different ntuple indices (no lengths)
            (('2',  ('i', '2i'),    ('2i', 'i')),
             ('2',  ('i', '2i'),    ('2i', 'i')),
             {'ntuple_index': 'j'}, {}),

            # different ntuple indices (with lengths)
            (('2',  ('i', '2i'),    ('2i', 'i')),
             ('2',  ('i', '2i'),    ('2i', 'i')),
             {'left_len': '2k', 'right_len': '2k + 1', 'ntuple_index': 'j'},
             {'left_len': '2k', 'right_len': '2k + 1'}),
        ]

        for info in test_data:
            pattern_1 = CentralVertexNumbering(*info[0], **info[2])
            pattern_2 = CentralVertexNumbering(*info[1], **info[3])
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
            pattern = CentralVertexNumbering(
                *info[0][:3], left_len=info[0][3], right_len=info[0][4])
            pattern.zip(inplace=True)

            expected = CentralVertexNumbering(
                *info[1][:3], left_len=info[1][3], right_len=info[1][4])

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
            pattern = CentralVertexNumbering(
                *info[1][:3], left_len=info[1][3], right_len=info[1][4])
            pattern.substitute(**info[0], inplace=True)
            expected = CentralVertexNumbering(
                *info[2][:3], left_len=info[2][3], right_len=info[2][4])
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
            pattern = CentralVertexNumbering(
                *info[1][:3], left_len=info[1][3], right_len=info[1][4])
            pattern.substitute(**info[0], inplace=True, only_sequences=True)
            expected = CentralVertexNumbering(
                *info[2][:3], left_len=info[2][3], right_len=info[2][4])
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
            seq = CentralVertexNumbering(
                *info[1][:3], left_len=info[1][3], right_len=info[1][4])
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
            args = list(info[1][:3])
            args[1] = NTermRecursionSequence(*info[1][1], ntuple_index='j')
            args[2] = NTermRecursionSequence(*info[1][2], ntuple_index='j')
            seq = CentralVertexNumbering(
                *args, left_len=info[1][3], right_len=info[1][4])
            self.assertRaises(ValueError, seq.substitute, **info[0])

    def test_substitute_recursive(self):

        test_data = [
            # {variable: substitute}/
            # /init formulas/
            # /result
            ({'a': 'b', 'b': 'c'},
             ('a', ('a', 'b', 'c'), ('c', 'a', 'b'),    'b',    'c'),
             ('c', ('c', 'c', 'c'), ('c', 'c', 'c'),    'c',    'c')),

            ({'a': 'b', 'b': 'c'},
             ('a', ('a+b', 'b+a'),  ('2a+b', '2b+a'),   'a-b',  'a-2b'),
             ('c', ('2c', '2c'),    ('3c', '3c'),       '0',    '-c')),

            ({'a': 'c', 'b': 'c', 'c': 'd'},
             ('a', ('a+b', 'b+a'),  ('2a+b', '2b+a'),   'a-b',  'a-2b'),
             ('d', ('2d', '2d'),    ('3d', '3d'),       '0',    '-d')),

            ({'n': 'k', 'k': 't', 't': 1},
             ('2n', ('i', '2i+k'),  ('2n', 'n+2'),      'k',    'k+1'),
             (2,    ('i', '2i+1'),  (2, 3),             1,      2)),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(
                *info[1][:3], left_len=info[1][3], right_len=info[1][4])
            pattern.substitute(**info[0], recursive=True, inplace=True)
            pattern.zip(inplace=True)

            expected = CentralVertexNumbering(
                *info[2][:3], left_len=info[2][3], right_len=info[2][4]).zip()

            self.assertEqual(pattern, expected)

    def test_reverse(self):

        test_data = [
            # init formulas/
            # /reversed
            (('a', ('i', '2i'), ('2i', 'i'), 3,  4),
             ('a', ('2i', 'i'), ('i', '2i'), 4,  3)),

            (('a', ('i', '2i'),         ('3i', '2i', 'i'),  'b', 'a'),
             ('a', ('3i', '2i', 'i'),   ('i', '2i'),        'a', 'b')),

            (('2n', ('i', 'i-j'),   ('i+j', 'i-1'), '3c', '4d'),
             ('2n', ('i+j', 'i-1'), ('i', 'i-j'),   '4d', '3c')),
        ]

        for info in test_data:
            pattern = CentralVertexNumbering(
                *info[0][:3], left_len=info[0][3], right_len=info[0][4])
            expected = CentralVertexNumbering(
                *info[1][:3], left_len=info[1][3], right_len=info[1][4])

            pattern.reverse(inplace=True)
            self.assertEqual(pattern, expected)

    def test_set_lengths(self):

        test_data = [
            # init formulas
            (4,     ('i', '2i'),    ('2i', 'i'),    3,      3       ),
            ('2n',  ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1'),
            (4,     ('i', '2i'),    ('2i', 'i'),    '2n',   7       ),
        ]

        for args in test_data:
            pattern = CentralVertexNumbering(*args[:3])
            expected = CentralVertexNumbering(
                *args[:3], left_len=args[3], right_len=args[4])

            pattern.set_lengths(args[3], args[4], inplace=True)
            self.assertEqual(pattern, expected)
            self.assertEqual(pattern.left_seq.length, LinearFormula(args[3]))
            self.assertEqual(pattern.right_seq.length, LinearFormula(args[4]))

    def test_set_ntuple_index(self):

        center = 4
        left_args = ('i', '2i', '3i')
        right_args = ('2i', '-2i', 'i')

        left_seq = NTermRecursionSequence(*left_args)
        right_seq = NTermRecursionSequence(*right_args)

        pattern = CentralVertexNumbering(
            center, left_args, right_args)
        expected = CentralVertexNumbering(
            center, left_args, right_args, ntuple_index='j')

        pattern.set_ntuple_index('j', inplace=True)

        self.assertEqual(pattern, expected)
        self.assertEqual(pattern.ntuple_index, 'j')

        self.assertEqual(
            pattern.left_seq, left_seq.set_ntuple_index('j'))
        self.assertEqual(
            pattern.right_seq, right_seq.set_ntuple_index('j'))

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
            ((4, ('i', '2i'), ('2i', 'i')),
             (0, 4),    (-1, 0),    (-2, 0),    (-3, 1),    (-4, 2),
             (1, 0),    (2, 0),     (3, 2),     (4, 1),     (5, 4)),

            (('2', ('a + i', '2i', '6i'), ('2i', 'i')),
             (0, 2),    (1, 0),     (2, 0),     (3, 2),         (4, 1),
             (-1, 'a'), (-2, 0),    (-3, 0),    (-4, 'a + 1'),  (-5, 2)),

            ((4, ('i',), ('2i',)),
             (0, 4),    (1, 0),     (2, 2),     (3, 4),     (4, 6),
             (-1, 0),   (-2, 1),    (-3, 2),    (-4, 3),    (-5, 4)),

            ((4, ('i', 'i'), ('2i', '2i')),
             (0, 4),    (1, 0),     (2, 0),     (3, 2),     (4, 2),
             (-1, 0),   (-2, 0),    (-3, 1),    (-4, 1),    (-5, 2)),

            (('2n', ('3', '2'), ('a', 'i')),
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
            args = info[0][:3]
            kwargs = {}
            if len(info[0]) > 3:
                kwargs['left_len'] = info[0][3]
                kwargs['right_len'] = info[0][4]

            pattern = CentralVertexNumbering(*args, **kwargs)

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
            pattern = CentralVertexNumbering(
                *info[0][:3], left_len=info[0][3], right_len=info[0][4])
            self.assertEqual(pattern.get_variables(omit_zeros=True), info[1])

    def test_get_edge(self):

        test_data = [
            ((1, (1, 1, 1), (1, 1)),
             (2, 2, [2, 2, 2], [2, 2])),

            (('a', ('i', 'i+1', 'i+2'), ('i-1', 'i-2')),
             ('a', 'a-1', ['2i+1', '2i+3', '2i+3'], ['2i-3', '2i-2'])),
        ]

        for info in test_data:

            # test with default ntuple index
            pattern = CentralVertexNumbering(*info[0])
            ctrl_pattern = CentralVertexNumbering(*info[0])

            center_left = LinearFormula(info[1][0])
            center_right = LinearFormula(info[1][1])

            left = info[1][2]
            right = info[1][3]

            self.assertEqual(
                pattern.get_edge('left', 'center').zip(), center_left)
            self.assertEqual(
                pattern.get_edge('right', 'center').zip(), center_right)

            for i in range(len(left)):
                self.assertEqual(
                    pattern.get_edge('left', i).zip(),
                    LinearFormula(left[i])
                )

            for i in range(len(right)):
                self.assertEqual(
                    pattern.get_edge('right', i).zip(),
                    LinearFormula(right[i])
                )

            self.assertEqual(pattern, ctrl_pattern)

            # test with custom ntuple indices
            pattern = CentralVertexNumbering(*info[0], ntuple_index='j')

            self.assertEqual(
                pattern.get_edge('left', 'center').zip(), center_left)
            self.assertEqual(
                pattern.get_edge('right', 'center').zip(), center_right)

            for i in range(len(left)):
                self.assertEqual(
                    pattern.get_edge('left', i).zip(),
                    LinearFormula(left[i]).substitute(i='j')
                )

            for i in range(len(right)):
                self.assertEqual(
                    pattern.get_edge('right', i).zip(),
                    LinearFormula(right[i]).substitute(i='j')
                )

    #-------------------------------------------------------------------------
