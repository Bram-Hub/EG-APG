from parse_tree import parse_sentence
from statement import *
from existential_statement import *

# TODO: Figure out if we should pass in the entire tree or just the parent of
# what needs to be double cutted -> essentially how do we relink up the entire Tree
# NOTE: also another idea to consider: should we have a parent attribute for
# each statement so that way we can go back and forth between parent and children?
def add_double_cut(root):
    return False

# Pass in the root node of the to be DC structure
# Insert double cut around the specified node
# Returns the modified node that contains the DC around it
# Handle merging with parent on the outside
# Should be able to insert a double cut around anything
def node_of_cut_to_add(node_to_dc):
    inner_neg = EGNegation(node_to_dc)
    outer_neg = EGNegation(inner_neg)
    return outer_neg

# Pass in the parent of the node that is the outer layer of the DC
# Will remove an double cuts present in the children
# Returns the modified parent that no longer contains the double cut
def node_of_cut_to_rm(parent):
    # Should not ever pass in an atom or empty cut statement as they will never
    # have double cuts
    if not isinstance(parent, EGAtom) or not isinstance(parent, EGEmptyCut):
        # In both of these cases, each child could potentially contain a double cut
        if isinstance(parent, EGAnd) and isinstance(parent, SheetAssignment):
            children = parent.children
            for i in range(0, len(children)):
                child = children[i]
                # Check if the child is a negation statement (outer cut)
                if isinstance(child, EGNegation):
                    # Check if the child's child is a negation statement (inner cut)
                    if isinstance(child.child, EGNegation):
                        new_child = child.child.child # Save whatever is inside the double cut
                        parent.replace_child(new_child, i) # By moving the child, should be removing the DC
        elif isinstance(parent, EGNegation):
            child = parent.child
            # Check if the Negation contains a DC as children
            if isinstance(child, EGNegation):
                if isinstance(child, EGNegation):
                    new_child = child.child.child
                    parent.replace_child(new_child)
        else:
            left_child = parent.left
            right_child = parent.right
            # Check left child for DC
            if isinstance(left_child, EGNegation):
                if isinstance(left_child.child, EGNegation):
                    new_child = left_child.child.child
                    parent.left.replace_left_child(new_child)
            if isinstance(right_child, EGNegation):
                if isinstance(left_child.child, EGNegation):
                    new_child = right_child.child.child
                    parent.right.replace_right_child(new_child)
    return parent

# Pass in the parent (root) of the node of where to insert the iteration and the thing to iterate
# Iteration is basically like ANDing statements together
# Returns the modified parent with the iterated statement as a child
# Parent should not be an atom or empty cut (no children)
def iterate(parent, to_iterate):
    # If it's an AND statement or the sheet of assignment
    if isinstance(parent, EGAnd) or isinstance(parent, SheetAssignment):
        parent.add_children(to_iterate)
    # Can't iterate anything into an atom or empty cut
elif not isinstance(parent, EGAtom) and not isinstance(parent, EGEmptyCut):
        # If it's already a negation, just make sure the child is an and statement
        if isinstance(parent, EGNegation):
            if not isinstance(parent.child, EGAnd):
                old_child = parent.child
                children = []
                children.append(old_child)
                parent.replace_child(EGAnd(1, children))
                parent.child.add_children(to_iterate)
            else:
                parent.child.add_children(to_iterate)
        # If it's not a negation, convert and make children into an and statement
        else:
            old_children = []
            old_children.append(parent.left_child)
            old_children.append(parent.right_child)

            new_child = EGAnd(2, old_children)
            new_child.add_children(to_iterate)
            parent = EGNegation(new_child)
    return parent

# Usage note: if attempting to deiterate on an OR, IMPLICATION, BICONDITIONAL
# statement, then pass in a '0' for the left child or a '1' for the right child
# Assumes that determining the correct child has been figured out already
# Note that if deiterating in something that does not resemble an AND-like
# structure, means that the child will be replaced with a None object
# Removes the child from the parent's list of children
# Returns the modified parent with the specified child deiterated
def deiterate(parent, index_of_child_to_deiterate):
    # If it's just an AND-like statement, then just remove the specified child
    if isinstance(parent, EGAnd) or isinstance(parent, SheetAssignment):
        parent.remove_child(index_of_child_to_deiterate)
    # Cannot deiterate from an atom or empty cut statement
    elif not isinstance(parent, EGAtom) or not isinstance(parent, EGEmptyCut):
        # First check if it's a negation statement
        if isinstance(parent, EGNegation):
            if isinstance(parent.child, EGAnd):
                parent.child.remove_child(index_of_child_to_deiterate)
            else:
                # If it's a negation of anything else, just erase everything
                parent.replace_child(None)
        else:
            try:
                # If it's an OR, IMP, or BICON, then determine which child to remove
                if index_of_child_to_deiterate == 0:
                    parent.replace_left_child(None)
                elif index_of_child_to_deiterate == 1:
                    parent.replace_right_child(None)
                break
            except ValueError:
                print "Incorrect indices for left or right child!"
    return parent
