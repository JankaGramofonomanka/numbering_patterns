from .linear_formula import LinearFormula
from .cv_numbering import CentralVertexNumbering


class Case():
    """A class that represents a case in a mathematical proof"""
    # For example if we want to prove a statement alpha(n) and we have to
    # consider cases where n = 2k and n = 2k + 1 for some natural number k,
    # then we will have two <Case> instances, one of them will hold the
    # information that n = 2k, the other one that n = 2k + 1

    def __init__(self, **kwargs):
        self.variables = {}
        for variable, formula in kwargs.items():
            self.variables[variable] = LinearFormula(formula)

    def __str__(self):
        string = ''
        for variable, formula in self.variables.items():
            string += f'{variable} = {str(formula)}, '

        string = f'Case({string[:-2]})'
        return string


class MyCase(Case):
    """A class to represent a case in the context of numbering an SSA-cycle"""
    # SSA-graph - Simply Sequentially Additive graph

    def __init__(self, n, upper_pattern, lower_pattern, **kwargs):

        Case.__init__(self, n=n, **kwargs)

        self.upper_pattern = CentralVertexNumbering(upper_pattern)
        self.lower_pattern = CentralVertexNumbering(lower_pattern)

        # make sure that the lengths of the sequences sum up to <n>
        len_1 = self.upper_pattern.left_len.copy()
        len_1 += self.upper_pattern.right_len
        len_1 += self.lower_pattern.left_len
        len_1 += self.lower_pattern.right_len
        len_1 += 2

        len_1.substitute(**self.variables, inplace=True)
        len_1.zip(inplace=True)

        len_2 = self.variables['n'].copy()
        while set(self.variables) & len_2.get_variables() != set():
            len_2.substitute(**self.variables, inplace=True)
            len_2.zip(inplace=True)

        if len_1 != len_2:
            raise ValueError('lengths of the sequences do not sum up to n')

    def __str__(self):
        string = f'My{Case.__str__(self)}'
        string += f'\nupper pattern:{str(self.upper_pattern)}'
        string += f'\nlower pattern:{str(self.lower_pattern)}'
        return string

    def substitute_recursive(self):

        self.upper_pattern.substitute(
            **self.variables, recursive=True, inplace=True)
        self.lower_pattern.substitute(
            **self.variables, recursive=True, inplace=True)





