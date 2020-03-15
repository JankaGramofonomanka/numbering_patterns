# numbering_patterns
This is a project that contains classes that are meant to make working
with graph numberings easier. The classes are: LinearFormula,
NTermRecursionSequence, CentralVertexNumberingPattern.


## ```LinearFormula```
The class ```LinearFormula``` in linear_formula.py represents a linear 
formula also known as first degree polynomial.
The user can initialize it with a string, insert and remove segments,
simplify it, substitute variables with other formulas, and find the
modulo n equivalent of it


## ```NTermRecursionSequence```
This class represents an n-term-recursion sequence, that is a sequence
determined by n formulas f_1(i), f_2(i), ...f_n(i), in the following 
way:
sequence == ( f_1(0), f_2(0), ... f_n(0), f_1(1), f_2(1), ..., f_n(1),
              f_1(2), f_2(2), ... f_n(2), ... )


## ```CentralVertexNumberingPattern```
This class represents a numbering pattern of a cycle (a type of a graph)
determined by a central vertex number, left-hand and right-hand 
sequences. For example if the central number is c,
the left-hand sequence is l_n (n = 1, 2, 3, ...)
the right-hand sequence is r_n (n = 1, 2, 3, ...)
then the pattern will be:
..., l_3,   l_2,   l_1,   c,   r_1,   r_2,   r_3, ...
..., v_n-3, v_n-2, v_n-1, v_0, v_1,   v_2,   v_3, ...
where the cycle is v_0, v_1, v_2, ..., v_n-2, v_n-1, v_0,
and v_0 is chosen to be the central vertex


## example usage of ```LinearFormula```
### 1. Initialization:
```
>>> LinearFormula('a + 3b - 4c')
a + 3b - 4c
(Currently the string-to-formula conversion algorithm supports only 
integer multipliers)

>>> LinearFormula({'a': 1, 'b': 3, 'c': -4'})
a + 3b - 4c

>>> LinearFormula([1, 3, -4], ['a', 'b', 'c'])
a + 3b - 4c

>>> LinearFormula(45)
45
```
### 2. Evaluation:
```
>>> LinearFormula('a + 3b').evaluate(a=2, b=1})
5
```
### 3. Substitute variables:
```
>>> formula_1 = LinearFormula('a + 3b - 4c')
>>> formula_2 = LinearFormula('x + 2')
>>> formula_1.substitute(a=formula_2)
x + 2 + 3b - 4c

>>> formula_1.substitute(a='y - 2')
y - 2 + 3b - 4c

>>> formula_1.substitute(a='x', b='y', c='2a')
x + 3y - 8a
```
### 4. Simplify:
```
>>> formula_1 = LinearFormula('a + 3b - 4c + 3a - b')
>>> formula_.zip()
4a + 2b - 4c
```
### 5. Find modulo equivalent:
```
>>> LinearFormula('a + 5b + 6c + 4').modulo(3)
a + 2b + 1
```
### 6. Add/insert/remove segments:
```
>>> LinearFormula('a + 3b').add_segment(-4, 'c')
a + 3b - 4c

>>> LinearFormula('a + 3b').insert_segment(-4, 'c', 1)
a - 4c + 3b

>>> LinearFormula('a + 3b - 4c').remove_segment(1)
a - 4c
```
### 7. The methods used in points 3 - 6 can modify the formula instead of 
returning another formula
```
>>> formula_1 = LinearFormula('a + 3b')
>>> formula_1.add_segment(-4, 'c', inplace=True)
>>> formula_1
a + 3b - 4c

>>> forula_2 = formula_1.add_segment(5, 'd')
>>> formula_2
a + 3b - 4c + 5d

>>> formula_1
a + 3b - 4c
```
### 8. Operations on formulas:
```
>>> formula_1 = LinearFormula('a + 3b')
>>> formula_2 = LinearFormula('4c - d')

>>> -formula_1
-a - 3b

>>> fornula_1 + formula_2
a + 3b + 4c - d

>>> formula_1 + formula_2
a + 3b - 4c + d

>>> formula_1 * 2
2a + 6b

>>> formula_1 % 2
a + b

>>> formula_1[0]
(3, 'b')
```
### 9. Other:
```
>>> LinearFormula('a + 3b - 4c').length()
3

>>> LinearFormula('a + 3b - 4c').get_segment(1)
(3, 'b')

>>> LinearFormula('a + 3b - 4c').copy()
a + 3b - 4c
```
