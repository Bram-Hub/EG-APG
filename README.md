# ExistentialGraphProofGenerator
Generates Existential Graph Proofs from set of premises to a goal.

Assumptions: We are given a valid argument.

Input: (1) premises & goal textfile

  textfiles are formatted as such:

    atoms are '[a-zA-Z]''
    not is '~''
    and is '&''
    or is '|''
    implication is '-''
    biconditional is '='
    contradiction is '!'
    left parenthesis is '('
    right parenthesis is ')'
    and the goal is prepended by '$'

  ex: premises_example.txt:       
          `p & q
          r | s`

  ex: goal_example.txt:
          `p`

## To Do
- Parse premise & goal textfile into lex and yacc readable sentence (and feed to parse_sentence in parese_tree.py) (write this in python... Sam)
- Use lex and yacc to parse and represent the statements are trees
- Convert trees into existential graph format (write this in python... Beverly)
  - existential graph format is:
    - "()" to represent a cut
    - strings to represent atoms
    - create existential graph rules systematically (write up rules python then use lex & yacc to parse logic statement & the rule that you're writing [in rules.py]) [talk about this more...]

## Pegasus format
Currently each line in Pegasus starts off with an action and two states: the start and end states.
atoms : A...Z...0...9
cuts: ()
end of atom : |
[-] : stuff in between brackets to be removed
[+] : stuff in between brackets to be added
[/] : keep everything in between these brackets
[.] : notifies where the iteration is coming from

## Test
In terminal, run:

`python generate.py <premise.txt> <goal.txt>`

premises.txt and goal.txt should contain well-formed logic statement (recommended to not put in spaces).

Two trees will be printed for each premise and goal if you correctly put in a well-formed logic statement.  The first tree is a binary tree of the original statement, and the second tree is "squashed" tree where only "ANDs" are allowed to have multiple children.
