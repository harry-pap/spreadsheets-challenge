# About

Implementation of an interesting spreadsheets challenge. Part of the challenge was to implement it in a language that
I don't have much experience with.


## Problem Statement
You're given a CSV file, titled `transactions.csv`. 

- The delimiter is the pipe operator `|`
- Named columns have an exclamation mark prefix `!`
- Named columns appear anywhere in the file as long as they maintain the same column count
- Cells can have equations prefixed with `=`

The goal is to take `transactions.csv` and compute what needs to be computed producing a file
that contains all the static values + all the equations resolved.

**Operations & Equations**
Any computable expression in the CSV must be prefixed with `=`. The expression
language is very similar to excel formulas, it supports basic arithmetic expressions
as well as function calls that provide additional features like comparisons,
string concatenations and other useful utility functions.

**Operations**

- `^^` Copies the formula from the cell above in the same column, with some special evaluation rules
- `(A..Z)n` references a cell by a combination of a column-letter+row-number. Ex: A2 B3
- `A^` copies the evaluated result of the cell above in the same column
- `!label` Columns can have labels, which allows this ability to have different column groups in the same file as long as the number of columns stays consistent
- `A^v` copies the evaluated result of the last cell in the specified column from the most recently available column group that has data in that specified column
- `@label<n>` References a specific labeled column and a specific row `n` under that column relative to where the column was labeled. This is a reference operator with relative row traversal


## Running
You need the latest python 3.9.6+(earlier versions of python 3 might work as well) in your path as well as pip.

Install virtualenv:
`pip install virtualenv`

Create a virtual evn with:
`python -m venv <virtual-environment-name>` 

Activate the virtual environment:

`source <virtual-environment-name>/bin/activate`

Install the requirements:

`pip install -r requirements.txt`

Run the tests:

`python -m unittest`

To run the tool, provide the path to the input file as the first argument, and the output as the second:

`python main.py /tmp/parser/transactions.csv /tmp/parser/output.csv`


## Implementation
Each expression is parsed into a binary syntax tree, which is evaluated from the left bottom up(Post-Order traversal). 
If no numeric operators are in place then each function is added as the left child of the enclosing function, effectively
emulating the stack of function calls. 

### Arithmetic operators
When arithmetic operators are involved, two variables(pointers) are used to track root(lowest priority operation) and 
last added(which may point to root, or to the right child of root). A weight property is used to determine operator 
priority. The following logic is used to re-order the tree, where `operator` is the current scanned operator, `subtree`
is the currently scanned subtree(can be a value or an expression within parentheses, which is computed recursively), 
when parsing `1+2`, `+` is `operator` and `1` is `subtree` :

* if `last_added is none`(tree initialisation) 

 -> operator.left = subtree 

 -> root, last_added = operator

* else if `operator.weight > last_added.weight` (scanned operator should be executed before last added, so it ends up a level below last_added)

-> operator.left = subtree

-> last_added.right = operator

-> last_added = operator

* else if `operator.weight > root.weight` (scanned operator has the same weight or lower as last_added, but has priority
over root, so should be executed after last_added but before root, for example: 1+2\*3\*4, the second multiplication(*4)
should be executed after the first multiplication but before the addition)

-> last_added.right = subtree

-> operator.left = last_added

-> last_added = operator

-> root.right = last_added

* `else` (operator is lower/same priority as root, should be executed last and thus becomes root)

-> last_added.right = subtree

-> operator.left = root

-> last_added, root = operator

#### Example tree
The expression `sqr(sqr(2))+3+4*5*6` (where sqr returns the square of a number) is represented by the following tree,
where left child appears before the right child

```
Addition
├── Addition
│   ├── Square
│   │   └── Square
│   │       └── 2
│   └── 3
└── Multiplication
    ├── Multiplication
    │   ├── 4
    │   └── 5
    └── 6
```

### CSV processing
When the csv is being processed, the results of the functions are written on a per-line basis to the output file, 
the syntax tree of each cell however is stored in a dictionary, which is accessed later if a cell has a reference to the
given computed cell or copies it. A cell may only be referenced(explicitly i.e. `B3` or relatively `B^V`) if it has
already been processed. When the copy operator(`^^`) is found, the expression tree is copied the argument to `incFrom`
if it belongs to the tree is incremented. Please note that the <b>STATIC REFERENCE</b> remains the same if copied(and 
not incremented each time it's copied), not sure if this is the intended behaviour, I can create a fix for this if
that's the case

### Special case nodes

#### Link
When a function may have more than two arguments, like concat or sum, then a special case `Link` node is added, 
which purpose is to link together multiple values. When the tree is traversed all values under one or more `Link` objects
are gathered in a single list and submitted to the function

#### CellReferencingNode 
For relative operators link `A^`, a special `CellReferencingNode` is added in the tree. When the tree is traversed the
value of the node is instantiated and computed. 

### Known issues
For the sake of a fast solution a circular dependency was introduced between cell_reference.py and node.py, and in the 
solution is not polished in general, as it's meant to be a challenge and not production code.
