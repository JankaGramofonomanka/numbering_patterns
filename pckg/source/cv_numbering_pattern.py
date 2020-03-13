from pckg.source.linear_formula import LinearFormula
from pckg.source.ntr_sequence import NTermRecursionSequence
from pckg.source import misc

class CentralVertexNumberingPattern():
    """A class to represent a numbering pattern of a cycle determined by a
    central vertex number, left-hand and right-hand sequences"""
    # for example if the central number is c,
    # the left-hand sequence is l_n (n = 1, 2, 3, ...)
    # the right-hand sequence is r_n (n = 1, 2, 3, ...)
    # then the pattern will be:
    # ..., l_3,   l_2,   l_1,   c,   r_1,   r_2,   r_3, ...
    # ..., v_n-3, v_n-2, v_n-1, v_0, v_1,   v_2,   v_3, ...
    # where the cycle is v_0, v_1, v_2, ..., v_n-2, v_n-1, v_0,
    # and v_0 is chosen to be the central vertex
    
    def __init__(self, central_number, left_seq, right_seq, 
        l_len='inf', r_len='inf'):

        self.center = LinearFormula(central_number)
        
        self.left_seq = NTermRecursionSequence(left_seq)
        self.right_seq = NTermRecursionSequence(right_seq)

        self.left_len = LinearFormula(l_len)
        self.right_len = LinearFormula(r_len)

    def __str__(self):

        string = ''

        string += f'center: {self.center}, '
        string += f'left: {self.left_seq.formulas_str()}, '
        string += f'right: {self.right_seq.formulas_str()}'

        string = f'CVNP({string})'

        return string

    def __eq__(self, other):
        return (self.center == other.center
            and self.left_seq == other.left_seq
            and self.right_seq == other.right_seq
            and self.left_len == other.left_len
            and self.right_len == other.right_len)

    def evaluate(self, index):
        """Returns: the <index>-th right number if <index> > 0,
                    the <-index>-th left number if <index> < 0
                    the central vertex number   if <index> == 0"""

        if index == 0:
            return self.center
        elif index > 0:
            return self.right_seq.evaluate(index - 1)
        elif index < 0:
            return self.left_seq.evaluate(-index - 1)

    def print(self, l_len='default', r_len='default'):
        """prints the pattern from the <l_len>-th left number to the
        <r_len>-th right number"""

        if l_len == 'default':
            try:
                l_len = self.left_len.evaluate()
            except  TypeError:
                raise TypeError('left sequence length is not a number')

        if r_len == 'default':
            try:
                r_len = self.right_len.evaluate()
            except TypeError:
                raise TypeError('right sequence length is not a number')

        string = ''

        for i in range(-l_len, r_len):
            string += f'{self.evaluate(i)}, '

        string += f'{self.evaluate(r_len)}'

        string = f'({string})'

        print(string)

    def get_variables(self, omit_zeros=False):
        """Returns a set of variables used in any of the formulas that
        determine the pattern"""

        result = self.center.get_variables(omit_zeros=omit_zeros)
        result |= self.left_seq.get_variables(omit_zeros=omit_zeros)
        result |= self.right_seq.get_variables(omit_zeros=omit_zeros)
        if self.left_len != LinearFormula('inf'):
            result |= self.left_len.get_variables(omit_zeros=omit_zeros)
        if self.right_len != LinearFormula('inf'):
            result |= self.right_len.get_variables(omit_zeros=omit_zeros)

        return result

    def copy(self):
        """Returns a copy of <self>"""
        return CentralVertexNumberingPattern(self.center, self.left_seq,
            self.right_seq, self.left_len, self.right_len)

    @misc.inplace(default=False)
    def zip(self):
        """Simplifies the formulas determining the pattern"""

        self.center.zip(inplace=True)
        self.left_seq.zip(inplace=True)
        self.right_seq.zip(inplace=True)
        self.left_len.zip(inplace=True)
        self.right_len.zip(inplace=True)

    @misc.inplace(default=False)
    def substitute(self, **kwargs):
        """Substitutes given variables for given formulas in all formulas
        determining the pattern"""

        self.center.substitute(**kwargs, inplace=True)
        self.left_seq.substitute(**kwargs, inplace=True)
        self.right_seq.substitute(**kwargs, inplace=True)
        self.left_len.substitute(**kwargs, inplace=True)
        self.right_len.substitute(**kwargs, inplace=True)

    @misc.inplace(default=False)
    def reverse(self):
        """Switches the left and right-hand sequences"""

        temp_seq = self.left_seq.copy()
        self.left_seq = self.right_seq.copy()
        self.right_seq = temp_seq

        temp_len = self.left_len.copy()
        self.left_len = self.right_len.copy()
        self.right_len = temp_len