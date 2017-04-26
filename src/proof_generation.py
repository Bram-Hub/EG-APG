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
    print "In remove double cuts from tree.  Here is tree:"
    print tree
    print_eg_tree(tree)
    # Base Case - if an atom or empty cut, just return it
    if isinstance(tree, EGAtom) or isinstance(tree, EGEmptyCut) or tree == None:
        return tree
    # Base Case 2 - if a negation statement, then check to see if any double cuts can be removed
    elif isinstance(tree, EGNegation):
        tree = node_of_cut_to_rm(tree, 0)
        # print "In Negation check... Here is the tree after remove dc function:"
        # print_eg_tree(tree)
        # return tree
        # If it stayed as a negation then just check its child for dc
        if isinstance(tree, EGNegation):
            tree.replace_child(remove_dc_from_tree(tree.child, out_file))
        # If it was altered and no longer a negation, then check if the new structure contains any double cuts
        else:
            tree = remove_dc_from_tree(tree, out_file)
            # return tree
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
    # print "Here is the result: "
    # print tree
    return tree

# Helper function - check if there are any empty cuts in a subtree and remove that subtree
# Idea is that only the immediate parent of the empty cut gets removed (entire structure)
# but that's it
def remove_empty_cuts(tree, out_file):
    # print "In remove empty cuts:"
    # print tree
    # print_eg_tree(tree)

    # Base case:  tree is the empty cut or an atom
    if isinstance(tree, EGEmptyCut) or isinstance(tree, EGAtom) or tree == None:
        return tree
    elif isinstance(tree, EGNegation):
        result = remove_empty_cuts(tree.child, out_file)
        if result == None:
            tree.replace_child(None)
        elif isinstance(tree, EGEmptyCut):
            return None
    elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
        found_empty = False
        i = 0
        while i < tree.num_children:
            result = remove_empty_cuts(tree.children[i], out_file)
            if result == None:
                tree.remove_child(i)
                i -= 1
            # If one of the children is an empty cut, then just get rid of the parent
            elif isinstance(result, EGEmptyCut):
                found_empty = True
                break
            else:
                tree.replace_child(result, i)
                i += 1
        if found_empty == True:
            return None
    else:
        left_child = remove_empty_cuts(tree.left, out_file)
        right_child = remove_empty_cuts(tree.right, out_file)

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
    print "In clean up. Here is the tree:"
    print_eg_tree(tree)

    # First clean up double cuts from the entire tree
    print "Removing double cuts from tree..."
    update_tree = remove_dc_from_tree(tree, out_file)

    print "Tree without double cuts:"
    print_eg_tree(update_tree)

    # Second look for empty cuts in a set of children and if at least one is found
    # then remove the parent and all of its children
    print "Removing empty cuts from tree..."
    update_tree = remove_empty_cuts(update_tree, out_file)
    print "Tree without empty cuts:"
    print_eg_tree(update_tree)

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
    if eg_tree == None:
        print "EG_CONS: In case 1."
        sys.exit("Inconsistent premises and goal! Exiting...")
    # If the only thing that is left on the sheet of assignment is an empty cut,
    # then return an empty cut and end the function
    # Can ignore whether or not we have sheet of assignment - the root should be considered an EGEmptyCut or EGNegation with 0 children
    elif isinstance(eg_tree, EGEmptyCut) or \
        (isinstance(eg_tree, EGNegation) and eg_tree.child == None):
        print "EG_CONS: In case 2. This is the tree: "
        print_eg_tree(eg_tree)
        return EGEmptyCut()
    # Case if left with a negation of an and with a literal and a blob of stuff
    # Remove the literal from the blob and call eg_cons on it after clean up
    # If not in this structure, then assumed that something went wrong, and program terminates
    elif isinstance(eg_tree, EGNegation) and isinstance(eg_tree.child, EGAnd):
        print "EG_CONS: In case 3.  This is the tree: "
        print_eg_tree(eg_tree)
        old_child = eg_tree
        if isinstance(old_child, EGNegation) and isinstance(old_child.child, EGAnd):
            if old_child.child.num_children == 2:
                if isinstance(old_child.child.children[0], EGAtom) or \
                    (isinstance(old_child.child.children[0], EGNegation) and \
                    isinstance(old_child.child.children[0].child, EGAtom)):
                    # The atom is on the first child, so remove from the entire tree
                    temp = remove_literal(old_child.child.children[0], old_child.child.children[1], out_file)
                    temp = cleanup(temp, out_file)
                    eg_tree.child.replace_child(temp, 1)
                    return eg_cons(eg_tree.child.children[1], out_file)
                elif isinstance(old_child.child.children[1], EGAtom) or \
                    (isinstance(old_child.child.children[1], EGNegation) and \
                    isinstance(old_child.child.children[1].child, EGAtom)):
                    # Do the reverse of above
                    temp = remove_literal(old_child.child.children[1], old_child.child.children[0], out_file)
                    temp = cleanup(temp, out_file)
                    eg_tree.child.replace_child(temp, 0)
                    return eg_cons(eg_tree.child.children[0], out_file)
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
    # Should assume that theres always some kind of AND at the base of every SA
    # Structure: SA
    #            |
    #           SA
    #          /  \
    #        NEG  BLOB
    #         |     |
    #        SA    {}
    elif (isinstance(eg_tree, SheetAssignment) and eg_tree.num_children == 1 and isinstance(eg_tree.children[0], EGAnd)) \
        or (isinstance(eg_tree, EGAnd) and eg_tree.num_children == 2):
        print "EG_CONS: In case 4.  Current tree:"
        print_eg_tree(eg_tree)
        if isinstance(eg_tree, SheetAssignment):
            new_root = eg_tree.children[0] # Should be EGAnd
        elif isinstance(eg_tree, EGAnd):
            # print "HERE"
            new_root = eg_tree
        else:
            print_eg_tree(eg_tree)
            sys.exit("Something went wrong in case 4 of eg_cons...")

        # Check if the premises are on the left side
        premise_index = 0
        premise_index = 1
        if isinstance(new_root.children[0], EGNegation) and (isinstance(new_root.children[0].child, EGAnd) \
            or isinstance(new_root.children[0].child, EGAtom)):
            premise_index = 0
            blob_index = 1
        elif isinstance(new_root.children[1], EGNegation) and (isinstance(new_root.children[1].child, EGAnd) \
            or isinstance(new_root.children[1].child, EGAtom)):
            premise_index = 1
            blob_index = 0
        else:
            print_eg_tree(eg_tree)
            sys.exit("Incorrectly formatted tree for the 4th case in eg_cons!")

        print "Premises:"
        premises = new_root.children[premise_index] # Set it equal to the negation of the AND
        print_eg_tree(premises)
        # print premises
        print "Blob:"
        blob = new_root.children[blob_index]
        print_eg_tree(blob)
        # Double cut all premises and iterate the blob into the outer level of each double cut
        i = 0
        if isinstance(premises, EGNegation) and isinstance(premises.child, EGAtom):
            temp = premises
            dc_child = node_of_cut_to_add(temp)
            print "Added double cut:"
            print_eg_tree(dc_child)
            temp2 = iterate(dc_child, blob)
            print "Finished child:"
            print_eg_tree(temp2)
            temp = temp2
            print "Added DC and blob:"
            print_eg_tree(temp)
            # Link back up to the original tree
            premises.replace_child(temp)

        while i < premises.child.num_children and not isinstance(premises, EGNegation):
            # print "Child:"
            # print premises.child.children[i]
            if i < 0:
                i = 0
            # Not sure why there's just a None child in the list of premises - need to check if that's right
            if premises.child.children[i] != None:
                # For the inner and representing the original premises
                # Remember to double cut the goal which is outside of this and bc it's treated as another premise
                # At the moment the blob and the negated goal are identical but still need to iterate
                temp = premises.child.children[i]
                # print "This is temp"
                # print temp
                # print_eg_tree(temp)
                prev = None
                # Skip through all the top level and statements to get to the actual premises of the proof
                while isinstance(temp, EGAnd) and temp.num_children == 1:
                    # print "HERE"
                    prev = temp
                    temp = temp.children[0]
                # If there is only one premise, then double cut on just that node
                if not isinstance(temp, EGAnd) and prev != None:
                    temp = prev

                print prev
                # No outer AND or only one level of AND
                if prev == None and not isinstance(temp, EGAnd):
                    dc_child = node_of_cut_to_add(temp)
                    print "Added double cut:"
                    print_eg_tree(dc_child)
                    temp2 = iterate(dc_child, blob)
                    print "Finished child:"
                    print_eg_tree(temp2)
                    temp = temp2
                else:
                    # Base layer AND statement found, now double cut all premises
                    for j in range(0, temp.num_children):
                        # Double cut all the original premises
                        dc_child = node_of_cut_to_add(temp.children[j])
                        print "Added double cut:"
                        print_eg_tree(dc_child)
                        # Insert the blob to the outer layer of each double cut
                        temp2 = iterate(dc_child, blob)
                        print "Finished child:"
                        print_eg_tree(temp2)
                        temp.replace_child(temp2, j)
                print "Added DC and blob:"
                print_eg_tree(temp)
                # Link back up to the original tree
                premises.child.replace_child(temp, i)
                i += 1
            else:
                premises.child.remove_child(i)
                i -= 1
        print "Completed updating all premises:"
        print_eg_tree(premises.child)

        # Erase the outer blob
        new_root.remove_child(blob_index)
        print "Removed the outer blob: "
        print_eg_tree(new_root)

        if premise_index == 1:
            premise_index = 0

        # Replace the old children with updated ones (have the dc and blob)
        new_root.replace_child(premises, premise_index)
        print "Replaced old children: "
        print_eg_tree(new_root)

        # Clean up each child and run eg_cons on each premise
        for i in range(0, premises.child.num_children):
            if isinstance(premises.child.children[i], EGAnd):
                # Make sure to loop through individual premises and call recursively
                for j in range(0, premises.child.children[i].num_children):
                    temp_child = cleanup(premises.child.children[i].children[j], out_file)
                    return eg_cons(temp_child, out_file) # Hopefully will terminate -> should just return an empty cut
            else:
                temp_child = cleanup(premises.child.children[i], out_file)
                return eg_cons(temp_child, out_file) # Hopefully will terminate -> should just return an empty cut
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

    lst = []
    lst.append(setup_tree.children[1].child)
    inner_SA = SheetAssignment(1, lst)

    print "This is inner SA:"
    print_eg_tree(inner_SA)

    # Run consistency algorithm to determine proof
    final_tree = eg_cons(inner_SA, out_file)

    print "Completed proof... Here is final tree:"
    print final_tree
    print_eg_tree(final_tree)
