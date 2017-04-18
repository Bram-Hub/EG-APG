from statement import squash_tree, print_tree
from existential_statement import *
from parse_tree import parse_sentence
from rules import *
import sys

# Note this only takes in one line at a time, so for multiple premises,
#     need to add in an implementation to combine into a single tree
def parse(logic_statement):
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
  sa = SheetAssignment(0, [])
  for i in range(0, stack_len):
      prev_statement = e.pop()
      sa.add_children(prev_statement)
  eg_tree = sa
  # DEBUGGING TO MAKE SURE PARSED CORRECTLY
  # print_eg_tree(eg_tree)

  # Print in minimal Pegasus format for debugging
  # DEBUGGING TO MAKE SURE PARSED CORRECTLY
  # print_tree_pegasus_style(eg_tree)
  return eg_tree

  # Test for remove double cut - should write a general double cut function that handles what you pass in and stuff
  # print "Removing a double cut"
  # no_dc_tree = node_of_cut_to_rm(eg_tree.children[0])
  # print_eg_tree(no_dc_tree)

  # Test for adding a double cut
  # print "Adding a double cut"
  # new_dc_tree = node_of_cut_to_add(eg_tree.children[0])
  # print_eg_tree(new_dc_tree)

  # Test for iterating
  # print "Iterating"
  # new_tree = iterate(eg_tree.children[0].children[1], eg_tree.children[0].children[0])
  # print_eg_tree(new_tree)

if len(sys.argv) != 3:
    print "invalid command. please enter \"python generate.py premise.txt goal.txt\""
    exit(1)

premise_text_file = sys.argv[1] #raw_input("Enter premises textfile name (ex. premise.txt):")
goal_text_file = sys.argv[2] #raw_input("Enter goal textfile name (ex. goal.txt):")

path = "../testcases/"

premise_trees = []


print '\nPREMISE reading: ', premise_text_file
with open(path + premise_text_file, 'r') as file:
    for line in file:
        premise_txt = line
        print "read: ", premise_txt
        premise_tree = parse(premise_txt)
        premise_trees.append(premise_tree)
        # #DBUGGING PRINT
        # print_eg_tree(premise_tree)
        # #ANOTHER DEBUGGING PRINT
        # print_tree_pegasus_style(premise_tree)

for tree in premise_trees:
    #DBUGGING PRINT
    print "Printing beautiful sideways format"
    print_eg_tree(tree)
    #ANOTHER DEBUGGING PRINT
    print_tree_pegasus_style(tree)

print '\n\nGOAL reading: ', goal_text_file
file = open(path + goal_text_file, 'r')
goal = file.read()
goal_tree = parse(goal)
#DBUGGING PRINT
print "Printing beautiful sideways format"
print_eg_tree(goal_tree)
#ANOTHER DEBUGGING PRINT
print_tree_pegasus_style(goal_tree)


# testing compare
print "expect true (1): ", compare_EG_trees(premise_trees[0], premise_trees[0])
print "expect false (0): ", compare_EG_trees(premise_trees[0], premise_trees[1])

# uncomment when find_proof happens
# find_proof(premises_tree, goal_tree)
