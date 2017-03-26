from statement import squash_tree, print_tree
from existential_statement import *
from parse_tree import parse_sentence
import sys

# Note this only takes in one line at a time, so for multiple premises, 
#     need to add in an implementation to combine into a single tree
def parse_and_print(logic_statement):
  # First parse the logic statement
  start_tree = parse_sentence(logic_statement)

  # Squash AND statement in the tree
  stack = []
  s = squash_tree(start_tree, stack)
  squashed_tree = s.pop()
  print_tree(squashed_tree)

  # Transform the tree into an Existential graph tree
  stack = []
  e = transform(squashed_tree, stack)
  stack_len = len(e)
  sa = SheetAssertion(0, [])
  for i in range(0, stack_len):
      prev_statement = e.pop()
      sa.add_children(prev_statement)
  eg_tree = sa
  print_eg_tree(eg_tree)

if len(sys.argv) != 3:
  print "invalid command. please enter \"python generate.py premise.txt goal.txt\""
  exit(1)

premise_text_file = sys.argv[1] #raw_input("Enter premises textfile name (ex. premise.txt):")
goal_text_file = sys.argv[2] #raw_input("Enter goal textfile name (ex. goal.txt):")

path = "testcases/"

print '\nreading: ', premise_text_file
file = open(path + premise_text_file, 'r') 
premise = file.read()
parse_and_print(premise)

print '\nreading: ', goal_text_file
file = open(path + goal_text_file, 'r') 
goal = file.read()
parse_and_print(goal)