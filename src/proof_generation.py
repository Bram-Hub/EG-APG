# Contains the main and helper functions used to general proofs for Existential Graphs

from existential_statement import *
from rules import *
import sys

# Helper function - removes any literal that matches the specified literal
def remove_literal(literal, tree, out_file):
    return False

# Helper function - clean up any double cuts and empty cuts
def cleanup(tree, out_file):
    return False

# Converts the premises tree into the format needed for conducting the proof
# Also includes the setup files in the output file
def setup(premises, goal, out_file):
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
    negate_goal = EGNegation(goal.children[0])
    print "This is the negated goal:"
    print_eg_tree(negate_goal)
    # Based on what was done above, the empty dc should be the last child on the sheet of assignment
    temp = iterate(premises.children[premises.num_children-1], negate_goal)
    premises.replace_child(temp, premises.num_children-1)
    print "Inserted the negation of goal:"
    print_eg_tree(premises)

    # Iterate the premises and complement of the goal into the inner level of the double cut
    if isinstance(premises.children[1], EGNegation):
        if isinstance(premises.children[1].child, EGAnd):
            p = premises.children[0]
            temp = iterate(premises.children[premises.num_children-1].child.children[0], p)
            temp = iterate(premises.children[premises.num_children-1].child.children[0], negate_goal)
            premises.children[premises.num_children-1].child.replace_child(temp, 0)
            print "Inserted the negation of goal and premises:"
            print_eg_tree(premises)
    else:
        sys.exit("Incorrectly formatted tree!")

    return premises

# Consistency checker - evaluates if all the given premises and complement of the
# goal are consistent with one another -> will also generate the proof in the
# output file that can be loaded into Pegasus
def eg_cons(eg_tree, out_file):
    if eg_tree == None:
        sys.exit("Inconsistent premises and goal! Exiting...")
    elif isinstance(eg_tree, SheetAssignment) and eg_tree.num_children() == 1 and \
        (isinstance(eg_tree.children[0], EGEmptyCut) or (isinstance(eg_tree.children[0], EGNegation) and eg_tree.children[0].child == None)):
        return EGEmptyCut()
    elif isinstance(eg_tree, SheetAssignment) and eg_tree.num_children() == 1:
        old_child = eg_tree.children[0]
        if isinstance(old_child, EGNegation) and isinstance(old_child.child, EGAnd):
            if old_child.child.num_children() == 2:
                if isinstance(old_child.child.children[0], EGAtom):
                    temp = remove_literal(old_child.child.children[0], old_child.child.children[1], out_file)
                    temp = cleanup(temp, out_file)
                    eg_tree.replace_child(temp, 0)
                    return eg_cons(eg_tree, out_file)
                elif isinstance(old_child.children[1], EGAtom):
                    temp = remove_literal(old_child.children[1], old_child.children[0], out_file)
                    temp = cleanup(temp, out_file)
                    eg_tree.replace_child(temp, 0)
                    return eg_cons(eg_tree, out_file)
                else:
                    print_eg_tree(eg_tree)
                    sys.exit("Missing a literal for this case for eg_cons!")
            else:
                print_eg_tree(eg_tree)
                sys.exit("Too many children for this case for eg_cons!")
        else:
                print_eg_tree(eg_tree)
                sys.exit("Incorrectly formatted tree for the 3rd case in eg_cons!")
    elif isinstance(eg_tree, SheetAssignment) and eg_tree.num_children() == 2:
        if isinstance(eg_tree.children[0], EGNegation) and isinstance(eg_tree.children[0].child, EGAnd):
            premises = eg_tree.children[0]
            blob = eg_tree.children[1]
            # Double cut all premises and iterate the blob into the outer level of each double cut
            for i in range(0, premises.child.num_children()):
                dc_child = node_of_cut_to_add(premises.child.children[i])
                dc_child = iterate(dc_child, blob) # Should just update the double cut with the blob inside it
                premises.child.replace_child(dc_child, i)
            # Erase the outer blob
            eg_tree.remove_child(1)
            eg_tree.replace_child(premises, 0)
            for i in range(0, premises.child.num_children()):
                return eg_cons(premises.child.children[i], out_file) # Hopefully will terminate -> should just return an empty cut
        elif isinstance(eg_tree.children[1], EGNegation) and isinstance(eg_tree.children[1].child, EGAnd):
            premises = eg_tree.children[1]
            blob = eg_tree.children[0]
            # Double cut all premises and iterate the blob into the outer level of each double cut
            for i in range(0, premises.child.num_children()):
                dc_child = node_of_cut_to_add(premises.child.children[i])
                dc_child = iterate(dc_child, blob) # Should just update the double cut with the blob inside it
                premises.child.replace_child(dc_child, i)
            # Erase the outer blob
            eg_tree.remove_child(0)
            eg_tree.replace_child(premises, 0)
            for i in range(0, premises.child.num_children()):
                temp_child = cleanup(premises.child.children[i], out_file)
                return eg_cons(temp_child, out_file) # Hopefully will terminate -> should just return an empty cut
        else:
            print_eg_tree(eg_tree)
            sys.exit("Incorrectly formatted tree for the 4th case in eg_cons!")
    else:
        print_eg_tree(eg_tree)
        sys.exit("Incorrectly formatted tree for eg_cons!")

# Main function for finding a proof with the given premises and goal
# Takes in a tree of all the premises combined into a single eg tree and the
# goal as an eg tree
def find_proof(premises, goal):
    print

    # Create the output file -> should make it an option that the user puts in
    # the name of the file at the beginning
    out_file = open('output.pega', 'w')

    print "Provided premises:"
    print_eg_tree(premises)
    print "Provided goal:"
    print_eg_tree(goal)

    # Run setup on premises
    setup_tree = setup(premises, goal, out_file)

    print "This is the setup tree: "
    print_eg_tree(setup_tree)


    # Run consistency algorithm to determine proof
    #final_tree = eg_cons(setup_tree.children[1]).right_child())
