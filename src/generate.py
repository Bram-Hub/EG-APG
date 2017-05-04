from statement import squash_tree, print_tree
from existential_statement import *
from parse_tree import parse_sentence
from rules import *
from proof_generation import find_proof
import proof_generation as pg
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

if len(sys.argv) < 2:
    print "invalid command. please enter \"python generate.py premise.txt [-g goal.txt] [-o outputfilename]\""
    exit(1)

premise_text_file = sys.argv[1] #raw_input("Enter premises textfile name (ex. premise.txt):")
goal_text_file = premise_text_file[:-4] + "_goal.txt" #raw_input("Enter goal textfile name (ex. goal.txt):")

# Create the output file 
out_file = open('output.pega', 'w')
for i, a in enumerate(sys.argv):
  if a == "-o":
    assert (i+1 < len(sys.argv))
    outputfilename = sys.argv[i+1]
    out_file = open(outputfilename+'.pega', 'w')
  elif a == "-g":
    assert (i+1 < len(sys.argv))
    goal_text_file = sys.argv[i+1]




path = "../testcases/"
# path = ""

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
        print_tree_pegasus_style(premise_tree)

final_premise_tree = SheetAssignment(0, [])
and_tree = EGAnd(0, [])

# If there's only one premise, then don't need to concatenate anything together
if len(premise_trees) == 1:
    final_premise_tree = premise_trees[0]
else:
    # Assume that the root of every tree is SA
    for tree in premise_trees:
        #DEBUGGING PRINT
        print "Printing beautiful sideways format"
        print_eg_tree(tree)
        #ANOTHER DEBUGGING PRINT
        print_tree_pegasus_style(tree)
        # Merge premises into a single tree
        if tree.num_children > 1:
            temp = EGAnd(0, [])
            for i in range(0, tree.num_children):
                temp.add_children(tree.children[i])
                final_premise_tree.add_children(temp)
        else:
            and_tree.add_children(tree.children[0])
    final_premise_tree.add_children(and_tree)

print "Final Premise Tree:"
print_eg_tree(final_premise_tree)

print '\n\nGOAL reading: ', goal_text_file
file = open(path + goal_text_file, 'r')
goal = file.read()
goal_tree = parse(goal)
#DEBUGGING PRINT
print "Printing beautiful sideways format"
print_eg_tree(goal_tree)
#ANOTHER DEBUGGING PRINT
print_tree_pegasus_style(goal_tree)

# testing compare : should make more tests for like if extra SA's
#print "expect true (1): ", compare_EG_trees(premise_trees[0], premise_trees[0])
# print "expect false (0): ", compare_EG_trees(premise_trees[0], premise_trees[1])


# uncomment when find_proof happens
find_proof(final_premise_tree, goal_tree, out_file)


# testing remove_literal(literal, tree, out_file) :
# print "\n***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** "

# out_file = open('output-test.pega', 'w')
# testing_temp = pg.remove_literal(EGAtom("P"), EGAnd(2, [EGAtom("P"), EGAtom("Q")]), out_file)
# print " expect just Q: ", print_tree_pegasus_style(testing_temp),  print_eg_tree(testing_temp), "  <<< that's what I get... "
