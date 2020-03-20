from numbering_patterns.source.linear_formula import LinearFormula
from numbering_patterns.source import misc


class LinearEquation():
    """A class to represent an equation of two linear formulas"""

    #-INIT--------------------------------------------------------------------

    def __init__(self, *args):

        # init with another equation
        if len(args) == 1 and type(args[0]) == LinearEquation:
            LinearEquation.__init__(self, args[0].left, args[0].right)

        # init with string
        elif len(args) == 1 and type(args[0]) == str:
            self.read_from_string(args[0])

        # init with formulas
        elif len(args) == 2:
            self.left = LinearFormula(args[0])
            self.right = LinearFormula(args[1])

        else:
            raise TypeError('the constructor takes at most 2 arguments')

    #-------------------------------------------------------------------------


    #-STRING-TO-EQUATION-CONVERSION-------------------------------------------

    def read_from_string(self, string):
        """Converts a string into an equation"""

        if type(string) != str:
            raise TypeError('the argument is not a string')

        formulas = string.split('==')
        if len(formulas) > 2:
            raise ValueError('the string describes multiple equations')

        elif len(formulas) == 1:
            formulas = string.split('=')
            if len(formulas) > 2:
                raise ValueError('the string describes multiple equations')

            elif len(formulas) == 1:
                raise ValueError('the string does not describe an equation')

        self.left = LinearFormula(formulas[0])
        self.right = LinearFormula(formulas[1])

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def __str__(self):
        return f'{str(self.left)} == {str(self.right)}'

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __neg__(self):
        return LinearEquation(-self.left, -self.right)

    def __iadd__(self, other):
        if type(other) == LinearEquation:
            self.left += other.left
            self.right += other.right

        else:
            self.left += other
            self.right += other

        return self

    def __isub__(self, other):
        if type(other) == LinearEquation:
            self.left -= other.left
            self.right -= other.right

        else:
            self.left -= other
            self.right -= other

        return self

    def __imul__(self, other):
        self.left *= other
        self.right *= other
        return self

    def __itruediv__(self, other):
        self.left /= other
        self.right /= other
        return self

    def __imod__(self, other):
        self.left %= other
        self.right %= other
        return self

    @misc.assignment_to_binary('+=')
    def __add__(self, other):
        pass

    @misc.assignment_to_binary('-=')
    def __sub__(self, other):
        pass

    @misc.assignment_to_binary('*=')
    def __mul__(self, other):
        pass

    @misc.assignment_to_binary('/=')
    def __truediv__(self, other):
        pass

    @misc.assignment_to_binary('%=')
    def __mod__(self, other):
        pass

    #-------------------------------------------------------------------------


    #-MODIFICATION------------------------------------------------------------

    @misc.inplace(default=False)
    def substitute(self, recursive=False, **kwargs):
        """Substitutes given variables for given formulas"""

        self.left.substitute(**kwargs, recursive=recursive, inplace=True)
        self.right.substitute(**kwargs, recursive=recursive, inplace=True)

    @misc.inplace(default=False)
    def zip(self):
        """Reduces the left and right sides of the equation to the simplest
        form"""

        self.left.zip(inplace=True)
        self.right.zip(inplace=True)

    @misc.inplace(default=False)
    def modulo(self, n):
        """Reduces the left and right sides of the equation to their simplest
        modulo <n> equivalent"""

        self.left.modulo(n, inplace=True)
        self.right.modulo(n, inplace=True)

    @misc.inplace(default=False)
    def reverse(self):
        """Switches the sides of the equation"""

        temp = self.left.copy()
        self.left = self.right.copy()
        self.right = temp

    @misc.inplace(default=False)
    def solve(self):
        """Reduces the equation to the simplest equation in the form
        'L == 0'"""

        self.left -= self.right
        self.right = LinearFormula(0)
        self.left.zip(inplace=True)

        # TODO: find common divider

    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    def copy(self):
        """Returns a copy of the equation"""

        return LinearEquation(self.left, self.right)

    def evaluate(self, **kwargs):
        """Evaluates the sides of the equation, given the variable values"""

        result = self.copy()
        result.left = LinearFormula(result.left.evaluate(**kwargs))
        result.right = LinearFormula(result.right.evaluate(**kwargs))
        return result

    def get_variables(self, omit_zeros=False):
        """Returns a set of variables used in the equation"""

        result = self.left.get_variables(omit_zeros=omit_zeros)
        result |= self.right.get_variables(omit_zeros=omit_zeros)

        return result

    # TODO:
    def status(self, **kwargs):
        """Returns the logical status of the equation
        (true, false or unknown)"""

        solved_eq = self.solve()
        if solved_eq.get_variables() != set():
            return 'unknown'

        should_be_zero = solved_eq.left.evaluate()
        if should_be_zero != 0:
            return 'false'

        elif should_be_zero == 0:
            return 'true'

    # -------------------------------------------------------------------------

