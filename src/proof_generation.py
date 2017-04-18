# Contains the main and helper functions used to general proofs for Existential Graphs

from existential_statement import *
from rules import *

def setup(premises, goal):
    # First add an empty double cut onto the sheet of assignment
    empty_dc = node_of_cut_to_add(None)
    try:
        if isinstance(premises, SheetAssignment):
            premises.add_children(empty_dc)
    except ValueError:
        print "Incorrect format for the premises existential graph tree!"

    print "Added empty double cut: "
    print_eg_tree(premises)

    # Insert the negation of the goal into the outer level of the double cut
    negate_goal = EGNegation(goal)
    # Based on what was done above, the empty dc should be the last child on the sheet of assignment
    temp = iterate(premises.children[premises.num_children-1], negate_goal)
    premises.replace_child(temp, premises.num_children-1)
    print "Inserted the negation of goal:"
    print_eg_tree(premises)

    # Iterate the premises and complement of the goal into the inner level of the double cut
    p = premises.children[0]
    temp = iterate(premises.children[premises.num_children-1].children[0], p)
    temp = iterate(premises.children[premises.num_children-1].children[0], negate_goal)
    premises.children[premises.num_children-1].replace_child(temp, premises.children[premises.num_children-1][0])
    print "Inserted the negation of goal and premises:"
    print_eg_tree(premises)

    return premises

# Main function for finding a proof with the given premises and goal
# Takes in a tree of all the premises combined into a single eg tree and the
# goal as an eg tree
def find_proof(premises, goal):
    print "Provided premises:"
    print_eg_tree(premises)
    print "Provided goal:"
    print_eg_tree(goal)

    # Run setup on premises
    setup_tree = setup(premises, goal)

    print "This is the setup tree: "
    print_eg_tree(setup_tree)

    # Run consistency algorithm to determine proof
    #final_tree = eg_cons(setup_tree.children[1]).right_child())
