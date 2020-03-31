import unittest

from .test_lf_init import TestInit
from .test_lf_magic_methods import TestMagicMethods
from .test_lf_modifiers import TestModifiers
from .test_lf_other import TestOther

from .test_ntr_sequence import TestNTRSequence
from .test_cv_numbering import TestCVN

from .test_case import TestCase, TestMyCase

from .test_linear_relation import TestLinearRelation

if __name__ == '__main__':

    unittest.main()