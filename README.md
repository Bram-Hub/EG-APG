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
          p & q
          r | s

  ex: goal_example.txt:
          p

Inbetween: - Parse premise & goal textfile into lex and yacc readable sentence (and feed to parse_sentence in parse_tree.py) (write this in python... Sam)

           - Use lex and yacc to parse and represent the statements are trees
           - Convert trees into existential graph format (write this in python... Beverly)
                  - existential graph format is:
                          - "()" to represent a cut
                          - strings to represent atoms

           - create existential graph rules systematically (write up rules python then use lex & yacc to parse logic statement & the rule that you're writing [in rules.py])
           - clean up method
           - double cut w/ insertion set up (w/ manual trees)