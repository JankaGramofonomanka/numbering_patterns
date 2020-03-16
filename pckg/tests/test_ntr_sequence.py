import unittest
from pckg.source.ntr_sequence import NTermRecursionSequence
from pckg.source.linear_formula import LinearFormula

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

            seq = NTermRecursionSequence(*args, ntuple_index='xxx')
            self.assertEqual(seq.ntuple_index, 'xxx')

            # init with formulas
            new_args = []
            for i in range(n):
                new_args.append(LinearFormula(args[i]))

            seq = NTermRecursionSequence(*new_args)
            self.assertEqual(seq.n, n)
            for i in range(n):
                self.assertEqual(new_args[i], seq.formulas[i])

            # init with another sequence
            seq = NTermRecursionSequence(*args, ntuple_index='yyy')
            new_seq = NTermRecursionSequence(seq)
            self.assertEqual(seq.n, n)
            for i in range(n):
                self.assertEqual(seq.formulas[i], new_seq.formulas[i])
            self.assertEqual(new_seq.ntuple_index, 'yyy')

            new_seq = NTermRecursionSequence(seq, ntuple_index='xxx')
            self.assertEqual(new_seq.ntuple_index, 'xxx')

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def test_str(self):

        test_data = [
            # init args                     string
            (('a + b', '3i + 4', '4i'),     '3-TRSeq(a + b, 3i + 4, 4i)'),
            (('i',),                        '1-TRSeq(i)'                ),
            (('1', 'a'),                    '2-TRSeq(1, a)'             ),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0])
            self.assertEqual(str(seq), info[1])

    def test_eq(self):

        test_data = [
            (('a + b', '3i + 4', '4i'), 'i'),
            (('a + b',), 'j'),
        ]

        for info in test_data:
            seq_1 = NTermRecursionSequence(*info[0], ntuple_index=info[1])
            seq_2 = NTermRecursionSequence(*info[0], ntuple_index=info[1])
            self.assertEqual(seq_1, seq_2)

        test_data = [
            (('a + b', '3i + 4', '4i'), 'i',
             ('b + a', '3i + 4', '4i'), 'i'),

            (('a + b',),                'i',
             ('4i', '5i'),              'i'),

            (('a + b', '4i', '5i'),     'i',
             ('4i', '5i', 'a + b'),     'i'),

            (('2i', '2i', '2i'),        'i',
             ('2i', '2i'),              'i'),

            (('a + b', '3i + 4', '4i'), 'i',
             ('a + b', '3i + 4', '4i'), 'j'),

            (('i', 'i', 'i'),           'i',
             ('i', 'i', 'i'),           'j'),

            (('i', 'i', 'i'),           'a',
             ('i', 'i', 'i'),           'b'),
        ]

        for info in test_data:
            seq_1 = NTermRecursionSequence(*info[0], ntuple_index=info[1])
            seq_2 = NTermRecursionSequence(*info[2], ntuple_index=info[3])
            self.assertNotEqual(seq_1, seq_2)

    #-------------------------------------------------------------------------


    #-MODIFIERS---------------------------------------------------------------

    def test_zip(self):

        test_data = [
            # init args
            ('a + b + a', '3i + 4i', '4i'),
            ('i - i', 'i'),
            ('i + i',),
            ('1 + 1', 'a'),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info).zip()
            for i in range(len(info)):
                zipped_formula = LinearFormula(info[i]).zip()
                self.assertEqual((seq.formulas[i]), zipped_formula)

    def test_substitute(self):

        test_data = [
            # init args                     {variable: substitute}
            (('a + b', '3i + 4', '4i'),     {'a': 'x + 2'}              ),
            (('a + b', '3i + 4', '4i'),     {'i': 'i + 1'}              ),
            (('i', 'i'),                    {'i': '2i'}                 ),
            (('a + 2', 'a'),                {'a': '3b'}                 ),
            (('a + b', '3i + 4', '4i'),     {'a': 'x + 2', 'i': '2i'}   ),
            (('a + i', 'b - i'),            {'a': 'x + 2', 'b': '2i'}   ),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0])
            ntuple_index = seq.ntuple_index

            seq.substitute(**info[1], inplace=True)

            for i in range(len(info[0])):
                formula = LinearFormula(info[0][i]).substitute(**info[1])
                self.assertEqual(seq.formulas[i], formula)

            self.assertEqual(seq.ntuple_index, ntuple_index)

    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    def test_copy(self):
        seq = NTermRecursionSequence('a + i', '3i', 'i + 3', ntuple_index='j')
        copy_of_seq = seq.copy()
        self.assertEqual(seq, copy_of_seq)

        copy_of_seq.formulas[0] = LinearFormula('-4i + a')
        self.assertNotEqual(seq, copy_of_seq)

    def test_formulas_str(self):

        test_data = [
            # init args                     string
            (('a + b', '3i + 4', '4i'),     'a + b, 3i + 4, 4i' ),
            (('i',),                        'i'                 ),
            (('1', 'a'),                    '1, a'              ),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0])
            self.assertEqual(seq.formulas_str(), info[1])

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
            (('a + b', '3i + 4', '4i'),     {'a', 'b', 'i'} ),
            (('a + b + 3a', 'i'),           {'a', 'b', 'i'} ),
            (('a + b', 'a + 2b'),           {'a', 'b'}      ),
            (('a', 'aa'),                   {'a', 'aa'}     ),
            (('i', 'i'),                    {'i'}           ),
            (('a + 2', 'a' ),               {'a'}           ),
            (('a + 2', 'a + i'),            {'a', 'i'}      ),
            (('a + b', '3i + 4b', '4i'),    {'a', 'b', 'i'} ),
            (('a + i', 'b - i'),            {'a', 'i', 'b'} ),
            (('a + 0i', 'b'),               {'a', 'i', 'b'} ),
            (('a + i - i', 'b'),            {'a', 'i', 'b'} ),
        ]

        for info in test_data:
            seq = NTermRecursionSequence(*info[0])
            self.assertEqual(seq.get_variables(), info[1])

            # omit ntuple index
            self.assertEqual(
                seq.get_variables(global_only=True),
                info[1] - {'i'})

        test_data = [
            (('a + 0i', 'b'),       {'a', 'b'}  ),
            (('a + 0i', 'b + 0i'),  {'a', 'b'}  ),
            (('a + 0i', '0b'),      {'a'}       ),
        ]

        # omit zeros
        for info in test_data:
            seq = NTermRecursionSequence(*info[0])
            self.assertEqual(
                seq.get_variables(omit_zeros=True),
                info[1])

    #-------------------------------------------------------------------------
