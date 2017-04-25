# Contains the main and helper functions used to generate proofs for Existential Graphs

from existential_statement import *
from rules import *
import sys

# Helper function - removes any literal that matches the specified literal
def remove_literal(literal, tree, out_file):
# ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ###
# Cases that need to be considered:
#         EGAtom, EGNegation, SheetAssignment, EGEmptyCut, **EGAnd**
#         and.... maybe None.....
# Case A: literal is the negation of an atom
#     Base Case 1: EGAtom or EGEmptyCut: return tree (nothing we wanna change)
#     Base Case 2: EGNegation: has chance of being the literal, if it is, return None, if not, return tree (we don't wanna change it)
#     Base Case 3: SheetAssignment or EGAnd: do it to the children, return em as siblings
#     Everything else Case: (or, implicaiton, biconditional): do it to the left and right kids, return em as siblings
# Case B: literal is an atom
#     Base Case 1: EGEmptyCut: return tree (nothing we wanna change)
#     Base Case 2: EGAtom: has chance of being the literal, if it is, return None, if not, return tree (we don't wanna change it)
#     Base Case 3: EGNegation: do it to the kid, return as a kid
#     Base Case 4: SheetAssignment or EGAnd: same as above Base Case A3
#     Everythign else Case: same as above Everything else Case A
# ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ### # ###

    # assert that the literal is an atom or a negation
    # (should also check that the negation is the negation of an atom,
    # but this is just a sanity check, it doesn't catch everything...)
    assert ( isinstance(literal, EGNegation) or  isinstance(literal, EGAtom))

    # Case A: when literal is a negation
    if isinstance(literal, EGNegation):
        #asser that the literal is a literal (the negation should have an atom as a child)
        assert (isinstance(literal.child, EGAtom))
        # Case A: Base Case 1
        if isinstance(tree, EGAtom) or isinstance(tree, EGEmptyCut):
            return tree
        # Case A: Base Case 2
        elif isinstance(tree, EGNegation):
            if ( isinstance(tree.child, EGAtom) ):
                if compare_EG_trees(tree, literal):
                    return None
                else:
                    return tree
        # Case A: Base Case 3
        elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
            new_children = []
            # for each child, apply remove_literal recursively
            for i in range(0, tree.num_children):
                new_children.append(remove_literal(literal, tree.children[i], out_file))
            return EGAnd(len(new_children), new_children)
        # Case A: Everything else Case
        else:
            # if not catched above, the tree must be an Or, Implication or Biconditional
            assert( isinstance(tree, EGOr) or \
                isinstance(tree, EGImplication) or \
                isinstance(tree, EGBiconditional))
            # grab the left and right child after remove literal on them
            left_child = remove_literal(tree.left, out_file)
            right_child = remove_literal(tree.right, out_file)
            # Automatically convert representation to a negation of an AND
            # Only make it a chile, if it isn't None
            if left_child != None:
                old_children.append(left_child)
            if right_child != None:
                old_children.append(right_child)
            new_child = EGAnd(len(old_children), old_children)
            tree = EGNegation(new_child)

    # Case B: when literal is an Atom
    else:
        # Case B: Base Case 1
        if isinstance(tree, EGEmptyCut):
            return tree
        # Case B: Base Case 2
        elif isinstance(tree, EGAtom):
            if compare_EG_trees(tree, literal):
                return None
        # Case B: Base Case 3
        elif isinstance(tree, EGNegation):
            only_child = remove_literal(literal, tree.child, out_file)
            if only_child == None:
                return EGEmptyCut()
            else:
                return EGNegation(only_child)
        # Case B: Base Case 4
        elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
            new_children = []
            # for each child, apply remove_literal recursively
            for i in range(0, tree.num_children):
                new_child = remove_literal(literal, tree.children[i], out_file)
                if new_child != None:
                    new_children.append(new_child)
            return EGAnd(len(new_children), new_children)
        # Case B: Everything else Case
        else:
            # if not catched above, the tree must be an Or, Implication or Biconditional
            assert( isinstance(tree, EGOr) or \
                isinstance(tree, EGImplication) or \
                isinstance(tree, EGBiconditional))
            # grab the left and right child after remove literal on them
            left_child = remove_literal(tree.left, out_file)
            right_child = remove_literal(tree.right, out_file)
            # Automatically convert representation to a negation of an AND
            # Only make it a chile, if it isn't None
            if left_child != None:
                old_children.append(left_child)
            if right_child != None:
                old_children.append(right_child)
            new_child = EGAnd(len(old_children), old_children)
            tree = EGNegation(new_child)
    return tree

# Helper function - removes any double cuts found in the tree
# Should return a sub-tree containing with no double cuts
def remove_dc_from_tree(tree, out_file):
    # Base Case - if an atom or empty cut, just return it
    if isinstance(tree, EGAtom) or isinstance(tree, EGEmptyCut):
        return tree
    # Base Case 2 - if a negation statement, then check to see if any double cuts can be removed
    elif isinstance(tree, EGNegation):
        tree = node_of_cut_to_rm(tree, 0)
        # If it stayed as a negation then just check its child for dc
        if isinstance(tree, EGNegation):
            tree = remove_dc_from_tree(tree.child, out_file)
        # If it was altered and no longer a negation, then check if the new structure contains any double cuts
        else:
            tree = remove_dc_from_tree(tree, out_file)
    elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
        for i in range(0, tree.num_children):
            # Update the parent, which is an SA or AND statement, with all the children with no double cuts
            tree.replace_child(remove_dc_from_tree(tree.children[i], out_file), i)
    else:
        left_child = remove_dc_from_tree(tree.left, out_file)
        right_child = remove_dc_from_tree(tree.right, out_file)

        # Automatically convert representation to a negation of an AND
        old_children = [left_child, right_child]
        new_child = EGAnd(2, old_children)
        tree = EGNegation(new_child)
    return tree

# Helper function - check if there are any empty cuts in a subtree and remove that subtree
# Idea is that only the immediate parent of the empty cut gets removed (entire structure)
# but that's it
def remove_empty_cuts(tree, out_file):
    # Base case:  tree is the empty cut or an atom
    if isinstance(tree, EGEmptyCut) or isinstance(tree, EGAtom):
        return tree
    elif isinstance(tree, EGNegation):
        result = remove_empty_cuts(tree.child, out_file)
        if result == None:
            tree.replace_child(None)
        elif isinstance(tree, EGEmptyCut):
            return None
    elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
        found_empty = False
        for i in range(0, tree.num_children):
            result = remove_empty_cuts(tree.children[i], out_file)
            if result == None:
                tree.remove_child(i)
            # If one of the children is an empty cut, then just get rid of the parent
            elif isinstance(result, EGEmptyCut):
                found_empty = True
                break
            else:
                tree.replace_child(result, i)
        if found_empty == True:
            return None
    else:
        left_child = remove_empty_cuts(tree, out_file)
        right_child = remove_empty_cuts(tree, out_file)

        # This case shouldn't happen, but if it does, should propagate up the tree
        if left_child == None and right_child == None:
            return EGEmptyCut()
        # If one of the children contained an empty cut and has been removed, then just change this to a
        # negation of the remaining child
        elif left_child == None and right_child != None:
            return EGNegation(right_child)
        elif not (left_child != None) and right_child == None:
            return EGNegation(left_child)
        else:
            tree.replace_left_child(left_child)
            tree.replace_right_child(right_child)
            return tree

        # If one of the children contains an empty cut, then remove this structure
        if isinstance(left_child, EGEmptyCut) or isinstance(right_child, EGEmptyCut):
            return None
        else:
            tree.replace_left_child(left_child)
            tree.replace_right_child(right_child)
            return tree
    return tree

# Helper function - clean up any double cuts and empty cuts
def cleanup(tree, out_file):
    # First clean up double cuts from the entire Tree
    update_tree = remove_dc_from_tree(tree, out_file)

    # Second look for empty cuts in a set of children and if at least one is found
    # then remove the parent and all of its children
    update_tree = remove_empty_cuts(tree, out_file)

    return update_tree

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
    # Assumption of program (for now) is that the proof provided is valid
    # If after clean up, None is returned then that means the premises and goal
    # aren't consistent
    print eg_tree
    if eg_tree == None:
        sys.exit("Inconsistent premises and goal! Exiting...")
    # If the only thing that is left on the sheet of assignment is an empty cut,
    # then return an empty cut and end the function
    elif isinstance(eg_tree, SheetAssignment) and eg_tree.num_children == 1 and \
        (isinstance(eg_tree.children[0], EGEmptyCut) or (isinstance(eg_tree.children[0], EGNegation) \
        and eg_tree.children[0].child == None)):
        return EGEmptyCut()
    # Case if left with a negation of an and with a literal and a blob of stuff
    # Remove the literal from the blob and call eg_cons on it after clean up
    # If not in this structure, then assumed that something went wrong, and program terminates
    elif isinstance(eg_tree, SheetAssignment) and eg_tree.num_children == 1:
        old_child = eg_tree.children[0]
        if isinstance(old_child, EGNegation) and isinstance(old_child.child, EGAnd):
            if old_child.child.num_children == 2:
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
    # Case if there are 2 or more premises remaining, then setup all of the premises,
    # run the clean up function on it, then call eg_cons on each of the remaining premises
    elif isinstance(eg_tree, SheetAssignment) and eg_tree.num_children == 2:
        if isinstance(eg_tree.children[0], EGNegation) and isinstance(eg_tree.children[0].child, EGAnd):
            premises = eg_tree.children[0]
            blob = eg_tree.children[1]
            # Double cut all premises and iterate the blob into the outer level of each double cut
            for i in range(0, premises.child.num_children):
                dc_child = node_of_cut_to_add(premises.child.children[i])
                dc_child = iterate(dc_child, blob) # Should just update the double cut with the blob inside it
                premises.child.replace_child(dc_child, i)
            # Erase the outer blob
            eg_tree.remove_child(1)
            eg_tree.replace_child(premises, 0)
            for i in range(0, premises.child.num_children):
                return eg_cons(premises.child.children[i], out_file) # Hopefully will terminate -> should just return an empty cut
        elif isinstance(eg_tree.children[1], EGNegation) and isinstance(eg_tree.children[1].child, EGAnd):
            premises = eg_tree.children[1]
            blob = eg_tree.children[0]
            # Double cut all premises and iterate the blob into the outer level of each double cut
            for i in range(0, premises.child.num_children):
                dc_child = node_of_cut_to_add(premises.child.children[i])
                dc_child = iterate(dc_child, blob) # Should just update the double cut with the blob inside it
                premises.child.replace_child(dc_child, i)
            # Erase the outer blob
            eg_tree.remove_child(0)
            eg_tree.replace_child(premises, 0)
            for i in range(0, premises.child.num_children):
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

    inner_SA = SheetAssignment(1, setup_tree.children[1].child)

    # Run consistency algorithm to determine proof
    final_tree = eg_cons(inner_SA, out_file)
