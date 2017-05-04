# Contains the main and helper functions used to generate proofs for Existential Graphs

from existential_statement import *
from rules import *
import sys

def remove_inside_of_neg_literal_replace_with_empty_cut(literal, tree, out_file):
    assert ( isinstance(literal, EGNegation) and isinstance(literal.child, EGAtom) )

    if isinstance(tree, EGEmptyCut) or tree == None:
        return tree
    # Case B: Base Case 2
    elif isinstance(tree, EGAtom):
        # print "GOT TO ATOM"
        if compare_EG_trees(tree, literal.child):
            # print "COMPARE TRUE"
            return EGEmptyCut()
    # Case B: Base Case 3
    elif isinstance(tree, EGNegation):
        # print "SHOULD BE HERE"
        # print_eg_tree(tree)
        only_child = remove_inside_of_neg_literal_replace_with_empty_cut(literal, tree.child, out_file)
        if only_child == None:
            # print "RETURNING EMPTY CUT"
            return EGEmptyCut()
        else:
            return EGNegation(only_child)
    # Case B: Base Case 4
    elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
        # print "gotem"
        new_children = []
        # for each child, apply remove_inside_of_neg_literal_replace_with_empty_cut recursively
        for i in range(0, tree.num_children):
            new_child = remove_inside_of_neg_literal_replace_with_empty_cut(literal, tree.children[i], out_file)

            # print "THIS IS THE NEW CHILD"
            # print_eg_tree(new_child)
            if new_child != None:
                # print "adding new kid: ", new_child
                new_children.append(new_child)
        # print "THIS IS THE NEW CHILDREN"
        # print new_children
        temp = EGAnd(len(new_children), new_children)
        print "this is what removing the inside of the neg literal replaced with emty cut looks like:"
        print_eg_tree(temp)
        # return EGAnd(len(new_children), new_children)
        return temp
    # Case B: Everything else Case
    else:
        print "everything else!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        if not (isinstance(tree, EGOr) or \
            isinstance(tree, EGImp) or \
            isinstance(tree, EGBicon)):
            print type(tree)
        else:
            # if not catched above, the tree must be an Or, Implication or Biconditional
            assert( isinstance(tree, EGOr) or \
                isinstance(tree, EGImp) or \
                isinstance(tree, EGBicon))
        # grab the left and right child after remove literal on them
        left_child = remove_inside_of_neg_literal_replace_with_empty_cut(literal, tree.left, out_file)
        right_child = remove_inside_of_neg_literal_replace_with_empty_cut(literal, tree.right, out_file)
        # Automatically convert representation to a negation of an AND
        # Only make it a chile, if it isn't None
        if left_child != None:
            old_children.append(left_child)
        if right_child != None:
            old_children.append(right_child)
        new_child = EGAnd(len(old_children), old_children)
        tree = EGNegation(new_child)
    return tree




####################################################################################################################################
####################################################################################################################################


# Helper function - removes any literal that matches the specified literal
def remove_literal(literal, tree, out_file):
    print "heres the literal"
    print_eg_tree(literal)
    assert( isinstance(literal, EGAtom) or (isinstance(literal, EGNegation) and isinstance(literal.child, EGAtom) ) )
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
    # print "THIS IS THE LITERAL"
    # print_eg_tree(literal)
    # Case A: when literal is a negation
    if isinstance(literal, EGNegation):
        #asser that the literal is a literal (the negation should have an atom as a child)
        print "unioeqefdsf", literal.child
        assert (isinstance(literal.child, EGAtom))
        # Hack to move complement of atom to the end of the list of children
        # print "DON'T WANT COMPLEMENT"
        # print_eg_tree(tree)

        tree = remove_inside_of_neg_literal_replace_with_empty_cut(literal, tree, out_file)

        # new_literal = tree.children[0]
        # print "new literallllll: ", new_literal
        # print "len: ", len(new_literal.child.children)
        # print "new literalllll's child's child: ", new_literal.child.children[0]
        # tree.remove_child(0)
        # tree.add_children(literal)
        # # print "MOVED TO END"
        # # print_eg_tree(tree)
        # tree = remove_literal(new_literal, tree, out_file)

        # Case A: Base Case 1
        # if isinstance(tree, EGAtom) or isinstance(tree, EGEmptyCut):
        #     return tree
        # # Case A: Base Case 2
        # elif isinstance(tree, EGNegation):
        #     if ( isinstance(tree.child, EGAtom) ):
        #         if compare_EG_trees(tree, literal):
        #             return None
        #         else:
        #             return tree
        # # Case A: Base Case 3
        # elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
        #     new_children = []
        #     # for each child, apply remove_literal recursively
        #     for i in range(0, tree.num_children):
        #         new_children.append(remove_literal(literal, tree.children[i], out_file))
        #     return EGAnd(len(new_children), new_children)
        # # Case A: Everything else Case
        # else:
        #     # if not catched above, the tree must be an Or, Implication or Biconditional
        #     assert( isinstance(tree, EGOr) or \
        #         isinstance(tree, EGImplication) or \
        #         isinstance(tree, EGBiconditional))
        #     # grab the left and right child after remove literal on them
        #     left_child = remove_literal(tree.left, out_file)
        #     right_child = remove_literal(tree.right, out_file)
        #     # Automatically convert representation to a negation of an AND
        #     # Only make it a chile, if it isn't None
        #     if left_child != None:
        #         old_children.append(left_child)
        #     if right_child != None:
        #         old_children.append(right_child)
        #     new_child = EGAnd(len(old_children), old_children)
        #     tree = EGNegation(new_child)

    # Case B: when literal is an Atom
    else:
        # print "heeyyooo here"
        # Case B: Base Case 1
        if isinstance(tree, EGEmptyCut) or tree == None:
            return tree
        # Case B: Base Case 2
        elif isinstance(tree, EGAtom):
            # print "GOT TO ATOM"
            if compare_EG_trees(tree, literal):
                # print "COMPARE TRUE"
                return None
        # Case B: Base Case 3
        elif isinstance(tree, EGNegation):
            # print "SHOULD BE HERE"
            # print_eg_tree(tree)
            only_child = remove_literal(literal, tree.child, out_file)
            if only_child == None:
                # print "RETURNING EMPTY CUT"
                return EGEmptyCut()
            else:
                return EGNegation(only_child)
        # Case B: Base Case 4
        elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
            # print "gotem"
            new_children = []
            # for each child, apply remove_literal recursively
            for i in range(0, tree.num_children):
                new_child = remove_literal(literal, tree.children[i], out_file)

                # print "THIS IS THE NEW CHILD"
                # print_eg_tree(new_child)
                if new_child != None:
                    # print "adding new kid: ", new_child
                    new_children.append(new_child)
            # print "THIS IS THE NEW CHILDREN"
            # print new_children
            temp = EGAnd(len(new_children), new_children)
            print_eg_tree(temp)
            # return EGAnd(len(new_children), new_children)
            return temp
        # Case B: Everything else Case
        else:
            print "everything else!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            if not (isinstance(tree, EGOr) or \
                isinstance(tree, EGImp) or \
                isinstance(tree, EGBicon)):
                print type(tree)
            else:
                # if not catched above, the tree must be an Or, Implication or Biconditional
                assert( isinstance(tree, EGOr) or \
                    isinstance(tree, EGImp) or \
                    isinstance(tree, EGBicon))
            # grab the left and right child after remove literal on them
            left_child = remove_literal(literal, tree.left, out_file)
            right_child = remove_literal(literal, tree.right, out_file)
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
# Printing in Pegasus output can also just print a line with no actual changes if no double cuts are present
def remove_dc_from_tree(tree, out_file):
    before_tree = None
    after_tree = None
    # Base Case - if an atom or empty cut, just return it
    if isinstance(tree, EGAtom) or isinstance(tree, EGEmptyCut) or tree == None:
        return tree
    # Base Case 2 - if a negation statement, then check to see if any double cuts can be removed
    elif isinstance(tree, EGNegation):
        before_tree = copy_tree(tree)
        tree = node_of_cut_to_rm(tree, 0)
        # If it stayed as a negation then just check its child for dc
        if isinstance(tree, EGNegation):
            tree.replace_child(remove_dc_from_tree(tree.child, out_file))
            if isinstance(tree.child, EGAnd) and tree.child.num_children == 1 and isinstance(tree.child.children[0], EGNegation):
                tree = tree.child.children[0].child
            elif isinstance(tree.child, EGNegation):
                tree = tree.child.child
            # Want to avoid small sub trees of the entire tree when printing in Pegasus format, so print after all recursive calls
            # Draw back is that there can be multiple double cuts removed that will be reflected in a single line
            after_tree = copy_tree(tree)
            write_to_file(out_file, "DC", before_tree, after_tree)
        # If it was altered and no longer a negation, then check if the new structure contains any double cuts
        else:
            tree = remove_dc_from_tree(tree, out_file)
            after_tree = copy_tree(tree)
            write_to_file(out_file, "DC", before_tree, after_tree)
    elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
        i = 0
        before_tree = copy_tree(tree)
        while i < tree.num_children:
            # Update the parent, which is an SA or AND statement, with all the children with no double cuts
            to_replace = remove_dc_from_tree(tree.children[i], out_file)
            if to_replace == None:
                tree.remove_child(i)
                after_tree = copy_tree(tree)
                write_to_file(out_file, "DC", before_tree, after_tree)
                i -= 1
            else:
                tree.replace_child(to_replace, i)
                after_tree = copy_tree(tree)
                write_to_file(out_file, "DC", before_tree, after_tree)
                i += 1
        if isinstance(tree, EGAnd):
            if tree.num_children == 1:
                tree = tree.children[0]
    else:
        before_tree = copy_tree(tree)

        left_child = remove_dc_from_tree(tree.left, out_file)
        right_child = remove_dc_from_tree(tree.right, out_file)

        # Automatically convert representation to a negation of an AND
        old_children = [left_child, right_child]
        new_child = EGAnd(2, old_children)
        tree = EGNegation(new_child)
        after_tree = copy_tree(tree)
        # For current implement, a single line will show multiple changes happening at once
        write_to_file(out_file, "DC", before_tree, after_tree)
    # print "Here is the result: "
    # print tree
    # assert(tree != None)
    return tree

# Helper function - check if there are any empty cuts in a subtree and remove that subtree
# Idea is that only the immediate parent of the empty cut gets removed (entire structure)
# but that's it
# Is the action considered a removal of a double cut or just an erase
def remove_empty_cuts(tree, level, out_file):
    before_tree = copy_tree(tree)
    after_tree = copy_tree(tree)

    # Base case:  tree is the empty cut or an atom
    if isinstance(tree, EGEmptyCut) or isinstance(tree, EGAtom) or tree == None:
        return tree
    elif isinstance(tree, EGNegation):
        result = remove_empty_cuts(tree.child, level+1, out_file)
        if result == None:
            tree.replace_child(None)
        elif isinstance(result, EGEmptyCut):
            return None
        else:
            tree.replace_child(result)
    elif isinstance(tree, SheetAssignment) or isinstance(tree, EGAnd):
        found_empty = False
        i = 0
        while i < tree.num_children:
            result = remove_empty_cuts(tree.children[i], level+1, out_file)
            # Got rid of an empty cut from a subtree
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
        elif level == 0 and found_empty == True:
            for i in range(0, tree.num_children):
                if not isinstance(tree.children[i], EGEmptyCut):
                    tree.remove_child(i)
    else:
        left_child = remove_empty_cuts(tree.left, level+1, out_file)
        right_child = remove_empty_cuts(tree.right, level+1, out_file)

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
    # First clean up double cuts from the entire tree
    print "CLEANUP: THIS IS THE TREE"
    print_eg_tree(tree)
    update_tree = remove_dc_from_tree(tree, out_file)
    print "CLEANUP: REMOVED DOUBLE CUTS"
    print_eg_tree(update_tree)

    # Second look for empty cuts in a set of children and if at least one is found
    # then remove the parent and all of its children
    update_tree = remove_empty_cuts(update_tree, 0, out_file)
    # print "CLEANUP: REMOVED EMPTY"

    return update_tree

def write_to_file(out_file, rule, before, after):
    before_str = to_string_tree(before)
    after_str = to_string_tree(after)
    out_file.write("%s:%s => %s\n" % (rule, before_str, after_str))

# Converts the premises tree into the format needed for conducting the proof
# Also includes the setup files in the output file
def setup(premises, goal, out_file):
    # Variables below how the before and after states of the tree to print in Pegasus format
    before_tree = copy_tree(premises)
    after_tree = copy_tree(premises)

    # First add an empty double cut onto the sheet of assignment
    empty_dc = node_of_cut_to_add(None)
    try:
        if isinstance(premises, SheetAssignment):
            premises.add_children(empty_dc)
    except ValueError:
        print "Incorrect format for the premises existential graph tree!"

    # print "Added empty double cut: "
    # print_eg_tree(premises)
    after_tree = copy_tree(premises)
    write_to_file(out_file, "DC", before_tree, after_tree)

    # Insert the negation of the goal into the outer level of the double cut
    negate_goal = EGNegation(goal.children[0])
    # print "This is the negated goal:"
    # print_eg_tree(negate_goal)
    before_tree = copy_tree(premises)
    # Based on what was done above, the empty dc should be the last child on the sheet of assignment
    temp = iterate(premises.children[premises.num_children-1], negate_goal)
    premises.replace_child(temp, premises.num_children-1)
    after_tree = premises
    # print "Inserted the negation of goal:"
    # print_eg_tree(premises)
    write_to_file(out_file, "IT", before_tree, after_tree)

    # Iterate the premises and complement of the goal into the inner level of the double cut
    if isinstance(premises.children[1], EGNegation):
        if isinstance(premises.children[1].child, EGAnd):
            p = premises.children[0]
            before_tree = copy_tree(premises)
            temp = iterate(premises.children[premises.num_children-1].child.children[0], p)
            premises.children[premises.num_children-1].child.replace_child(temp, 0)
            after_tree = copy_tree(premises)
            write_to_file(out_file, "IT", before_tree, after_tree)

            before_tree = copy_tree(premises)
            temp = iterate(premises.children[premises.num_children-1].child.children[0], negate_goal)
            premises.children[premises.num_children-1].child.replace_child(temp, 0)
            after_tree = copy_tree(premises)
            write_to_file(out_file, "IT", before_tree, after_tree)
            # print "Inserted the negation of goal and premises:"
            # print_eg_tree(premises)
    else:
        sys.exit("Incorrectly formatted tree!")

    return premises

# boolean function that tells you if we should do case 3.
def figure_out_if_we_should_do_case_3(tree):
    # Skip all the ANDs to the last ones
    previous = None
    better_root = tree
    while isinstance(better_root, EGAnd) and better_root.num_children == 1:
        previous = better_root
        better_root = better_root.children[0]
    if previous != None:
        better_root = previous

    if isinstance(better_root, EGAnd):
        for child in better_root.children:
            if isinstance(child, EGAtom) or (isinstance(child, EGNegation) and isinstance(child.child, EGAtom)):
                print "************** ******************* ************* **********GOT A CASE 3"
                return True
    return False

# Consistency checker - evaluates if all the given premises and complement of the
# goal are consistent with one another -> will also generate the proof in the
# output file that can be loaded into Pegasus
def eg_cons(eg_tree, out_file):
    do_case_3 = figure_out_if_we_should_do_case_3(eg_tree)
    # Assumption of program (for now) is that the proof provided is valid
    # If after clean up, None is returned then that means the premises and goal
    # aren't consistent
    if eg_tree == None:
        # print "EG_CONS: In case 1."
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
    # DEBUG THIS CASE - ONLY CONSIDER ATOMS NOT NEGATION OF ATOMS
    elif (isinstance(eg_tree, EGNegation) and isinstance(eg_tree.child, EGAnd)) or do_case_3:
        print "EG_CONS: In case 3.  This is the tree: "
        print_eg_tree(eg_tree)
        old_child = eg_tree
        if do_case_3:
            # Skip all the ANDs to the last ones
            previous = None
            better_root = eg_tree
            while isinstance(better_root, EGAnd) and better_root.num_children == 1:
                previous = better_root
                better_root = better_root.children[0]
            if previous != None:
                better_root = previous

            things_to_work_with = better_root

        elif old_child.child.num_children >= 2:
            things_to_work_with = old_child.child
        else:
            print_eg_tree(eg_tree)
            sys.exit("Not enough children for this case for eg_cons!")

        no_literal_found = False
        literal = None
        list_of_blob = []
        for i,potential_literal in enumerate(things_to_work_with.children):
            if potential_literal == None:
                pass
            # If you see another AND statement, search through for thing to reduce on
            if isinstance(potential_literal, EGAnd):
                for j in range(0, potential_literal.num_children):
                    if potential_literal.children[j] == None:
                        pass
                    if isinstance(potential_literal, EGAtom):
                        literal = potential_literal.children[j]
                        no_literal_found = True
                    else:
                        list_of_blob.append(potential_literal.children[j])
            elif isinstance(potential_literal, EGBicon) or isinstance(potential_literal, EGImp) or isinstance(potential_literal, EGOr):
                if no_literal_found == False:
                    if isinstance(potential_literal.left, EGAtom):

                        # The left side of a biconditional should always be an implication
                        literal = potential_literal.left
                        no_literal_found = True
                        list_of_blob.append(potential_literal.right)
                    else:
                        assert (isinstance(potential_literal.right, EGAtom))

                        # The right side of a biconditional should always be an implication
                        literal = potential_literal.right
                        no_literal_found = True
                        list_of_blob.append(potential_literal.left)

                else:
                    list_of_blob.append(potential_literal.left)
                    list_of_blob.append(potential_literal.right)
            elif isinstance(potential_literal, EGAtom):
                if no_literal_found == False:
                    literal = potential_literal
                    # no_literal_found = True
                else:
                    list_of_blob.append(potential_literal)
            elif potential_literal == None:
                pass
            elif isinstance(potential_literal, EGNegation):
                if isinstance(potential_literal.child, EGAtom) or \
                        (isinstance(potential_literal.child, EGNegation) and \
                        isinstance(potential_literal.child.child, EGAtom)):
                    if no_literal_found == False:
                        literal = potential_literal
                        # no_literal_found = True
                    else:
                        list_of_blob.append(potential_literal)
                else:
                    list_of_blob.append(potential_literal)
            else:
                print "should be asesrting 0 next: ", potential_literal
                assert(0)

        if no_literal_found:
            print_eg_tree(eg_tree)
            sys.exit("Missing a literal for this case for eg_cons!")

        # And everything else together to make a blob
        blob = EGAnd(len(list_of_blob), list_of_blob)

        print "EG CONS CASE 3: THIS IS OLD BLOB"
        print_eg_tree(blob)

        assert(blob.num_children > 0)
        assert(literal != None)


        # Located the literal and the blob

        print "Removing literal from the blob:"
        print_eg_tree(literal)
        # ++ if (literal == None):

        new_blob = remove_literal(literal, blob, out_file)
        print "No more literals:"
        print_eg_tree(new_blob)
        new_blob = EGNegation(new_blob)
        print "Re-negated no more literals tree"
        print_eg_tree(new_blob)
        new_blob = cleanup(new_blob, out_file)
        # eg_tree.child.replace_child(new_blob, 1) // isgnored because not sure of strcture
        # print "EG CONS CASE 3: THIS IS LITERAL"
        # print_eg_tree(literal)
        print "EG CONS CASE 3: THIS IS THE NEW BLOB"
        print_eg_tree(new_blob)
        return eg_cons(new_blob, out_file)

        # else:
        #     print_eg_tree(eg_tree)
        #     sys.exit("Incorrectly formatted tree for the 3rd case in eg_cons!")
    # Case if there are 2 or more premises remaining, then setup all of the premises,
    # run the clean up function on it, then call eg_cons on each of the remaining premises
    # Should assume that theres always some kind of AND at the base of every SA
    elif (isinstance(eg_tree, SheetAssignment) and eg_tree.num_children == 1 and isinstance(eg_tree.children[0], EGAnd)) \
        or (isinstance(eg_tree, EGAnd) and eg_tree.num_children >= 2):
        print "EG_CONS: In case 4.  Current tree:"
        print_eg_tree(eg_tree)
        if isinstance(eg_tree, SheetAssignment):
            new_root = eg_tree.children[0] # Should be EGAnd
        elif isinstance(eg_tree, EGAnd):
            # print "HERE"
            new_root = eg_tree # Top of the tree passed in
        else:
            print_eg_tree(eg_tree)
            sys.exit("Something went wrong in case 4 of eg_cons...")

        # Skip all the ANDs to the last ones
        previous = None
        temporary = new_root
        while isinstance(temporary, EGAnd) and temporary.num_children == 1:
            previous = temporary
            temporary = temporary.children[0]
        if previous != None:
            temporary = previous

        # Find the sub tree to reduce on and the "blob"
        list_of_blob = []
        to_reduce = None
        found_to_reduce = False
        for i in range(0, temporary.num_children):
            # If you see another AND statement, search through for thing to reduce on
            if isinstance(temporary.children[i], EGAnd):
                for j in range(0, temporary.children[i].num_children):
                    if temporary.children[i].children[j] == None:
                        pass
                    if temporary.children[i].children[j].value == "()" and found_to_reduce == False:
                        to_reduce = temporary.children[i].children[j]
                        found_to_reduce = True
                    else:
                        list_of_blob.append(temporary.children[i].children[j])
            elif isinstance(temporary.children[i], EGBicon):
                if found_to_reduce == False:
                    # The left side of a biconditional should always be an implication
                    to_reduce = temporary.children[i].left
                    list_of_blob.append(temporary.children[i].right)
                    found_to_reduce = True
                else:
                    list_of_blob.append(temporary.children[i].left)
                    list_of_blob.append(temporary.children[i].right)
            elif isinstance(temporary.children[i], EGAtom):
                list_of_blob.append(temporary.children[i])
            elif temporary.children[i] == None:
                pass
            else:
                if found_to_reduce == False:
                    to_reduce = temporary.children[i]
                    found_to_reduce = True
                else:
                    list_of_blob.append(temporary.children[i])

        # print "EG CONS CASE 4: THIS IS THE THING TO REDUCE ON"
        # print_eg_tree(to_reduce)
        # And everything else together to make a blob
        blob = EGAnd(len(list_of_blob), list_of_blob)
        # print "EG CONS CASE 4: THIS IS THE BLOB"
        # print_eg_tree(blob)

        assert(blob.num_children > 0)
        assert(to_reduce != None)

        # Double cut each child of the thing to reduce on and iterate the blob into each child
        # If it's a negation of an ANDs
        if isinstance(to_reduce.child, EGAnd):
            for i in range(0, to_reduce.child.num_children):
                # First double cut each child - dc_child will point to the outer layer of the double cut
                dc_child = node_of_cut_to_add(to_reduce.child.children[i])
                # Second iterate the blob into the outer child
                dc_child = iterate(dc_child, blob)
                dc_child = cleanup(dc_child, out_file)
                print "EG CONS CASE 4: THIS IS THE TREE BEFORE CALLING EG CONS"
                print_eg_tree(dc_child.child)
                return eg_cons(dc_child.child, out_file)
        elif isinstance(to_reduce.child, EGAtom) or isinstance(to_reduce.child, EGEmptyCut):
            dc_child = node_of_cut_to_add(to_reduce.child)
            dc_child = iterate(dc_child, blob)
            dc_child = cleanup(dc_child, out_file)
            print "EG CONS CASE 4: THIS IS THE TREE BEFORE CALLING EG CONS"
            print_eg_tree(dc_child.child)
            return eg_cons(dc_child.child, out_file)
        else:
            dc_child_left = node_of_cut_to_add(to_reduce.child.left)
            dc_child_left = iterate(dc_child_left, blob)
            dc_child_left = cleanup(dc_child_left, out_file)

            # Can stop early if an empty cut is found
            if isinstance(eg_cons(dc_child_left.child, out_file), EGEmptyCut):
                return EGEmptyCut()

            dc_child_right = node_of_cut_to_add(to_reduce.child.right)
            dc_child_right = iterate(dc_child_right, blob)
            dc_child_right = cleanup(dc_child_right, out_file)
            print "EG CONS CASE 4: THIS IS THE TREE BEFORE CALLING EG CONS"
            print_eg_tree(dc_child_right.child)
            return eg_cons(dc_child_right.child, out_file)
    else:
        print_eg_tree(eg_tree)
        sys.exit("Incorrectly formatted tree for eg_cons!")

# Main function for finding a proof with the given premises and goal
# Takes in a tree of all the premises combined into a single eg tree and the
# goal as an eg tree
def find_proof(premises, goal, out_file):
    print

    before_tree = None
    after_tree = None

    print "Provided premises:"
    print_eg_tree(premises)
    print "Provided goal:"
    print_eg_tree(goal)

    # Run setup on premises
    setup_tree = setup(premises, goal, out_file)

    print "This is the setup tree: "
    print_eg_tree(setup_tree)

    # Currently will jump to the sub tree in Pegasus output
    lst = []
    lst.append(setup_tree.children[1].child.children[0].child)
    inner_SA = SheetAssignment(1, lst)

    print "This is the subtree used for consisency checking:"
    print_eg_tree(inner_SA)
    print_tree_pegasus_style(inner_SA)

    # Run consistency algorithm to determine proof
    inner_SA = cleanup(inner_SA, out_file)
    print "THIS IS INNER SA:"
    print_eg_tree(inner_SA)
    print_tree_pegasus_style(inner_SA)
    cons_tree = eg_cons(inner_SA, out_file)

    print "Completed eg_cons... Here is the tree:"
    print_eg_tree(cons_tree)

    # print "Inserting results:"
    before_tree = copy_tree(setup_tree)
    setup_tree.children[1].child.children[0].replace_child(cons_tree)
    # print_eg_tree(setup_tree)
    after_tree = copy_tree(setup_tree)
    write_to_file(out_file, "IT", before_tree, after_tree)

    # print "Removing original premises:"
    before_tree = copy_tree(setup_tree)
    setup_tree.remove_child(0)
    # print_eg_tree(setup_tree)
    after_tree = copy_tree(setup_tree)
    write_to_file(out_file, "ER", before_tree, after_tree)

    # print "Remove double cuts on tree:"
    final_tree = remove_dc_from_tree(setup_tree, out_file)
    # print_eg_tree(final_tree)

    print "Reached goal:"
    print_eg_tree(final_tree)

    print "Completed proof searching... Exiting..."
