# Carroll
Carroll is a **C**ommand-line **A**pp for **R**apidly **R**emoving **O**bstacles to **L**earning **L**ogic.

<h2>Usage</h2>
```
$ python carroll.py table "((A&B) v (~A&~B))" --verbose
 A  B  True
~A  B  False
 A ~B  False
~A ~B  True

Satisfiable: True
Tautology: False
```
To find out which characters Carroll interprets as connectives (and to define your own), see `symbols.py`.

**Dependencies:** Carroll uses Nose and Click.


<h2>Commands</h2>

 - ```table```: Prints a truth table for an expression. Optionally checks satisfiability and tautology too.
 - ```equiv```: Checks two expressions for logical equivalence (i.e. whether they compute the same boolean function)
 - ```cnf``` and ```dnf```: Converts an expression to its equivalent in conjunctive or disjunctive normal form.

<h2>Planned features:</h2>

 - Check any number of propositions for equivalence, mutual satisfiability, etc
 - Simplify expressions
 - Use user-defined connectives?
