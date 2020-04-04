from .linear_formula import LinearFormula
from .ntr_sequence import NTermRecursionSequence
from .linear_relation import LinearRelation
from . import misc


class CentralVertexNumbering():
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


    #-INIT--------------------------------------------------------------------

    def __init__(self, *args, **kwargs):
        """Initializes the pattern"""

        # init with other pattern
        if len(args) == 1:
            other_pattern = args[0]
            if type(other_pattern) != CentralVertexNumbering:
                raise TypeError('the argument is not a sequence')

            # try to get data from <kwargs>
            try:
                ntuple_index = kwargs['ntuple_index']
            except KeyError:
                ntuple_index = other_pattern.ntuple_index

            try:
                left_len = kwargs['left_len']
            except KeyError:
                left_len = other_pattern.left_seq.length

            try:
                right_len = kwargs['right_len']
            except KeyError:
                right_len = other_pattern.right_seq.length

            # initialize
            CentralVertexNumbering.__init__(
                self,
                other_pattern.center,
                other_pattern.left_seq,
                other_pattern.right_seq,
                ntuple_index=ntuple_index,
                left_len=left_len,
                right_len=right_len,
            )

        # init with formulas and sequences
        elif len(args) == 3:
            center = args[0]
            left_seq = args[1]
            right_seq = args[2]

            # central vertex number
            self.center = LinearFormula(center)

            # left-hand sequence
            if type(left_seq) in {tuple, list}:
                self.left_seq = NTermRecursionSequence(*left_seq)
            else:
                self.left_seq = NTermRecursionSequence(left_seq)

            # right-hand sequence
            if type(right_seq) in {tuple, list}:
                self.right_seq = NTermRecursionSequence(*right_seq)
            else:
                self.right_seq = NTermRecursionSequence(right_seq)

            # try to get data from <kwargs>

            # ntuple_index
            try:
                ntuple_index = kwargs['ntuple_index']
                if type(ntuple_index) != str:
                    raise TypeError(
                        'the ntuple_index keyword argument must be a string')

                self.ntuple_index = ntuple_index

                # set the <ntuple_index> variable in the sequences
                self.left_seq.set_ntuple_index(ntuple_index, inplace=True)
                self.right_seq.set_ntuple_index(ntuple_index, inplace=True)

            except KeyError:
                self.ntuple_index = self.left_seq.ntuple_index
                try:
                    self.right_seq.set_ntuple_index(
                        self.ntuple_index, inplace=True)
                except ValueError:
                    raise ValueError("the right sequence uses the left"
                                     + " sequence's 'ntuple_index' variable")

            if self.ntuple_index in self.center.variables:
                raise ValueError(
                    'the ntuple_index variable is used by the central number')

            # left_len
            try:
                self.left_seq.set_length(kwargs['left_len'], inplace=True)
            except KeyError:
                pass

            # left_len
            try:
                self.right_seq.set_length(kwargs['right_len'], inplace=True)
            except KeyError:
                pass

        # raise error if the arguments cannot be interpreted
        else:
            raise TypeError('cannot interpret the arguments')

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def __str__(self):

        string = ''

        string += f'center: {self.center}, '
        string += f'left: {self.left_seq.formulas_str()}, '
        string += f'right: {self.right_seq.formulas_str()}'

        string = 'CVN({ll}<-|{ls}|<-{li}|{ct}|{ri}->|{rs}|->{rl})'.format(
            ll=str(self.left_seq.length),
            rl=str(self.right_seq.length),
            li=self.left_seq.ntuple_index,
            ri=self.right_seq.ntuple_index,
            ls=self.left_seq.formulas_str(reversed=True),
            rs=self.right_seq.formulas_str(),
            ct=str(self.center)
        )

        return string

    def __eq__(self, other):
        return (
            self.center == other.center
            and self.left_seq == other.left_seq
            and self.right_seq == other.right_seq
        )

    #-------------------------------------------------------------------------


    #-MODIFIERS---------------------------------------------------------------

    @misc.inplace(default=False)
    def zip(self):
        """Simplifies the formulas determining the pattern"""

        self.center.zip(inplace=True)
        self.left_seq.zip(inplace=True)
        self.right_seq.zip(inplace=True)

    @misc.inplace(default=False)
    def substitute(self, only_sequences=False, recursive=False, **kwargs):
        """Substitutes given variables for given formulas in all formulas
        determining the pattern"""

        if not only_sequences:
            # check if the substitute formulas use one of the <ntuple_index>
            # variables
            for formula in kwargs.values():
                variables = LinearFormula(formula).get_variables()
                if self.ntuple_index in variables:
                    raise ValueError(
                        "one of the formulas uses left or right sequences'"
                        + " ntuple_index variable,"
                        + " use the keyword argument: only_sequences=True"
                    )

            self.center.substitute(
                **kwargs, recursive=recursive, inplace=True)

        self.left_seq.substitute(
            **kwargs,
            recursive=recursive,
            inplace=True,
            formulas_only=only_sequences
        )
        self.right_seq.substitute(
            **kwargs,
            recursive=recursive,
            inplace=True,
            formulas_only=only_sequences
        )

    @misc.inplace(default=False)
    def reverse(self):
        """Switches the left and right-hand sequences"""

        temp_seq = self.left_seq.copy()
        self.left_seq = self.right_seq.copy()
        self.right_seq = temp_seq

    @misc.inplace(default=False)
    def set_lengths(self, l_len, r_len):
        """Sets the lengths of the left and right sequences"""

        self.left_seq.set_length(LinearFormula(l_len), inplace=True)
        self.right_seq.set_length(LinearFormula(r_len), inplace=True)

    @misc.inplace(default=False)
    def set_ntuple_index(self, variable):
        if type(variable) != str:
            raise TypeError('the argument must be a string')

        if variable in self.center.variables:
            raise ValueError(f'the variable: {variable} is already used')

        self.left_seq.set_ntuple_index(variable, inplace=True)
        self.right_seq.set_ntuple_index(variable, inplace=True)
        self.ntuple_index = variable

    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    def print(self, l_len='default', r_len='default'):
        """prints the pattern from the <l_len>-th left number to the
        <r_len>-th right number"""

        if l_len == 'default':
            try:
                l_len = self.left_len.evaluate()
            except TypeError:
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

    def copy(self):
        """Returns a copy of <self>"""
        return CentralVertexNumbering(self)

    def evaluate(self, index):
        """Returns: the <index>-th right number if <index> > 0,
                    the <-index>-th left number if <index> < 0,
                    the central vertex number   if <index> == 0"""

        if index == 0:
            return self.center.zip()
        elif index > 0:
            return self.right_seq.evaluate(index - 1)
        elif index < 0:
            return self.left_seq.evaluate(-index - 1)

    def get_variables(self, omit_zeros=False, global_only=False):
        """Returns a set of variables used in any of the formulas that
        determine the pattern"""

        result = self.center.get_variables(omit_zeros=omit_zeros)

        result |= self.left_seq.get_variables(
            omit_zeros=omit_zeros, global_only=global_only)

        result |= self.right_seq.get_variables(
            omit_zeros=omit_zeros, global_only=global_only)

        return result

    def get_edge(self, side, key):
        """Returns a value assigned to the chosen edge of the graph based on
        the vertex numbering"""

        if type(key) not in {int, str}:
            raise TypeError(f'invalid key type: {key}')

        if side == 'left':
            seq = self.left_seq
        elif side == 'right':
            seq = self.right_seq
        else:
            raise ValueError("the side argument must be 'left' or 'right'")

        if key in range(seq.n - 1):
            return seq.formulas[key] + seq.formulas[key + 1]

        elif key == seq.n - 1:

            this_formula = seq.formulas[key]
            next_formula = seq.formulas[0].substitute(
                **{self.ntuple_index: f'{self.ntuple_index} + 1'})

            return this_formula + next_formula

        elif key == 'center':
            return self.center + seq.evaluate(0)
        else:
            raise ValueError(f'invalid key value: {key}')

    #-------------------------------------------------------------------------
