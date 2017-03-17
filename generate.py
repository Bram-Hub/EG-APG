import statement
import existential_statement
import parse_tree

logic_statement = raw_input('Input a well-formed logic statement (No quantifiers): ')

# First parse the logic statement
start_tree = parse_tree.parse_sentence(logic_statement)

# Squash AND statement in the tree
stack = []
s = statement.squash_tree(start_tree, stack)
squashed_tree = s.pop()
statement.print_tree(squashed_tree)
