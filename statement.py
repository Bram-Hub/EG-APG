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

class AndStatement(Statement):
    def __init__(self, value, children):
        super(AndStatement, self).__init__(value)
        self._children = children

    @property
    def children(self):
        return self._children

    def add_children(self, new_child):
        self._children.append(new_child)

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
    elif isinstance(tree, AndStatement):
        print "\t"*level, tree.value
        #print tree.children
        for i in range(0, len(tree.children)):
            print_tree(tree.children[i], level + 1)
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

# Combine all the levels of an extended AND into a single level in the tree
def squash_tree(tree, stack):
    if isinstance(tree, BinaryStatement) or isinstance(tree, AndStatement):
        # Check if it's an AND
        if tree.value == '&':
            # Check the top of the stack and combine if not an AND statement
            squash_tree(tree.left, stack)
            squash_tree(tree.right, stack)
            prev_statement = stack.pop()
            and_statement = AndStatement('&', [])
            if len(stack) > 0:
                # Keep adding to the list of children of the and statement until another and statement or binary statement is reached
                # Should work for left and right leaning tree with an "AND" chain
                while len(stack) > 0 and (not isinstance(prev_statement, AndStatement) or not isinstance(prev_statement, BinaryStatement)):
                    #print type(prev_statement)
                    and_statement.add_children(prev_statement)
                    prev_statement = stack.pop()
                # if isinstance(prev_statement, BinaryStatement) or isinstance(prev_statement, AndStatement):
                #     stack.append(prev_statement)
                # else:
                and_statement.add_children(prev_statement)

                stack.append(and_statement)
            else:
                stack.append(prev_statement)
        else:
            # For any other binary statement, just recreate the binary statement and push onto the stack
            # If following a post order traversal, should be able to depend on the fact that the children are already on the stack
            squash_tree(tree.left, stack)
            squash_tree(tree.right, stack)
            prev_right = stack.pop()
            prev_left = stack.pop()
            stack.append(BinaryStatement(tree.value, prev_left, prev_right))
    elif isinstance(tree, UnaryStatement):
        squash_tree(tree.child, stack)
        prev_statement = stack.pop()
        stack.append(UnaryStatement(tree.value, prev_statement))
    elif isinstance(tree, IdStatement):
        stack.append(IdStatement(tree.value))
    elif isinstance(tree, ContradictionStatement):
        stack.append(ContradictionStatement())
    else:
        print "WARNING: could not understand tree type"
        assert False
    return stack

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
