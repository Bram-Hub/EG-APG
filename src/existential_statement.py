from statement import *
from sys import stdout

class EGStatement(object):
    def __init__(self, value, num_children):
        self._value = value
        self._num_children = num_children

    @property
    def value(self):
        return self._value
    @property
    def num_children(self):
        return self._num_children

    def printTree(self):
        stdout.write(value)

# Root of every Existential Graph Tree is the Sheet of Assertion (SA), so that's
# the default value of a simple statement
# Only takes in a list of children but the value is always "SA"
# Children: >= 0
class SheetAssignment(EGStatement):
    def __init__(self, num_children, children):
        super(SheetAssignment, self).__init__("SA", num_children)
        self._children = children

    @property
    def children(self):
        return self._children
    def add_children(self, new_child):
        self._children.append(new_child)
        self._num_children += 1
    def remove_child(self, child_index):
        del self._children[child_index]
        self._num_children -= 1
    def replace_child(self, new_child, child_index):
        self._children[child_index] = new_child

    def printTree(self):
        for i in range(0, self.num_children):
            if self.children[i] == None:
                stdout.write("()")
            else:
                self.children[i].printTree()

# An atom in the EG tree that only has a value that is a starting
# Children: None
class EGAtom(EGStatement):
    def __init__(self, value):
        super(EGAtom, self).__init__(value, 0)

    def printTree(self):
        stdout.write(self.value + "|")

# An empty cut, or a contradiction, in the EG tree
# Children: None
class EGEmptyCut(EGStatement):
    def __init__(self):
        super(EGEmptyCut, self).__init__("()", 0)

    def printTree(self):
        stdout.write("()")

# A negation is represented by a cut as the value and 1 child
class EGNegation(EGStatement):
    def __init__(self, child):
        super(EGNegation, self).__init__("()", 1)
        self._child = child

    @property
    def child(self):
        return self._child
    def replace_child(self, new_child):
        self._child = new_child

    def printTree(self):
        stdout.write("(")
        if self.child == None:
            stdout.write("()")
        else:
            self.child.printTree()
        stdout.write(")")

# An and statement is represented by the SA as the value and at least 2 children
# Potentially might need a redesign because "inner" SAs need to be removed from the tree
class EGAnd(EGStatement):
    def __init__(self, num_children, children):
        super(EGAnd, self).__init__("SA", num_children)
        self._children = children

    @property
    def children(self):
        return self._children
    def add_children(self, new_child):
        self._children.append(new_child)
        self._num_children += 1
    def remove_child(self, child_index):
        del self._children[child_index]
        self._num_children -= 1
    def replace_child(self, new_child, child_index):
        print_eg_tree(self._children[child_index])
        self._children[child_index] = new_child
        print_eg_tree(self._children[child_index])

    def printTree(self):
        for i in range (0, self.num_children):
            if self.children[i] == None:
                stdout.write("()")
            else:
                self.children[i].printTree()

# A or statement is represented by a cut as the value and 2 children
# Need to figure out how to represent something like: p | q | r | etc.
class EGOr(EGStatement):
    def __init__(self, left, right):
        super(EGOr, self).__init__("()", 2)
        self._left = EGNegation(left) # Make the left child into a EGNegation - will this work?
        self._right = EGNegation(right) # Make the right child into a EGNegation

    @property
    def left(self):
        return self._left
    def replace_left_child(self, new_child):
        self._left = new_child
    @property
    def right(self):
        return self._right
    def replace_right_child(self, new_child):
        self._right = new_child

    def printTree(self):
        stdout.write("(")
        if self.left == None:
            stdout.write("()")
        else:
            self.left.printTree()
        if self.right == None:
            stdout.write("()")
        else:
            self.right.printTree()
        stdout.write(")")

# An implication is represented by a cut and 2 children
class EGImp(EGStatement):
    def __init__(self, left, right):
        super(EGImp, self).__init__("()", 2)
        self._left = left # Can be anything theoretically
        self._right = EGNegation(right) # Change it to an EGNegation

    @property
    def left(self):
        return self._left
    def replace_left_child(self, new_child):
        self._left = new_child
    @property
    def right(self):
        return self._right
    def replace_right_child(self, new_child):
        self._right = new_child

    def printTree(self):
        stdout.write("(")
        if self.left == None:
            stdout.write("()")
        else:
            self.left.printTree()
        if self.right == None:
            stdout.write("()")
        else:
            self.right.printTree()
        stdout.write(")")

# A biconditional is represented by the SA and two children
# Potentially might need a redesign because "inner" SAs need to be removed from the tree
class EGBicon(EGStatement):
    def __init__(self, left, right):
        super(EGBicon, self).__init__("SA", 2)
        self._left = EGImp(left, right) # Should be an EGImp
        self._right = EGImp(right, left) # Should be an EGImp except flipped from the previous one

    @property
    def left(self):
        return self._left
    def replace_left_child(self, new_child):
        self._left = new_child
    @property
    def right(self):
        return self._right
    def replace_right_child(self, new_child):
        self._right = new_child

    def printTree(self):
        if self.left == None:
            stdout.write("()")
        else:
            self.left.printTree()
        if self.right == None:
            stdout.write("()")
        else:
            self.right.printTree()

# Takes a "standard-squashed" tree and converts it into an existential graph
# tree.  Returns the stack - need to add SA root outside
def transform(tree, stack):
    if isinstance(tree, IdStatement):
        stack.append(EGAtom(tree.value))
    elif isinstance(tree, ContradictionStatement):
        stack.append(EGEmptyCut())
    elif isinstance(tree, UnaryStatement):
        transform(tree.child, stack)
        prev_statement = stack.pop()
        stack.append(EGNegation(prev_statement))
    elif isinstance(tree, AndStatement):
        num_children = len(tree.children)
        for i in range(0, num_children):
            transform(tree.children[i], stack)
        count = 0
        and_statement = EGAnd(0, [])
        while count < num_children:
            prev_statement = stack.pop()
            and_statement.add_children(prev_statement)
            count += 1
        stack.append(and_statement)
    elif isinstance(tree, BinaryStatement):
        if tree.value == '|':
            transform(tree.left, stack)
            transform(tree.right, stack)
            prev_right = stack.pop()
            prev_left = stack.pop()
            stack.append(EGOr(prev_left, prev_right))
        elif tree.value == '-':
            transform(tree.left, stack)
            transform(tree.right, stack)
            prev_right = stack.pop()
            prev_left = stack.pop()
            stack.append(EGImp(prev_left, prev_right))
        elif tree.value == '=':
            transform(tree.left, stack)
            transform(tree.right, stack)
            prev_right = stack.pop()
            prev_left = stack.pop()
            stack.append(EGBicon(prev_left, prev_right))
    else:
        print "WARNING: could not understand tree type"
        assert False
    return stack

def print_eg_tree(tree, level=0):
    if isinstance(tree, SheetAssignment):
        # print "level", level, ":", tree.value
        print "\t"*level, tree.value
        for i in range(0, tree.num_children):
            print_eg_tree(tree.children[i], level + 1)
    elif isinstance(tree, EGAnd):
        print "\t"*level, tree.value
        #print tree.children
        for i in range(0, tree.num_children):
            print_eg_tree(tree.children[i], level + 1)
    elif isinstance(tree, EGOr) or isinstance(tree, EGImp) or isinstance(tree, EGBicon):
        # print "level", level, ":", tree.value
        print "\t"*level, tree.value
        print_eg_tree(tree.left, level + 1)
        print_eg_tree(tree.right, level + 1)
    elif isinstance(tree, EGNegation):
        print "\t"*level, tree.value
        print_eg_tree(tree.child, level + 1)
    elif isinstance(tree, EGAtom):
        print "\t"*level, tree.value
        # print "level", level, ":", tree.value
    elif isinstance(tree, EGEmptyCut):
        print "\t"*level, tree.value
        # print "level", level, ":", tree.value
    else:
        print "WARNING: could not understand tree type"
        assert False

# Consider implementing a print statement for each class
def print_tree_pegasus_style(tree):
    print "Printing out existential graph tree in minimal Pegasus format..."
    tree.printTree()
    print
