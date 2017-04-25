from statement import *
from sys import stdout
import re
# import string

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

    def to_string_tree(self):
        return str(value)

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

    def to_string_tree(self):
        my_str = ""
        for i in range(0, self.num_children):
            my_str += self.children[i].to_string_tree()
        return my_str

# An atom in the EG tree that only has a value that is a starting
# Children: None
class EGAtom(EGStatement):
    def __init__(self, value):
        super(EGAtom, self).__init__(value, 0)

    def printTree(self):
        stdout.write(self.value + "|")

    def to_string_tree(self):
        return str(self.value) + "|"

# An empty cut, or a contradiction, in the EG tree
# Children: None
class EGEmptyCut(EGStatement):
    def __init__(self):
        super(EGEmptyCut, self).__init__("()", 0)

    def printTree(self):
        stdout.write("()")

    def to_string_tree(self):
        return "()"

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

    def to_string_tree(self):
        my_str = ""
        my_str += "("
        my_str += self.child.to_string_tree()
        my_str += ")"
        return my_str

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
        self._children[child_index] = new_child

    def printTree(self):
        for i in range (0, self.num_children):
            if self.children[i] == None:
                stdout.write("()")
            else:
                self.children[i].printTree()

    def to_string_tree(self):
        my_str = ""
        for i in range (0, self.num_children):
            my_str += self.children[i].to_string_tree()
        return my_str

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

    def to_string_tree(self):
        my_str = ""
        my_str += "("
        my_str += self.left.to_string_tree()
        my_str += self.right.to_string_tree()
        my_str += ")"
        return my_str

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

    def to_string_tree(self):
        my_str = ""
        my_str += "("
        my_str += self.right.to_string_tree()
        my_str += self.left.to_string_tree()
        my_str += ")"
        return my_str

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

    def to_string_tree(self):
        my_str = ""
        my_str += self.left.to_string_tree()
        my_str += self.right.to_string_tree()

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
    elif tree is None:
        pass
    else:
        print "WARNING: could not understand tree type"
        assert False

# Consider implementing a print statement for each class
def print_tree_pegasus_style(tree):
    print "Printing out existential graph tree in minimal Pegasus format..."
    tree.printTree()
    #print tree.to_string_tree()

# given n,
# returns all permutations

#ex. n=1: [[1]]
#ex. n=2: [[1,2],[2,1]]
#ex. n=3: [[x,1,2][1,x,2][1,2,x],[x,2,1][2,x,1][2,1,x]]
# [[3,1,2][1,3,2][1,2,3],[3,2,1][2,3,1][2,1,3]]
#ex. n=4: [[]]
def permutate(n):
    p = []
    if n == 1:
        p.append([1])
        return p
    else:
        temp = permutate(n-1)
        # print "temp: ", temp
        end = len(temp)
        build = []
        for j in range (end):
            for i in range (n-1):
                # print "j: ", j, " i:",i
                build.extend(temp[j][0:i])
                build.append(n)
                build.extend(temp[j][i:end])
                p.append(build)
                build = []
            build.extend(temp[j])
            build.append(n)
            p.append(build)
            build = []
        return p


def children_of(str_t):
    children = []
    next_index = 0

    # opens = [m.start() for m in re.finditer('\(', str_t)]
    # closes = [m.start() for m in re.finditer('\)', str_t)]

    # print "opens: ", opens, "   closes: ", closes


    # if len(opens) != len(closes):
        # print "screwed up somehow: length of opens doesn't equal length of closes"

    # if simple children, no cuts
    if str_t.find('(') == -1:
         for i in range(len(str_t)-1):
            if i < next_index:
                continue
            # identify the start and end index of this child
            child_index = i
            next_index = str_t.find('|', i)+1
            # add the child to the list of em all
            if child_index != next_index:
                children.append(str_t[child_index:next_index])
    else:
    # more complicated children - figure out the matching close paren
        for i in range(len(str_t)):
            if i < next_index:
                continue
            if str_t[i] == '(':
                open_paren_count = 1  #umm not sure why this is a 2 rather than a 1
                child_index = i
                s = i
                s += 1
                ne_op_in = str_t.find('(', s)
                ne_cl_in = str_t.find(')', s)
                while open_paren_count > 0:
                    # print "open_paren_count: ", open_paren_count
                    # found another open
                    if (ne_cl_in > ne_op_in):
                        open_paren_count += 1
                    else:
                        open_paren_count -= 1
                        if open_paren_count == 0:
                            next_index = ne_cl_in+1
                            break
                    s += 1
                    ne_op_in = str_t.find('(', s)
                    ne_cl_in = str_t.find(')', s)
            else:
                child_index = i
                next_index = str_t.find('|', i)+1

            if child_index != next_index:
                children.append(str_t[child_index:next_index])

    children = filter(None, children)
    return children
        # str.find(str, beg=0, end=len(string))

def string_permutations_of_EG_tree(t):
    permutations = []
    str_t = t.to_string_tree()
    ch_list = children_of(str_t)
    print "childresn!!!: ", ch_list

    permutation_indicies = permutate(len(ch_list))
    # print "permutation_indicies: ", permutation_indicies

    for perm in permutation_indicies:
        build = ""
        for p in perm:
            build += ch_list[p-1]
        permutations.append(build)

    # permutations.append(t.to_string_tree())

    return permutations

# compare function:
# input: two existential statements
# returns true if EG equivelent
# otherwise false
def compare_EG_trees(eg_tree_1, eg_tree_2):
    test = permutate(3)
    # print "test 3: ", test
    # permutations = string_permutations_of_EG_tree(eg_tree_2)
    print "permutations"
    for p in permutations:
        print p
        if eg_tree_1.to_string_tree() == p:
            return True
    return False
