from numbering_patterns.source.linear_formula import LinearFormula

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

        string = f'Case({string})'



