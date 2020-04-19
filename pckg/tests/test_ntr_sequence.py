import unittest
from ..source.ntr_sequence import NTermRecursionSequence
from ..source.linear_formula import LinearFormula
from ..source.linear_relation import LinearRelation

class TestNTRSequence(unittest.TestCase):


    #-INIT--------------------------------------------------------------------

    def test_init(self):

        test_data = [
            # init args
            ('a + b', '3i + 4', '4i'),
            ('i',),
            ('i',),
            ('1', 'a'),
            ('i', 'j'),
        ]

        for args in test_data:

            # init with strings
            seq = NTermRecursionSequence(*args)
            n = len(args)

            self.assertEqual(seq.n, n)
            self.assertEqual(len(seq.formulas), n)
            for i in range(n):
                self.assertEqual(LinearFormula(args[i]), seq.formulas[i])
                self.assertEqual((type(seq.formulas[i])), LinearFormula)

            self.assertEqual(seq.ntuple_index, 'i')
            self.assertEqual(seq.length, LinearFormula('inf'))

            seq = NTermRecursionSequence(
                *args, length='4k', ntuple_index='xxx')
            self.assertEqual(seq.ntuple_index, 'xxx')
            self.assertEqual(seq.length, LinearFormula('4k'))

            # init with formulas
            new_args = []
            for i in range(n):
                new_args.append(LinearFormula(args[i]))

            seq = NTermRecursionSequence(
                *new_args, length=LinearFormula('4k'))
            self.assertEqual(seq.n, n)
            for i in range(n):
                self.assertEqual(new_args[i], seq.formulas[i])
                self.assertEqual(seq.length, LinearFormula('4k'))

            # init with another sequence
            seq = NTermRecursionSequence(
                *args, length='4k', ntuple_index='yyy')

            new_seq = NTermRecursionSequence(seq)
            self.assertEqual(seq.n, n)
            for i in range(n):
                self.assertEqual(seq.formulas[i], new_seq.formulas[i])
            self.assertEqual(new_seq.ntuple_index, 'yyy')
            self.assertEqual(new_seq.length, LinearFormula('4k'))

            new_seq = NTermRecursionSequence(
                seq, ntuple_index='xxx', length='8p')
            self.assertEqual(new_seq.ntuple_index, 'xxx')
            self.assertEqual(new_seq.length, LinearFormula('8p'))

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def test_str(self):

        test_data = [
            # init args               string
            ('a + b', '3i + 4', '4i', '3-TRSeq({}->|a + b, 3i + 4, 4i|->{})'),
            ('i',                     '1-TRSeq({}->|i|->{})'                ),
            ('1', 'a',                '2-TRSeq({}->|1, a|->{})'             ),
        ]

        for info in test_data:
            args = info[:-1]
            seq = NTermRecursionSequence(*args)
            self.assertEqual(str(seq), info[-1].format('i', 'inf'))

            seq = NTermRecursionSequence(*args, length='5l', ntuple_index='j')
            self.assertEqual(str(seq), info[-1].format('j', '5l'))

    def test_eq(self):

        test_data = [
            (('a + b', '3i + 4', '4i'), '5l', 'i'),
            (('a + b',), '6k', 'j'),
        ]

        for info in test_data:
            seq_1 = NTermRecursionSequence(
                *info[0], length=info[1], ntuple_index=info[2])
            seq_2 = NTermRecursionSequence(
                *info[0], length=info[1], ntuple_index=info[2])
            self.assertEqual(seq_1, seq_2)

        test_data = [
            (('a + b', '3i + 4', '4i'), 'inf',  'i',
             ('b + a', '3i + 4', '4i'), 'inf',  'i'),

            (('a + b',),                'inf',  'i',
             ('4i', '5i'),              'inf',  'i'),

            (('a + b', '4i', '5i'),     'inf',  'i',
             ('4i', '5i', 'a + b'),     'inf',  'i'),

            (('2i', '2i', '2i'),        'inf',  'i',
             ('2i', '2i'),              'inf',  'i'),

            (('a + b', '3i + 4', '4i'), 'inf',  'i',
             ('a + b', '3i + 4', '4i'), 'inf',  'j'),

            (('a + b', '3i + 4', '4i'), '4k',   'i',
             ('a + b', '3i + 4', '4i'), '5k',   'i'),

            (('i', 'i', 'i'),           'inf',  'i',
             ('i', 'i', 'i'),           'inf',  'j'),

            (('i', 'i', 'i'),           'inf',  'a',
             ('i', 'i', 'i'),           'inf',  'b'),

            (('i', 'i', 'i'),           32,     'a',
             ('i', 'i', 'i'),           14,     'b'),
        ]

        for info in test_data:
            seq_1 = NTermRecursionSequence(
                *info[0], length=info[1], ntuple_index=info[2])
            seq_2 = NTermRecursionSequence(
                *info[3], length=info[4], ntuple_index=info[5])
            self.assertNotEqual(seq_1, seq_2)

    #-------------------------------------------------------------------------


    #-MODIFIERS---------------------------------------------------------------

    def test_zip(self):

        test_data = [
            # init args
            ('a + b + a', '3i + 4i', '4i',  '3k+k'),
            ('i - i', 'i',                  'inf'),
            ('i + i',                       '3k'),
            ('1 + 1', 'a',                  'k-k'),
        ]

        for info in test_data:
            args = info[:-1]
            seq = NTermRecursionSequence(*args, length=info[-1]).zip()
            for i in range(len(args)):
                zipped_formula = LinearFormula(args[i]).zip()
                self.assertEqual((seq.formulas[i]), zipped_formula)

    def test_substitute(self):

        # everything
        test_data = [
            # init args                 length  {variable: substitute}
            (('a + b', '3i + 4', '4i'), '3a',   {'a': 'x + 2'}              ),
            (('a + b', '3i + 4', '4i'), '3k',   {'i': 'b + 1'}              ),
            (('i', 'i'),                56,     {'i': '2'}                  ),
            (('a + 2', 'a'),            'a+b',  {'a': '3b'}                 ),
            (('a + b', '3i + 4', '4i'), 'a',    {'a': 'x + 2', 'i': '23'}   ),
            (('a + i', 'b - i'),        'a+b',  {'a': 'x + 2', 'b': '2c'}   ),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0], length=info[1])
            ntuple_index = seq.ntuple_index

            seq.substitute(**info[2], inplace=True)

            for i in range(len(info[0])):
                formula = LinearFormula(info[0][i]).substitute(**info[2])
                self.assertEqual(seq.formulas[i], formula)

            formula = LinearFormula(info[1]).substitute(**info[2])
            self.assertEqual(seq.length, formula)
            self.assertEqual(seq.ntuple_index, ntuple_index)

        # formulas only
        test_data = [
            # init args                 length  {variable: substitute}
            (('a + b', '3i + 4', '4i'), '3a',   {'a': 'x + 2'}              ),
            (('a + b', '3i + 4', '4i'), '3k',   {'i': 'i + 1'}              ),
            (('i', 'i'),                56,     {'i': '2i'}                 ),
            (('a + 2', 'a'),            'a+b',  {'a': '3i'}                 ),
            (('a + b', '3i + 4', '4i'), 'a',    {'a': 'x + 2', 'i': '2i'}   ),
            (('a + i', 'b - i'),        'a',    {'a': 'x + 2', 'b': '2i'}   ),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0], length=info[1])
            ntuple_index = seq.ntuple_index

            seq.substitute(**info[2], formulas_only=True, inplace=True)

            for i in range(len(info[0])):
                formula = LinearFormula(info[0][i]).substitute(**info[2])
                self.assertEqual(seq.formulas[i], formula)

            self.assertEqual(seq.length, LinearFormula(info[1]))
            self.assertEqual(seq.ntuple_index, ntuple_index)

    def test_substitute_recursive(self):

        test_data = [
            # init formulas/    {variable: substitute}
            # /result
            (('a', 'b', 'c'),   {'a': 'b', 'b': 'c'},
             ('c', 'c', 'c')                                    ),
            (('a+b', 'b+a'),    {'a': 'b', 'b': 'c'},
             ('2c', '2c')                                       ),
            (('a+b', 'b+a+c'),  {'a': 'b', 'b': 'c'},
             ('2c', '3c')                                       ),
            (('a+b', 'b+a'),    {'a': 'c', 'b': 'c', 'c': 'd'},
             ('2d', '2d')                                       ),
            (('a+b',),          {'a': 'k+1', 'b': 'k-2'},
             ('2k-1',)                                          ),
            (('a', 'a+2', 'b'), {'c': 'd', 'b': 'c', 'a': 'b'},
             ('d', 'd+2', 'd')                                  ),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0])
            seq.substitute(**info[1], recursive=True, inplace=True)

            self.assertEqual(seq.zip(), NTermRecursionSequence(*info[2]).zip())

    def test_set_length(self):

        seq = NTermRecursionSequence('i', '2i', '3i', length='5k')
        seq.set_length('8l+2', inplace=True)
        self.assertEqual(seq.length, LinearFormula('8l+2'))

        seq.set_length(45, inplace=True)
        self.assertEqual(seq.length, LinearFormula(45))

        self.assertRaises(ValueError, seq.set_length, '3i+k')

    def test_set_ntuple_index(self):

        seq = NTermRecursionSequence('i', '2i', '3i', length='5k')
        seq.set_ntuple_index('j', inplace=True)
        expected_seq = NTermRecursionSequence(
            'j', '2j', '3j', length='5k', ntuple_index='j')
        self.assertEqual(seq, expected_seq)
        self.assertRaises(ValueError, seq.set_ntuple_index, 'k')
        self.assertRaises(TypeError, seq.set_ntuple_index, 3)
        self.assertRaises(TypeError, seq.set_ntuple_index, LinearFormula('j'))

    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    def test_copy(self):
        seq = NTermRecursionSequence(
            'a + i', '3i', 'i + 3', length='4k', ntuple_index='j')
        copy_of_seq = seq.copy()
        self.assertEqual(seq, copy_of_seq)

        copy_of_seq.formulas[0] = LinearFormula('-4i + a')
        self.assertNotEqual(seq, copy_of_seq)

    def test_formulas_str(self):

        test_data = [
            # init args/
            # /string                   reversed=True
            (('a + b', '3i + 4', '4i'),
             'a + b, 3i + 4, 4i',       '4i, 3i + 4, a + b'),
            (('i',),
             'i',                       'i'),
            (('1', 'a'),
             '1, a',                    'a, 1'),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0])
            self.assertEqual(seq.formulas_str(), info[1])
            self.assertEqual(seq.formulas_str(reversed=True), info[2])

    def test_evaluate(self):

        test_data = [
            # init args                 ntuple  index   index-th number
            #                           index
            (('a + b', '3i + 4', '4i'), 'i',    4,      7       ),
            (('a + b', '3i + 4', '4i'), 'i',    0,      'a + b' ),
            (('a + b', '3i + 4', '4i'), 'i',    1,      '4'     ),
            (('a + b', '3i + 4', '4i'), 'i',    2,      0       ),
            (('i', 'i'),                'i',    0,      0       ),
            (('i', 'i'),                'i',    1,      0       ),
            (('i', 'i'),                'i',    2,      1       ),
            (('i',),                    'i',    4,      4       ),
            (('i',),                    'i',    3,      3       ),
            (('1', 'a'),                'i',    4,      1       ),
            (('a', 'b'),                'i',    4,      'a'     ),
            (('a + i', 'b - i'),        'i',    4,      'a + 2' ),
            (('a + i', 'b - i'),        'i',    6,      'a + 3' ),
            (('a + i', 'b - i'),        'i',    5,      'b - 2' ),
            (('a + j', 'b - j'),        'j',    4,      'a + 2' ),
            (('a + j', 'b - j'),        'j',    6,      'a + 3' ),
            (('a + j', 'b - j'),        'j',    5,      'b - 2' ),
            (('j', 'j'),                'j',    2,      1       ),
            (('j',),                    'j',    4,      4       ),
            (('j',),                    'j',    3,      3       ),
            (('i', 'i'),                'j',    2,      'i'     ),


        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0], ntuple_index=info[1])
            index = info[2]
            expected_result = LinearFormula(info[3]).zip()

            self.assertEqual(seq.evaluate(index), expected_result)

    def test_get_variables(self):

        test_data = [
            (('a + b', '3i + 4', '4i'),     '4k',   {'a', 'b', 'i', 'k'}),
            (('a + b + 3a', 'i'),           '3a',   {'a', 'b', 'i'}     ),
            (('a + b', 'a + 2b'),           '5b',   {'a', 'b'}          ),
            (('a', 'aa'),                   'k',    {'a', 'aa', 'k'}    ),
            (('i', 'i'),                    'inf',  {'i'}               ),
            (('a + 2', 'a') ,               'inf',  {'a'}               ),
            (('a + 2', 'a + i'),            'inf',  {'a', 'i'}          ),
            (('a + b', '3i + 4b', '4i'),    'inf',  {'a', 'b', 'i'}     ),
            (('a + i', 'b - i'),            'inf',  {'a', 'i', 'b'}     ),
            (('a + 0i', 'b'),               'inf',  {'a', 'i', 'b'}     ),
            (('a + i - i', 'b'),            'inf',  {'a', 'i', 'b'}     ),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0], length=info[1])
            self.assertEqual(seq.get_variables(), info[2])

            # omit ntuple index
            self.assertEqual(
                seq.get_variables(global_only=True),
                info[2] - {'i'})

        test_data = [
            (('a + 0i', 'b'),       '0c',   {'a', 'b'}      ),
            (('a + 0i', 'b + 0i'),  '3c',   {'a', 'b', 'c'} ),
            (('0a + 0i', 'b + 0i'), '2a',   {'a', 'b'}      ),
            (('a + 0i', '0b'),      '0a',   {'a'}           ),
        ]

        # omit zeros
        for info in test_data:
            seq = NTermRecursionSequence(*info[0], length=info[1])
            self.assertEqual(
                seq.get_variables(omit_zeros=True),
                info[2])

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
            seq = NTermRecursionSequence(*n*[1], length=length)

            for no_f in range(n):
                for no_last_f in range(n):

                    expected = LinearRelation(info[2][no_f][no_last_f])
                    actual = seq.get_ntuple_index_inequality(
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
            seq = NTermRecursionSequence(*n*[1], length=length)

            for no_f in range(n):
                no_last_f = (length - 1) % n
                expected = LinearRelation(info[2][no_f])
                actual = seq.get_ntuple_index_inequality(
                    no_formula=no_f,
                    no_last_formula=no_last_f
                )
                self.assertTrue(expected.equivalent(actual))

    def test_get_length_mod_n(self):

        test_data = [
            (3, 3, 0),
            (3, '6k + 2', 2),
            (5, '5k + 3', 3),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0]*[1], length=info[1])
            self.assertEqual(seq.get_length_mod_n(), info[2])

        test_data = [
            (3, '2l'),
            (3, '7k + 2'),
            (5, '4k + 3'),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0]*[1], length=info[1])
            self.assertRaises(ValueError, seq.get_length_mod_n)

    def test_get_ntuple_index_bound(self):

        test_data = [
            # n     bounds
            #   length
            (3, 3,  (0, 0, 0)),
            (3, 4,  (1, 0, 0)),
            (3, 5,  (1, 1, 0)),
            (3, 6,  (1, 1, 1)),
            (3, 7,  (2, 1, 1)),
            (4, 4,  (0, 0, 0, 0)),
            (4, 6,  (1, 1, 0, 0)),
            (4, 9,  (2, 1, 1, 1)),
            (5, 12, (2, 2, 1, 1, 1)),
        ]

        for info in test_data:
            n = info[0]
            length = info[1]
            seq = NTermRecursionSequence(*n*[1], length=length)

            for no_f in range(n):
                expected = LinearFormula(info[2][no_f])
                actual = seq.get_ntuple_index_bound(no_formula=no_f)
                self.assertEqual(expected, actual)

    def test_get_edge(self):

        test_data = [
            ((1, 1, 1), [2, 2, 2]),

            (('i', 'i+1', 'i+2'), ['2i+1', '2i+3', '2i+3']),

            (('i-1', 'i-2'), ['2i-3', '2i-2']),
        ]

        for info in test_data:

            # test with default ntuple index
            seq = NTermRecursionSequence(*info[0])
            ctrl_seq = NTermRecursionSequence(*info[0])

            for i in range(seq.n):
                self.assertEqual(
                    seq.get_edge(i).zip(),
                    LinearFormula(info[1][i])
                )

            self.assertEqual(seq, ctrl_seq)

    #-------------------------------------------------------------------------
