from .linear_formula import LinearFormula
from . import misc


class LinearRelation():
    """A class to represent an equation of two linear formulas"""

    _relations = ['==', '<=', '>=', '<', '>']
    _relations_in_str = ['==', '<=', '>=', '<', '>', '=']
    _reversed_rel = {
        '==': '==',
        '<=': '>=',
        '>=': '<=',
        '<': '>',
        '>': '<'
    }

    #-INIT--------------------------------------------------------------------

    def __init__(self, *args, relation=None):

        if relation is not None and relation not in LinearRelation._relations:
            raise ValueError(f'{args[2]} is not a valid relation sign')

        if len(args) == 1:

            # init with another relation
            if type(args[0]) == LinearRelation:
                if relation is None:
                    relation = args[0].relation

                LinearRelation.__init__(
                    self, args[0].left, args[0].right, relation=relation)

            # init with string
            if type(args[0]) == str:
                self.read_from_string(args[0])
                if relation is not None:
                    self.relation = relation

        # init with formulas
        elif len(args) == 2:

            self.left = LinearFormula(args[0])
            self.right = LinearFormula(args[1])
            if relation is None:
                relation = '=='

            self.relation = relation

        else:
            raise TypeError(
                'this constructor  takes at most 2 positional arguments')

    #-------------------------------------------------------------------------


    #-STRING-TO-EQUATION-CONVERSION-------------------------------------------

    def read_from_string(self, string):
        """Converts a string into an equation"""

        if type(string) != str:
            raise TypeError('the argument is not a string')

        formulas = []
        for relation in LinearRelation._relations_in_str:
            formulas = string.split(relation)
            if len(formulas) == 2:
                if relation == '=':
                    self.relation = '=='
                else:
                    self.relation = relation

                break

        if len(formulas) != 2:
            raise ValueError(
                'the provided string cannot be converted to any relation')

        self.left = LinearFormula(formulas[0])
        self.right = LinearFormula(formulas[1])

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def __str__(self):
        return f'{str(self.left)} {self.relation} {str(self.right)}'

    def __eq__(self, other):
        return (
            self.left == other.left
            and self.right == other.right
            and self.relation == other.relation
        )

    def __neg__(self):
        return LinearRelation(
            -self.left, -self.right,
            relation=LinearRelation._reversed_rel[self.relation]
        )


    def __iadd__(self, other):
        if type(other) == LinearRelation:
            if other.relation != self.relation:
                # TODO: figure out which relation to chose
                raise ValueError(
                    "you can't add two relations of different types")

            self.left += other.left
            self.right += other.right

        else:
            self.left += other
            self.right += other

        return self

    def __isub__(self, other):
        if type(other) == LinearRelation:
            if other.relation != self.relation:
                # TODO: figure out which relation to chose
                raise ValueError(
                    "you can't subtract two relations of different types")

            if self.relation == '==':
                self.left -= other.left
                self.right -= other.right
            else:
                self.left -= other.right
                self.right -= other.left

        else:
            self.left -= other
            self.right -= other

        return self

    @misc.convert_to_type(int, operator=True)
    def __imul__(self, other):
        self.left *= other
        self.right *= other
        if other < 0:
            self.relation = LinearRelation._reversed_rel[self.relation]

        return self

    @misc.convert_to_type(int, operator=True)
    def __itruediv__(self, other):
        self.left /= other
        self.right /= other
        if other < 0:
            self.relation = LinearRelation._reversed_rel[self.relation]

        return self


    @misc.convert_to_type(int, operator=True)
    def __imod__(self, other):

        # TODO: this is not ok:
        if self.relation != '==':
            raise TypeError(
                'the % operation does not preserve inequality relations')

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

        # TODO: this is not ok:
        if self.relation != '==':
            raise TypeError(
                'the % operation does not preserve inequality relations')

        self.left.modulo(n, inplace=True)
        self.right.modulo(n, inplace=True)

    @misc.inplace(default=False)
    def reverse(self):
        """Switches the sides of the equation"""

        temp = self.left.copy()
        self.left = self.right.copy()
        self.right = temp

        self.relation = LinearRelation._reversed_rel[self.relation]

    @misc.inplace(default=False)
    def solve(self):
        """Reduces the equation to the simplest equation in the form
        'L == 0'"""

        self -= self.right
        self.zip(inplace=True)

        gcd = misc.gcd(*self.left.multipliers)
        if gcd == 0:
            gcd = 1

        self /= gcd

    @misc.inplace(default=False)
    def expose(self, variable):
        if type(variable) != str:
            raise TypeError('the variable is not a string')

        self.solve(inplace=True)
        self.reverse(inplace=True)

        try:
            multiplier = self.right[variable]
        except KeyError:
            raise ValueError(f'{variable} is not part of the relation')

        self -= LinearFormula([multiplier], [variable])
        if multiplier > 0:
            self *= -1

        self.zip(inplace=True)

    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    def copy(self):
        """Returns a copy of the equation"""

        return LinearRelation(self.left, self.right, relation=self.relation)

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

    def status(self, **kwargs):
        """Returns the logical status of the equation
        (true, false or unknown)"""

        solved_eq = self.solve()
        if solved_eq.get_variables() != set():
            return 'unknown'

        solved_left = solved_eq.left.evaluate()
        if solved_eq.relation == '==':
            status = solved_left == 0
        elif solved_eq.relation == '<=':
            status = solved_left <= 0
        elif solved_eq.relation == '>=':
            status = solved_left >= 0
        elif solved_eq.relation == '<':
            status = solved_left < 0
        elif solved_eq.relation == '>':
            status = solved_left > 0

        if status == False:
            return 'false'

        elif status == True:
            return 'true'

    @misc.convert_to_type('owners type')
    def equivalent(self, other):
        """Tells the user whether <self> is equivalent to <other>"""

        # two relations of different type cannot be equivalent
        if (other.relation not in
                {self.relation, LinearRelation._reversed_rel[self.relation]}):
            return False

        # given 2 relations, ex. 'L1 == P1' and 'L2 == P2', we want to
        # transform them to the form 'L1 - P1 == 0' and 'L2 - P2 == 0'
        # and return something like "'L1 - P1'.equivalent(L2 - P2)"
        self_solved = self.solve()
        other_solved = other.solve()

        # note that the <solve> method divides the relation by the greatest
        # common divisor of the 'L - P' formula's multipliers, so the only
        # case when 'L1 - P1' == 'a*(L2 - P2)' that we have to take into
        # account is when 'a' == -1 and the relation in question is '=='
        # (or if the 2 relations are '<=' and '>=' or '<' and '>', but then
        # we will reverse one of them)

        if self.relation == '==':
            if self_solved.left.equivalent(other_solved.left):
                return True
            elif self_solved.left.equivalent(-other_solved.left):
                # the aforementioned case when 'L1 - P1' == '-(L2 - P2)'
                return True
            else:
                return False

        else:
            if other_solved.relation != self_solved.relation:
                # relations are reversed so we need to reverse one of the
                # relations'
                other_solved *= -1

            return self_solved.left.equivalent(other_solved.left)






    #-------------------------------------------------------------------------

