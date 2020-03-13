from pckg.source.linear_formula import LinearFormula
from pckg.source import misc


class NTermRecursionSequence():
    """A class to represent an n-term-recursion sequence"""
    # for example a 3-term-recursion sequence given by formulas
    # f1(i), f2(i), f3(i) looks like this:
    # f1(0), f2(0), f3(0), f1(1), f2(1), f3(1), f1(2), f2(2), f3(2), ...

    def __init__(self, *args):
        """Initializes the formula"""
        # args should consist of another instance of <NTermRecursionSequence>
        # or of formulas (values convertible to <LinearFormula>) determining
        # the sequence.
        # The variable 'i' is assumed to correspond to the place in the
        # sequence ('i' == 'index' // n, where 'index' is the actual place in
        # the sequence) (the variable i from class description)
        # Other variables are considered global.

        if len(args) == 1 and type(args[0]) == NTermRecursionSequence:
            self.n = args[0].n
            self.formulas = args[0].formulas.copy()

        elif len(args) == 1 and type(args[0]) in {tuple, list}:
            NTermRecursionSequence.__init__(self, *args[0])

        else:
            self.n = len(args)

            # convert args to formulas
            self.formulas = []
            for formula in args:
                self.formulas.append(LinearFormula(formula))

    def __str__(self):
        return f'{self.n}-TRSeq(' + self.formulas_str() + ')'

    def __eq__(self, other):
        return self.n == other.n and self.formulas == other.formulas

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

        mod_n = index % self.n
        i = index // self.n
        return self.formulas[mod_n].substitute(i=i).zip()

    def print(self, length):
        """Prints the first <length> elements of the sequence"""

        string = ''
        for i in range(length - 1):
            string += f'{str(self.evaluate(i))}, '

        string += str(self.evaluate(length - 1))

        string = f'({string})'
        print(string)

    def get_variables(self, omit_zeros=False):
        """Returns a set of variables used by any of the formulas"""

        result = set({})
        for formula in self.formulas:
            result |= formula.get_variables(omit_zeros=omit_zeros)

        return result

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

    def copy(self):
        """Returns a copy of the sequence"""
        return NTermRecursionSequence(self)

