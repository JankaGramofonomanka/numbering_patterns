from pckg.source.linear_formula import LinearFormula
from pckg.source import misc


class NTermRecursionSequence():
    """A class to represent an n-term-recursion sequence"""
    # for example a 3-term-recursion sequence given by formulas
    # f1(i), f2(i), f3(i) looks like this:
    # f1(0), f2(0), f3(0), f1(1), f2(1), f3(1), f1(2), f2(2), f3(2), ...


    #-INIT--------------------------------------------------------------------

    def __init__(self, *args, ntuple_index=None):
        """Initializes the sequence"""
        # args should consist of another instance of <NTermRecursionSequence>
        # or of formulas (values convertible to <LinearFormula>) determining
        # the sequence.
        # The argument <ntuple_index> represents the number of the n-tuple in
        # which the actual index is in ("<ntuple_index> == index // n" or
        # "<ntuple_index> == the variable i from class description").
        # Other variables are considered global.

        # init with <NTermRecursionSequence>
        if len(args) == 1 and type(args[0]) == NTermRecursionSequence:
            if ntuple_index is None:
                ntuple_index = args[0].ntuple_index

            NTermRecursionSequence.__init__(
                self, *args[0].formulas, ntuple_index=ntuple_index)

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

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def __str__(self):
        return f'{self.n}-TRSeq(' + self.formulas_str() + ')'

    def __eq__(self, other):
        return (self.n == other.n
            and self.formulas == other.formulas
            and self.ntuple_index == other.ntuple_index)

    #-------------------------------------------------------------------------


    #-MODIFIERS---------------------------------------------------------------

    @misc.inplace(default=False)
    def zip(self):
        """Reduces all the formulas to the simplest form"""
        for i in range(self.n):
            self.formulas[i].zip(inplace=True)

    @misc.inplace(default=False)
    def substitute(self, **kwargs):
        """Substitutes given variables for given formulas in all formulas"""
        for i in range(self.n):
            self.formulas[i].substitute(**kwargs, inplace=True)

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

    def formulas_str(self):
        """Returns a string with formulas that determine the sequence"""
        # for example if the formulas are 'i', '4i', '3i + 4n' then the
        # string will be "'i', '4i', '3i + 4n'"

        string = ''

        for formula in self.formulas[0:-1]:
            string += f'{str(formula)}, '

        string += str(self.formulas[-1])

        return string

    def evaluate(self, index):
        """Returns <index>-th formula of the sequence, in the simplest form"""

        r = index % self.n
        i = index // self.n
        return self.formulas[r].substitute(**{self.ntuple_index: i}).zip()

    def get_variables(self, omit_zeros=False, global_only=False):
        """Returns a set of variables used by the sequence"""
        # if <global_only> is True, the method will return a set of global
        # variables used by the sequence's formulas,
        # otherwise, if any of the formulas uses the <self.ntuple_index>
        # variable, the returned set will include it

        result = set({})
        for formula in self.formulas:
            result |= formula.get_variables(omit_zeros=omit_zeros)

        if global_only == True:
            result -= {self.ntuple_index}

        return result

    #-------------------------------------------------------------------------

