# numbering_patterns
This is a project that contains classes that are meant to make working
with graph numberings easier. The classes are: ```LinearFormula```, 
```LinearRelation```, ```NTermRecursionSequence```, 
```CentralVertexNumberingPattern```.


## ```LinearFormula```
The class ```LinearFormula``` in linear_formula.py represents a linear 
formula also known as first degree polynomial.
The user can initialize it with a string, insert and remove segments,
simplify it, substitute variables with other formulas, and find the
modulo n equivalent of it


## ```LinearRelation```
This class represents a relation (equality or inequality) between two 
linear formulas, for example 'a + b <= c + 3d'.


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


## Example usage of ```LinearFormula```
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
### 2. Modification
#### Add/insert/remove segments:
```
>>> LinearFormula('a + 3b').add_segment(-4, 'c')
a + 3b - 4c

>>> LinearFormula('a + 3b').insert_segment(-4, 'c', 1)
a - 4c + 3b

>>> LinearFormula('a + 3b - 4c').remove_segment(1)
a - 4c
```
#### Substitute variables:
```
>>> formula_1 = LinearFormula('a + 3b - 4c')
>>> formula_2 = LinearFormula('x + 2')
>>> formula_1.substitute(a=formula_2)
x + 2 + 3b - 4c

>>> formula_1.substitute(a='y - 2')
y - 2 + 3b - 4c

>>> formula_1.substitute(a='x', b='y', c='2a')
x + 3y - 8a

>>> formula_1.substitute(a='b', b='d')
b + 3d - 4c

>>> formula_1.substitute(a='b', b='d', recursive=True)
d + 3d - 4c
```
#### Simplify:
```
>>> formula_1 = LinearFormula('a + 3b - 4c + 3a - b')
>>> formula_.zip()
4a + 2b - 4c
```
#### Find modulo equivalent:
```
>>> LinearFormula('a + 5b + 6c + 4').modulo(3)
a + 2b + 1
```
#### Modify "in place":
The methods presented in the "Modification" section can modify the 
formula instead of returning another formula
```
>>> formula_1 = LinearFormula('a + 3b')
>>> formula_1.add_segment(-4, 'c', inplace=True)
>>> formula_1
a + 3b - 4c

>>> formula_2 = formula_1.add_segment(5, 'd')
>>> formula_2
a + 3b - 4c + 5d

>>> formula_1
a + 3b - 4c
```
### 3. Operations on formulas
```
>>> formula_1 = LinearFormula('a + 3b')
>>> formula_2 = LinearFormula('4c - d')

>>> -formula_1
-a - 3b

>>> fornula_1 + formula_2
a + 3b + 4c - d

>>> formula_1 - formula_2
a + 3b - 4c + d

>>> formula_1 * 2
2a + 6b

>>> formula_1 % 2
a + b

>>> formula_1[1]
(3, 'b')

>>> formula_1['b']
3
```
### 4. Other math stuff
#### Evaluation:
```
>>> LinearFormula('a + 3b').evaluate(a=2, b=1})
5
```
#### Equivalence:
```
>>> LinearFormula('a + 2b').equivalent('2b + a')
True
>>> LinearFormula('a + b').equivalent('a + 2b')
False
>>> LinearFormula('a + 2b').equivalent('x + 2y')
False
```
#### Separate a "subformula":
A line ```formula_1.separate(formula_2)``` will return a tuple 
```(m, formula_3)``` such that: 
```formula_1 == m * formula_2 + formula_3```.
```
>>> LinearFormula('2a + 2b + c + 4d').separate('a + b')
(2, c + 4d)

>>> LinearFormula('2a + 3b + c + 4d').separate('a + b')
(2, b + c + 4d)
```
#### Find bounds, given the bounds of individual variables:
The method ```LinearForula.get_bouds``` will take two dicts: 
```lower_bounds``` and ```upper_bounds```, such that if 
```lower_bounds[variable] == formula_1``` and 
```upper_bounds[variable] == formula_2``` then that means 
```formula_1 <= variable <= formula_2```, and return a tuple that 
consists of lower and upper bounds of the original formula. 
```
>>> lower_bounds = {'a': 1, 'b': '2c'}
>>> upper_bounds = {'a': '5d'}
>>> LinearFormula('a + b').get_bounds(lower_bounds, upper_bounds)
(1 + 2c, 5d + b)

>>> LinearFormula('a - b').get_bounds(lower_bounds, upper_bounds)
(1 - b, 5d - 2c)

>>> lower_bounds = {'a': 'b', 'b': 'c'}
>>> upper_bounds = {'a': 'd', 'd': 'f'}
>>> formula = LinearFormula('a')
>>> formula.get_bounds(lower_bounds, upper_bounds, recursive=True)
(c, f)
```
### 5. Simple utilities
```
>>> LinearFormula('a + 3b - 4c').length()
3

>>> LinearFormula('a + 3b - 4c').copy()
a + 3b - 4c

>>> LinearFormula('a + 3b - 4c').get_segment(1)
(3, 'b')

>>> LinearFormula('a + 3b - 4c').get_variables()
{'a', 'b', 'c'}
```



## Example usage of ```LinearRelation```
### 1. Initialization
```
>>> LinearRelation('a', 'b')
a == b

>>> LinearRelation('a', 'b', relation='>')
a > b

>>> LinearRelation('a <= b')
a <= b

>>> formula_1 = LinearForula('a')
>>> formula_2 = LinearForula('b')
>>> LinearRelation(formula_1, formula_2, relation='<')
a < b

>>> relation = LinearRelation('a == b')
>>> LinearRelation(relation)
a == b
```
### 2. Modification
#### Substitute variables:
```
>>> relation = LinearRelation('a + b == c')
>>> formula = LinearFormula('x + 2')
>>> relation.substitute(a=formula)
x + 2 + b == c

>>> relation.substitute(a='y - 2')
y - 2 + b == c

>>> relation.substitute(a='x', b='y', c='2a')
x + y == 2a

>>> relation.substitute(a='b', b='d', recursive=True)
d + d == c
```
#### Simplify:
```
>>> relation = LinearRelation('a + 3c + a == 4c + 3b - b')
>>> relation.zip()
2a + 3c == 4c + 2b
```
#### Find modulo equivalent:
```
>>> LinearRelation('a + 5b == 7b + 4').modulo(3)
a + 2b == b + 4
```
#### Reverse:
```
>>> LinearRelation('a == b').reverse()
b == a

>>> LinearRelation('a <= b').reverse()
b >= a
```
#### Solve:
```
>>> LinearRelation('a + 3b == 2b - 4a').solve()
5a + b == 0
```
#### Expose a variable:
```
>>> LinearRelation('a - 2b + c == 3d').expose('a')
a == 3d + 2b - c
```
#### Modify "in place":
Similarly to ```LinearFormula```, the methods presented in the 
"Modification" section can modify the relation instead of returning 
another relation
```
>>> relation_1 = LinearRelation('a == 3b')
>>> relation_1.substitute(a=2x)
>>> relation_1
a == 3b

>>> relation_2 = relation_1.substitute(a=2x)
>>> relation_2
2x == 3b

>>> relation_1
a == 3b
```
### 3. Operations on formulas
```
>>> relation_1 = LinearRelation('a == 3b')
>>> relation_2 = LinearRelation('4c == d')

>>> -relation_1
-a == -3b

>>> relation_1 + relation_2
a + 4c == 3b + d

>>> relation_1 - relation_2
a - 4c == 3b - d

>>> relation_1 + '2c'
a + 2c == 3b + 2c

>>> relation_1 - '2c'
a - 2c == 3b - 2c

>>> relation_1 * 2
2a == 6b

>>> relation_1 % 2
a == b
```
```
>>> relation_1 = LinearRelation('a <= 3b')
>>> relation_2 = LinearRelation('4c <= d')

>>> -relation_1
-a >= -3b

>>> relation_1 + relation_2
a + 4c <= 3b + d

>>> relation_1 - relation_2
a - d <= 3b - 4c

>>> relation_1 + '2c'
a + 2c <= 3b + 2c

>>> relation_1 - '2c'
a - 2c <= 3b - 2c

>>> relation_1 * 2
2a <= 6b
```
### 4. Other math stuff
#### Evaluation:
```
>>> LinearRelation('a == 3b').evaluate(a=2, b=1})
2 == 3
```
#### Epistemological status:
```
>>> LinearRelation('a == a').status()
'true'

>>> LinearRelation('a <= a').status()
'true'

>>> LinearRelation('a < a').status()
'false'

>>> LinearRelation('a == b').status()
'unknown'

>>> LinearRelation('a <= b').status()
'unknown'

>>> LinearRelation('1 == 0').status()
'false'

>>> LinearRelation('1 <= 0').status()
'false'

>>> LinearRelation('1 >= 0').status()
'true'
```
#### Equivalence:
```
>>> LinearRelation('a == b').equivalent('b == a')
True

>>> LinearRelation('a <= b').equivalent('b >= a')
True

>>> LinearRelation('a == b').equivalent('2a == 2b')
True

>>> LinearRelation('a == b').equivalent('c == d')
False

>>> LinearRelation('a == b').equivalent('a == 2b')
False
```
### 5. Simple utilities
```
>>> LinearRelation('a + 3b == 4c').copy()
a + 3b == 4c

>>> LinearRelation('a + 3b == 4c').get_variables()
{'a', 'b', 'c'}
```
