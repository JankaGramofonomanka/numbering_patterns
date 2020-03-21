from functools import reduce
from math import gcd as old_gcd


def inplace(**kwargs):
    try:
        kwargs['default']
    except KeyError:
        raise ValueError('default argument not specified')
    
    def decorator(func):
        def real_func(self, *args, inplace=kwargs['default'], **kwargs):
            if inplace == True:
                func(self, *args, **kwargs)
            elif inplace == False:
                copy_of_self = self.copy()
                func(copy_of_self, *args, **kwargs)
                return copy_of_self
            else:
                raise ValueError(f"invalid 'inplace' argument: {inplace}")

        return real_func

    return decorator


def assignment_to_binary(operator):
    def decorator(func):
        
        def binary_operation(a, b):
            result = a.copy()
            if operator == '+=':
                result += b
            elif operator == '-=':
                result -= b
            elif operator == '*=':
                result *= b
            elif operator == '/=':
                result /= b
            elif operator == '//=':
                result //= b
            elif operator == '%=':
                result %= b
            elif operator == '**=':
                result **= b
            else:
                raise ValueError(f'invalid operator: {operator}')

            return result
    
        return binary_operation
    return decorator


def convert_to_type(target_type, arg_index=0, operator=False):
    if operator == True:
        error_message = 'invalid operand: {}'
    else:
        error_message = 'invalid argument: {}'

    def decorator(method):

        def real_method(owner, *args):
            nonlocal target_type
            nonlocal error_message

            if target_type == 'owners type':
                target_type = type(owner)
            try:
                new_args = []
                for i in range(len(args)):
                    if i == arg_index:
                        new_arg = target_type(args[i])
                        new_args.append(new_arg)
                    else:
                        new_args.append(args[i])
            except ValueError:
                raise ValueError(error_message.format(args[arg_index]))
            except TypeError:
                raise TypeError(error_message.format(args[arg_index]))

            return method(owner, *new_args)

        return real_method
    return decorator


def gcd(*args):
    if len(args) == 0:
        return 1

    return reduce(old_gcd, args)











