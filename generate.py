from statement import squash_tree, print_tree
from existential_statement import *
from parse_tree import parse_sentence

# Note this only takes in one line at a time, so for multiple premises, need to add in an implementation to combine into a single tree

logic_statement = raw_input('Input a well-formed logic statement (No quantifiers, no spaces): ')

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
print_eg_tree(eg_tree)

# Print in minimal Pegasus format for debugging
print_tree_pegasus_style(eg_tree)
