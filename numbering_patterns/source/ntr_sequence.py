from .linear_formula import LinearFormula
from .linear_relation import LinearRelation
from . import misc


class NTermRecursionSequence():
    """A class to represent an n-term-recursion sequence"""
    # for example a 3-term-recursion sequence given by formulas
    # f1(i), f2(i), f3(i) looks like this:
    # f1(0), f2(0), f3(0), f1(1), f2(1), f3(1), f1(2), f2(2), f3(2), ...


    #-INIT--------------------------------------------------------------------

    def __init__(self, *args, length=None, ntuple_index=None):
        """Initializes the sequence"""
        # <args> should consist of another instance of
        # <NTermRecursionSequence> or of formulas (values convertible to
        # <LinearFormula>) determining the sequence.

        # The argument <ntuple_index> represents the number of the n-tuple in
        # which the actual index is in ("<ntuple_index> == index // n" or
        # "<ntuple_index> == the variable i from class description").
        # Other variables are considered global.

        # init with <NTermRecursionSequence>
        if len(args) == 1 and type(args[0]) == NTermRecursionSequence:
            if ntuple_index is None:
                ntuple_index = args[0].ntuple_index

            if length is None:
                length = args[0].length

            NTermRecursionSequence.__init__(
                self, *args[0].formulas,
                length=length, ntuple_index=ntuple_index
            )

        # init with formulas
        else:
            self.n = len(args)

            # convert args to formulas
            self.formulas = []
            for formula in args:
                self.formulas.append(LinearFormula(formula))

            if ntuple_index is None:
                self.ntuple_index = 'i'
            elif type(ntuple_index) == str:
                self.ntuple_index = ntuple_index
            else:
                raise TypeError('the ntuple_index argument is not a string')

            if length is None:
                self.length = LinearFormula('inf')
            else:
                try:
                    self.length = LinearFormula(length)
                except:
                    raise TypeError(f'cannot convert {length} into a formula')

            # make sure that <self.ntuple_index> is not used by <self.length>
            if self.ntuple_index in self.length.variables:
                raise ValueError('length uses the ntuple_index variable')

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def __str__(self):
        content = '{nti}->|{formulas}|->{len}'
        content = content.format(
            nti=self.ntuple_index,
            formulas=self.formulas_str(),
            len=self.length
        )

        return f'{self.n}-TRSeq({content})'

    def __eq__(self, other):
        return (
            self.n == other.n
            and self.formulas == other.formulas
            and self.ntuple_index == other.ntuple_index
            and self.length == other.length
        )

    #-------------------------------------------------------------------------


    #-MODIFIERS---------------------------------------------------------------

    @misc.inplace(default=False)
    def zip(self):
        """Reduces all the formulas to the simplest form"""
        for i in range(self.n):
            self.formulas[i].zip(inplace=True)
        self.length.zip(inplace=True)

    @misc.inplace(default=False)
    def substitute(self, formulas_only=False, recursive=False, **kwargs):
        """Substitutes given variables for given formulas in all of the
        sequence's formulas"""
        if not formulas_only:
            # check if formulas don't use teh <self.ntuple_index> variable
            for formula in kwargs.values():
                if self.ntuple_index in LinearFormula(formula).variables:
                    raise ValueError(
                        'one of the substitute formulas uses the'
                        + ' ntuple_index variable of the sequence'
                    )

            self.length.substitute(
                **kwargs, recursive=recursive, inplace=True)

        for i in range(self.n):
            self.formulas[i].substitute(
                **kwargs, recursive=recursive, inplace=True)

    @misc.inplace(default=False)
    def set_length(self, length):
        self.length = LinearFormula(length)
        if self.ntuple_index in self.length.variables:
            raise ValueError(f'{length} is using the ntuple_index variable')

    @misc.inplace(default=False)
    def set_ntuple_index(self, variable):
        """Sets the value of <self.ntuple_index> and modifies the formulas so
        tha they use the new variable"""
        if type(variable) != str:
            raise TypeError('the argument must be a string')

        if variable in self.get_variables(global_only=True):
            raise ValueError(f'the variable: {variable} is already used')

        self.substitute(
            **{self.ntuple_index: variable},
            formulas_only=True, inplace=True
        )
        self.ntuple_index = variable

    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    def print(self, length):
        """Prints the first <length> elements of the sequence"""

        string = ''
        for i in range(length - 1):
            string += f'{str(self.evaluate(i))}, '

        string += str(self.evaluate(length - 1))

        string = f'({string})'
        print(string)

    def copy(self):
        """Returns a copy of the sequence"""
        return NTermRecursionSequence(self)

    def formulas_str(self, reversed=False):
        """Returns a string with formulas that determine the sequence"""
        # for example if the formulas are 'i', '4i', '3i + 4n' then the
        # string will be "'i', '4i', '3i + 4n'"

        string = ''

        if reversed:
            formulas = self.formulas[-1::-1]
        else:
            formulas = self.formulas[:]

        for formula in formulas[0:-1]:
            string += f'{str(formula)}, '

        string += str(formulas[-1])

        return string

    def evaluate(self, index):
        """Returns <index>-th value of the sequence, in the simplest form"""

        r = index % self.n
        i = index // self.n
        return self.formulas[r].substitute(**{self.ntuple_index: i}).zip()

    def get_variables(self, omit_zeros=False, global_only=False):
        """Returns a set of variables used by the sequence"""
        # if <global_only> is True, the method will return a set of global
        # variables used by the sequence's formulas,
        # otherwise, if any of the formulas uses the <self.ntuple_index>
        # variable, the returned set will include it

        result = set()
        if self.length != LinearFormula('inf'):
            result = self.length.get_variables(omit_zeros=omit_zeros)

        for formula in self.formulas:
            result |= formula.get_variables(omit_zeros=omit_zeros)

        if global_only == True:
            result -= {self.ntuple_index}

        return result

    def get_ntuple_index_inequality(self, no_formula, no_last_formula):
        """Returns an inequality relation between the <ntuple_index> variable
        of the <no_formula>-th formula of the sequence, and the length of the
        sequence, given that the last formula in that sequence is it's
        <no_last_formula>-th formula"""

        if not 0 <= no_formula < self.n:
            raise ValueError("the 'no_formula' and 'no_last_formula'"
                             + " arguments must be in [0, ..., n)")

        left = LinearFormula(
            [self.n, no_formula + 1],
            [self.ntuple_index, '']
        )

        if no_last_formula >= no_formula:
            right = self.length - no_last_formula + no_formula
        else:
            right = self.length - self.n - no_last_formula + no_formula

        return LinearRelation(left, right, relation='<=').zip()

    def get_length_mod_n(self):
        """Returns the value <self.length> % <self.n> if it can be
        determined"""

        result = self.length.zip() % self.n
        try:
            return result.evaluate()
        except TypeError:
            raise ValueError(
                f'the value {self.length} % {self.n} is ambiguous')

    #-------------------------------------------------------------------------

