Implementation of the spreadsheets challenge

## Stack

The solution was implemented in python. While I have worked with python before, it was in the context
of scripting its use was very limited(many years ago as well), this assignment is by far the most complicated task I have ever 
task I have ever implemented in this language. 

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
emulating the linked list of function calls. 

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



Looking forward to your feedback :) 
