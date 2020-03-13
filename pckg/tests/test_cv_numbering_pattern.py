import unittest
from pckg.source.cv_numbering_pattern import CentralVertexNumberingPattern
from pckg.source.ntr_sequence import NTermRecursionSequence
from pckg.source.linear_formula import LinearFormula

class TestCVNP(unittest.TestCase):

    def test_init(self):

        test_data = [
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
            (4,     ('i', '2i'),    ('2i', 'i'),    3,      3       ),
            ('2n',  ('i', '2i'),    ('2i', 'i'),    '2k',   '2k + 1'),
            (4,     ('i', '2i'),    ('2i', 'i') ),
        ]

        for args in test_data:
            pattern_1 = CentralVertexNumberingPattern(*args)
            pattern_2 = CentralVertexNumberingPattern(*args)

            self.assertEqual(pattern_1, pattern_2)

        test_data = [
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
            seq = CentralVertexNumberingPattern(*info[0])
            for index, value in info[1:]:
                result = seq.evaluate(index)
                expected_result = LinearFormula(value).zip()
                self.assertEqual(result, expected_result)