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

Inbetween: 
- Parse premise & goal textfile into lex and yacc readable sentence (and feed to parse_sentence in parese_tree.py) (write this in python... Sam)
- Use lex and yacc to parse and represent the statements are trees
- Convert trees into existential graph format (write this in python... Beverly)
  - existential graph format is:
    - "()" to represent a cut
    - strings to represent atoms
    - create existential graph rules systematically (write up rules python then use lex & yacc to parse logic statement & the rule that you're writing [in rules.py]) [talk about this more...]

## Test
In terminal, run:
  
`python generate.py`
  
It will prompt you to input a single well-formed logic statement (recommended to not put in spaces).  Two trees will then be printed if you correctly put in a well-formed logic statement.  The first tree is a binary tree of the original statement, and the second tree is "squashed" tree where only "ANDs" are allowed to have multiple children.
