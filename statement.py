class Statement(object):

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

class BinaryStatement(Statement):

    def __init__(self, value, arg1, arg2):
        super(BinaryStatement, self).__init__(value)
        self._left = arg1
        self._right = arg2

    @property
    def left(self):
        return self._left
    @property
    def right(self):
        return self._right

class UnaryStatement(Statement):

    def __init__(self, value, argument):
        super(UnaryStatement, self).__init__(value)
        self._child = argument

    @property
    def child(self):
        return self._child

class IdStatement(Statement):

    def __init__(self, value):
        super(IdStatement, self).__init__(value)

class ContradictionStatement(Statement):

    def __init__(self):
        super(ContradictionStatement, self).__init__("!")

def print_tree(tree, level=0):
    if isinstance(tree, BinaryStatement):
        # print "level", level, ":", tree.value
        print "\t"*level, tree.value
        print_tree(tree.left, level + 1)
        print_tree(tree.right, level + 1)
    elif isinstance(tree, UnaryStatement):
        # print "level", level, ":", tree.value
        print "\t"*level, tree.value
        print_tree(tree.child, level + 1)
    elif isinstance(tree, IdStatement):
        print "\t"*level, tree.value
        # print "level", level, ":", tree.value
    elif isinstance(tree, ContradictionStatement):
        print "\t"*level, tree.value
        # print "level", level, ":", tree.value
    else:
        print "WARNING: could not understand tree type"
        assert False

def getAllOrOperands(statement, ors):
    if statement.value != '|':
        ors.append(statement)
        return ors

    ors.append(statement.left)
    return getAllOrOperands(statement.right, ors)

def getAllAndOperands(statement, ands):
    if statement.value != '&':
        ands.append(statement)
        return ands

    ands.append(statement.left)
    return getAllAndOperands(statement.right, ands)

# Literal comparison
def compareTree(tree1, tree2):
    if isinstance(tree1, IdStatement) and isinstance(tree2, IdStatement):
        if tree1.value == tree2.value:
            return True
        else: return False
    if isinstance(tree1, ContradictionStatement) and isinstance(tree2, ContradictionStatement):
        return True

    if tree1.value == tree2.value:
        if isinstance(tree1, BinaryStatement) and isinstance(tree2, BinaryStatement):
            return compareTree(tree1.left, tree2.left) and compareTree(tree1.right, tree2.right)
        elif isinstance(tree1, UnaryStatement) and isinstance(tree2, UnaryStatement):
            return compareTree(tree1.child, tree2.child)

    return False
