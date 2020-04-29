from . import misc


class LinearFormula():
    """A class to represent a linear formula (a first degree polynomial)"""


    #-INIT--------------------------------------------------------------------

    def __init__(self, *args):
        """Initializes the formula"""
        
        self.multipliers = []
        self.variables = []
        # for example if the formula is 'a + 4b - 3c' then we should get
        #         <self.multipliers> == [1,   4,   -3 ]
        #           <self.variables> == ['a', 'b', 'c']

        if len(args) == 1:
            arg = args[0]

            # init with <LinearFormula>
            if type(arg) == LinearFormula:
                self.multipliers = arg.multipliers.copy()
                self.variables = arg.variables.copy()

            # init with string
            elif type(arg) == str:
                self.read_from_string(arg)

            # init with dict
            elif type(arg) == dict:
                for variable, multiplier in arg.items():
                    self.variables.append(variable)
                    self.multipliers.append(int(multiplier))

            # init with something convertible to an integer
            else:
                try:
                    self.multipliers.append(int(arg))
                    self.variables.append('')
                except ValueError:
                    raise ValueError(f'invalid argument: {arg}')
                except TypeError:
                    raise TypeError(f'invalid argument: {arg}')

        # init with lists
        elif len(args) == 2 and type(args[0]) == type(args[1]) == list:
            if len(args[0]) != len(args[1]):
                raise ValueError("""lists of multipliers and variables must 
                    have the same length""")
            else:
                self.multipliers = args[0].copy()
                self.variables = args[1].copy()
        
        elif len(args) == 2:
            raise TypeError('arguments have to be lists')

        else:
            raise TypeError('the constructor takes at most 2 arguments')

    #-------------------------------------------------------------------------


    #-STRING-TO-FORMULA-CONVERSION--------------------------------------------

    def read_from_string(self, string):
        """Converts a string into a formula"""
        # I assume that <string> is made of substrings like this:
        # operator, multiplier, variable, operator, multiplier, variable, ...
        # where some of the substrings can be empty
        
        # the algorithm in essence works like this:
        # 1. read operator
        # 2. read multiplier
        # 3. read variable
        # 4. add segment
        # 5. go back to point 1. if the string hasn't ended

        # set up temporary data
        self._setup_read_from_string()

        for char in string:
            self._process(char)

        # this will add the last segment
        self._process(' ')

        self._tear_down_read_from_string()

    def _setup_read_from_string(self):
        """Sets up memory for the <read_from_string> function"""
        self._current_operation = None
        self._current_multiplier = None
        self._current_variable = None
        self._phase = 'operation'

    def _tear_down_read_from_string(self):
        """Deletes memory used by the <read_from_string> function"""
        del self._current_operation
        del self._current_multiplier
        del self._current_variable
        del self._phase

    def _process(self, char):
        """Choses the processing algorithm based on which phase the main
        algorithm is in"""

        if self._phase == 'operation':
            self._process_operation(char)
        elif self._phase == 'multiplier':
            self._process_multiplier(char)
        elif self._phase == 'variable':
            self._process_variable(char)

    # the 3 methods below:
    # <_process_operation>, <_process_multiplier>, <_process_variable> 
    # work like this:
    # if <char> is "supported":
    #     do stuff
    # else:
    #     clean up
    #     go to the next phase 
    #     pass <char> to the next _process_whatever method

    def _process_operation(self, char):
        """Processes <char> given that <char> is part of an operation
        (+ or -)"""
            
        if char == ' ':
            # in the middle of a string a space does not tell us anything
            # also this prevents from going in circles when a space occurs 
            # after a variable name
            pass

        elif LinearFormula._type_of_char(char) == 'operator':
            if char == '+':
                self._current_operation = '+'
            elif char == '-':
                self._current_operation = '-'
            else:
                raise ValueError(f'invalid operation - {char}')

        else:
            # clean up
            if self._current_operation is None:
                self._current_operation = '+'
            
            # next phase
            self._phase = 'multiplier'
            self._process_multiplier(char)

    def _process_multiplier(self, char):
        """Processes <char> given that <char> is part of a number"""

        if LinearFormula._type_of_char(char) == 'number':
            if self._current_multiplier is None:
                self._current_multiplier = int(char)
            else:
                self._current_multiplier *= 10
                self._current_multiplier += int(char)

        else:
            # clean up
            if self._current_multiplier is None:
                self._current_multiplier = 1

            if self._current_operation == '-':
                self._current_multiplier *= -1

            # next phase
            self._phase = 'variable'
            self._process_variable(char)

    def _process_variable(self, char):
        """Processes <char> given that <char> is part of a variable name"""
    
        if LinearFormula._type_of_char(char) in {'char', 'number'}:
            # the first character of the variable name has to pass through
            # the <self._process_number> method so it won't be a number

            if self._current_variable is None:
                self._current_variable = char
            else:
                self._current_variable += char

        else:
            # clean up
            if self._current_variable is None:
                self._current_variable = ''

            # add segment (part of clean up)
            self.multipliers.append(self._current_multiplier)
            self.variables.append(self._current_variable)

            # reset temporary data and go to the next phase
            self._setup_read_from_string()
            self._process_operation(char)

    @classmethod
    def _type_of_char(cls, char):
        """Tells whether <char> is a number, space, operator or a regular
        character"""
        try:
            int(char)
            return 'number'
        except ValueError:
            if char == ' ':
                return 'space'
            elif char in {'+', '-'}:
                return 'operator'
            else:
                return 'char'

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def __str__(self):

        text = ''
        for i in range(self.length()):
            
            if self.multipliers[i] >= 0:
                if i != 0:
                    # the '+' should be omitted at the beginning
                    text += ' + '

                if self.multipliers[i] != 1 or self.variables[i] == '':
                    # if the multiplier is 1 and there is a variable, there is
                    # no sense in writing the multiplier
                    text += str(self.multipliers[i])
            else:
                if i != 0:
                    text += ' - '

                else:
                    # at the beginning the '-' shouldn't have spaces around it
                    text += '-'
                if self.multipliers[i] != -1 or self.variables[i] == '':
                    # if the multiplier is -1 and there is a variable, there 
                    # is no sense in writing the multiplier

                    # the '-' was already written
                    text += str(-self.multipliers[i])

            # don't forget the variable
            text += self.variables[i]

        # the string shouldn't be empty
        if text == '':
            text = '0'

        return text

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        if self.multipliers == [] or self.multipliers == [0]:
            return other.multipliers == [] or other.multipliers == [0]

        return (
            self.multipliers == other.multipliers 
            and self.variables == other.variables
        )

    def __neg__(self):
        result = self.copy()

        for i in range(result.length()):
            result.multipliers[i] *= -1
        
        return result
    
    @misc.convert_to_type('owners type', operator=True)
    def __iadd__(self, other):
        for i in range(other.length()):
            multiplier = other.multipliers[i]
            variable = other.variables[i]
            self.add_segment(multiplier, variable, inplace=True)
        
        return self
    
    @misc.convert_to_type('owners type', operator=True)
    def __isub__(self, other):
        self += -other
        return self
    
    @misc.convert_to_type(int, operator=True)
    def __imul__(self, other):
        for i in range(self.length()):
            self.multipliers[i] *= other
        
        return self

    @misc.convert_to_type(int, operator=True)    
    def __itruediv__(self, other):
        for i in range(self.length()):
            self.multipliers[i] = int(self.multipliers[i] / other)
        
        return self
    
    @misc.convert_to_type(int, operator=True)
    def __ifloordiv__(self, other):        
        self.zip()
        for i in range(self.length()):
            self.multipliers[i] //= other
        
        return self

    @misc.convert_to_type(int, operator=True)        
    def __imod__(self, other):
        self.modulo(other, inplace=True)
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
    
    @misc.assignment_to_binary('//=')
    def __floordiv__(self, other):
        pass
    
    @misc.assignment_to_binary('%=')
    def __mod__(self, other):
        pass

    def __rmul__(self, other):
        return self * other
    
    def __len__(self):
        return len(self.multipliers)
    
    def __getitem__(self, key):
        """Returns the <key>-th segment of the formula if <key> is an integer,
        if key is a variable name, returns the multiplier corresponding to
        <key>"""
        
        if type(key) == str:
            copy_of_self = self.copy()
            copy_of_self.zip(inplace=True)
            for i in range(len(copy_of_self)):
                if copy_of_self.variables[i] == key:
                    return copy_of_self.multipliers[i]
        
            raise KeyError(f'{key}')
        
        else:
            try:
                int(key)
            except ValueError:
                raise KeyError(f'{key}')
            except TypeError:
                raise KeyError(f'invalid key type: {type(key)}')
            
            if int(key) == key:
                return self.get_segment(key)
            else:
                raise KeyError(f'{key}')

    #-------------------------------------------------------------------------


    #-MODIFICATION------------------------------------------------------------

    @misc.inplace(default=False)
    def add_segment(self, multiplier, variable):
        self.multipliers.append(multiplier)
        self.variables.append(variable)

    @misc.inplace(default=False)
    def insert_segment(self, multiplier, variable, index):
        self.multipliers.insert(index, multiplier)
        self.variables.insert(index, variable)

    @misc.inplace(default=False)
    def remove_segment(self, index):
        del self.multipliers[index]
        del self.variables[index]

    @misc.inplace(default=False)
    def substitute(self, recursive=False, **kwargs):
        """Substitutes given variables for given formulas"""
        # <kwargs> should look like this {variable: formula}

        if recursive:
            self._substitute_recursive(**kwargs)
        else:
            self._substitute_non_recursive(**kwargs)

    def _substitute_non_recursive(self, **kwargs):
        """Substitutes given variables for given formulas once"""
        # <kwargs> should look like this {variable: formula}

        # assign integers to variables
        variable_ints = {}
        for i, variable in enumerate(kwargs.keys()):
            variable_ints[variable] = i

        # replace variables with the integers assigned to them
        for j in range(len(self)):
            variable = self.variables[j]
            if variable in variable_ints.keys():
                self.variables[j] = variable_ints[variable]

        # the steps above are included to avoid issues when one of the
        # formulas uses one of the variables we want to substitute

        # substitute the integers with desired formulas
        for variable, formula in kwargs.items():
            self._substitute_one_variable(variable_ints[variable], formula)

    def _substitute_recursive(self, **kwargs):
        """Substitutes given variables for given formulas recursively"""
        # that means if, for example, we want to substitute recursively
        # 'a' for 'b' and 'b' for 'c' in the formula 'a', we will get 'c'
        # instead of 'b'

        while set(kwargs) & self.get_variables() != set():
            for variable, formula in kwargs.items():

                # this will avoid issues when <formula> contains <variable>
                for i in range(len(self)):
                    if self.variables[i] == variable:
                        self.variables[i] = -1

                self._substitute_one_variable(-1, formula)

    @misc.convert_to_type('owners type', arg_index=1)
    def _substitute_one_variable(self, variable, formula):
        """Substitutes <variable> for <formula>"""
        # for example if <self> "==" 'a + b', 
        #             <variable> == 'a', 
        #             <formula> "==" 'x + 2' 
        # then the result should be 'x + 2 + b'

        # <formula> is assumed to not use <variable>

        while True:
            try:
                # find the first segment with <variable> and put it aside
                i = self.variables.index(variable)
                multiplier = self.get_segment(i)[0]
                self.remove_segment(i, inplace=True)

                # insert each segment from <formula> multiplied by
                # <multiplier> into <self>
                for j in range(formula.length()):
                    self.insert_segment(
                        multiplier*formula.multipliers[j],
                        formula.variables[j],
                        i + j,
                        inplace=True
                    )

            except ValueError:
                # break if no more segments with <variable> exist
                break

    @misc.inplace(default=False)
    def zip(self):
        """Reduces the formula to the simplest form"""

        for variable in set(self.variables):

            # find the first segment with <variable> and put it aside
            i = self.variables.index(variable)
            multiplier = self.get_segment(i)[0]
            self.remove_segment(i, inplace=True)

            while True:
                try:
                    # if more segments with <variable> exist, merge them 
                    # with the segment put aside
                    j = self.variables.index(variable)
                    multiplier += self.get_segment(j)[0]
                    self.remove_segment(j, inplace=True)

                except ValueError:
                    # if no more segments with <variable> exist, add the 
                    # merged segments to the formula
                    if multiplier != 0:
                        self.insert_segment(
                            multiplier, variable, i, 
                            inplace=True
                            )
                    break

    @misc.inplace(default=False)
    def modulo(self, n):
        """Reduces the formula to it's simplest modulo <n> equivalent"""
        
        self.zip(inplace=True)
        for i in range(self.length()):
            self.multipliers[i] %= n
        self.zip(inplace=True)

    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    def length(self):
        """Returns how many segments the formula has"""
        return len(self)

    def print(self):
        """Prints the formula"""
        print(self.__str__())

    def copy(self):
        """Returns a copy of <self>"""
        copy_of_self = LinearFormula(self.multipliers, self.variables)
        return copy_of_self

    def get_segment(self, index):
        """Returns a tuple representing <index>-th segment of the formula"""
        # for example if formula <formula> is 'a + 3b - 4c', then
        # <formula.get_segment(1)> will return (3, 'b')

        multiplier = self.multipliers[index]
        variable = self.variables[index]

        return (multiplier, variable)

    def evaluate(self, **kwargs):
        """Returns the value of the formula, given the variable values"""
        result = 0

        # no variable is represented by a '' string
        kwargs[''] = 1
        try:
            for i in range(self.length()):
                result += self.multipliers[i]*kwargs[self.variables[i]]
        except KeyError:
            raise TypeError("Not all values are provided")

        return result

    def get_variables(self, omit_zeros=False):
        """Returns a set of variables used by the formula"""

        if omit_zeros:
            return set(self.zip().variables) - {''}
        else:
            return set(self.variables) - {''}

    @misc.convert_to_type('owners type')
    def equivalent(self, other):
        """Tells the user whether <self> and <other> are euivalent or not"""

        self_zipped = self.zip()
        other_zipped = other.zip()

        # after zip() equivalent formulas should jave the same variables,
        # including the '' variable
        if set(self_zipped.variables) != set(other_zipped.variables):
            return False

        # if the formulas have different multipliers corresponding to the
        # same variable, the result is false
        for variable in self_zipped.variables:
            if self_zipped[variable] != other_zipped[variable]:
                return False

        # all multipliers are the same
        return True

    @misc.convert_to_type('owners type')
    def separate(self, formula):
        """Returns a tuple ('m', formula_2), such that
        m*<formula> + formula_2 == <self>"""

        this = self.zip()
        zipped_formula = formula.zip()

        if zipped_formula.variables in [[], ['']]:
            this -= formula
            return (1, this)

        condition = True
        multiplier = 0
        while condition:

            if zipped_formula.get_variables() - this.get_variables() != set():
                condition = False
                break

            var = zipped_formula.variables[0]
            if var == '':
                # this means there are more variables
                var = zipped_formula.variables[1]

            var_multiplier = this[var]
            if var_multiplier > 0 and multiplier >= 0:
                this -= zipped_formula
                multiplier += 1
            elif var_multiplier < 0 and var_multiplier <= 0:
                this += zipped_formula
                multiplier -= 1
            else:
                condition = False

            this.zip(inplace=True)

        return (multiplier, this)

    def get_bounds(
            self, lower_bounds={}, upper_bounds={},
            order=None, recursive=False
    ):

        if recursive == True and order is not None:
            raise ValueError(
                "The 'recursive' argument cannot be True "
                + "when 'order' is specified"
            )

        elif order is None:
            return self._get_bounds_no_order(
                lower_bounds, upper_bounds, recursive)

        else:
            return self._get_bounds_order(lower_bounds, upper_bounds, order)

    def _get_bounds_no_order(
            self, lower_bounds={}, upper_bounds={}, recursive=False):
        """Returns a tuple (l_bound, u_bound) such that
        l_bound <= <self> <= u_bound, given the bounds of the variables"""

        if type(upper_bounds) != dict or type(lower_bounds) != dict:
            raise TypeError('arguments are should be dictionaries')

        lower_kwargs = {}
        upper_kwargs = {}

        # zip to avoid redundant zips
        zipped = self.zip()

        # we will use the <substitute> method to get the lower and upper
        # bounds, therefore we need to chose which given bound goes where

        # for example if the formula is 'a + b' and the upper bound of 'b' is
        # 5, then we will get the upper bound of the formula by substituting
        # 'b' for 5, but if the formula is 'a - b', then the aforementioned
        # operation will give us the lower bound
        zipped._prepare_kwargs_for_get_bounds(
            lower_kwargs, lower_bounds, 'lower', 'lower')
        zipped._prepare_kwargs_for_get_bounds(
            lower_kwargs, upper_bounds, 'lower', 'upper')
        zipped._prepare_kwargs_for_get_bounds(
            upper_kwargs, lower_bounds, 'upper', 'lower')
        zipped._prepare_kwargs_for_get_bounds(
            upper_kwargs, upper_bounds, 'upper', 'upper')

        lower_bound = self.substitute(**lower_kwargs).zip()
        upper_bound = self.substitute(**upper_kwargs).zip()

        if recursive == True:
            calculate_lower = True
            calculate_upper = True

            while calculate_lower or calculate_upper:
                if calculate_lower:
                    lower_kwargs = {}

                    # zip to avoid redundant zips
                    lower_bound.zip(inplace=True)

                    # choose the variable bounds
                    lower_bound._prepare_kwargs_for_get_bounds(
                        lower_kwargs, lower_bounds, 'lower', 'lower')
                    lower_bound._prepare_kwargs_for_get_bounds(
                        lower_kwargs, upper_bounds, 'lower', 'upper')

                    if lower_kwargs == {}:
                        # there are no more bounds to use
                        calculate_lower = False

                    lower_bound.substitute(**lower_kwargs, inplace=True)
                    lower_bound.zip(inplace=True)

                if calculate_upper:
                    upper_kwargs = {}

                    # zip to avoid redundant zips
                    upper_bound.zip(inplace=True)

                    # choose the variable bounds
                    upper_bound._prepare_kwargs_for_get_bounds(
                        upper_kwargs, lower_bounds, 'upper', 'lower')
                    upper_bound._prepare_kwargs_for_get_bounds(
                        upper_kwargs, upper_bounds, 'upper', 'upper')

                    if upper_kwargs == {}:
                        # there are no more bounds to use
                        calculate_upper = False

                    upper_bound.substitute(**upper_kwargs, inplace=True)
                    upper_bound.zip(inplace=True)

        return (lower_bound, upper_bound)

    def _prepare_kwargs_for_get_bounds(
            self, kwargs, bounds, result_type, arg_type):
        """Modifies <kwargs> to pass to the <substitute> method,
        in the <get_bounds> method"""
        # <result_type> - type of the dict that's being modified - <kwargs>,
        # should be 'lower' or 'upper'

        # <arg_type> - type of the dict passed to <get_bounds> - <bounds>,
        # should be 'lower' or 'upper'

        for var, bound in bounds.items():
            try:
                mul = self[var]
            except KeyError:
                continue

            if mul >= 0 and arg_type == result_type:
                kwargs[var] = bound
            elif mul <= 0 and arg_type != result_type:
                kwargs[var] = bound

    def _get_bounds_order(self, lower_bounds, upper_bounds, order):
        """Substitutes variables for their bounds given in <lower_bounds> and
        <upper_bounds>, in order specified by <order> to return a tuple
        (l_bound, u_bound) such that l_bound <= <self> <= u_bound"""

        # <lower_bounds>, <upper_bounds> - dicts representing bounds of
        # individual variables, in a form {variable: bound}

        # <order> - a list representing the order in which to substitute the
        # variables

        upper_bound = self.zip()
        lower_bound = upper_bound.copy()

        for variable in order:

            # get the bounds of <variables>
            try:
                variable_lower_bound = lower_bounds[variable]
            except KeyError:
                variable_lower_bound = None

            try:
                variable_upper_bound = upper_bounds[variable]
            except KeyError:
                variable_upper_bound = None

            # and use them to get the bounds of <self>
            lower_bound._process_variable_bound(
                variable, 'lower',
                lower_bound=variable_lower_bound,
                upper_bound=variable_upper_bound
            )
            upper_bound._process_variable_bound(
                variable, 'upper',
                lower_bound=variable_lower_bound,
                upper_bound=variable_upper_bound
            )

        return lower_bound, upper_bound

    def _process_variable_bound(
            self, variable, output_bound_type,
            lower_bound=None, upper_bound=None
    ):
        """Modifies <self> so that <self> after the algorithm is the upper or
        lower bound of <self> before the algorithm, based on the bounds of
        <variable>"""

        # <lower_bound>, <upper_bound> - lower and upper bounds of <variable>

        # <output_bound_type> - should be "lower" or "upper" - a string that
        # specifies whether the modified <self> should be the lower or upper
        # bound of the original <self>

        try:
            multiplier = self[variable]
        except KeyError:
            return

        if output_bound_type not in ('lower', 'upper'):
            raise ValueError(
                f"invalid 'output_bound_type' argument: {output_bound_type}")

        # we will substitute one of the formulas <lower_bound>, <upper_bound>
        # for <variable> to get the desired outcome

        # for example <self> is 'a + b' and the upper bound of 'b' is 5, then
        # we will get the upper bound of the formula by substituting 'b' for
        # 5, but if the formula is 'a - b', then the aforementioned
        # operation will give us the lower bound

        if multiplier > 0:
            if output_bound_type == 'lower':
                bound = lower_bound
            elif output_bound_type == 'upper':
                bound = upper_bound

        else:
            if output_bound_type == 'lower':
                bound = upper_bound
            elif output_bound_type == 'upper':
                bound = lower_bound

        if bound is not None:
            self.substitute(**{variable: bound}, inplace=True)
            self.zip(inplace=True)

    #-------------------------------------------------------------------------


