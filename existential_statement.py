import statement
'''
Goal of this file to create basic classes to represent the different logical structures
in Existential Graphs.  Will also contain the createTree function that transfrom the standard
tree into the Existential Graph tree.

1. Convert statents using lex and yacc into starting tree
2. Apply the visitor pattern to search through starting tree for AND statements and squash the children to a single level
    - Add a function to statment.py - will probably want to make a subclass from binary statement specially for ANDs
3. Transformation function
    - Post order traversal on the starting tree using the visitor pattern
    - Keep a stack of "trees", so basically hold each chunck of the new EG tree where the top of the stack represents the top of the tree at thend
    - When you see a function (eg. NOT AND OR IMP BICON), call the associating EG convert function that just sets up the structure where you pass in the next two or more (for AND) elements as children
    - Push the new EG component created from the step before onto the stack
    - At the end, stack should only contain EG components and the root function which you then do a final Transformation
    - Return the tree
'''

# def transform(stdtree, eg_tree):
#     if isinstance(stdtree, )
#
# def transformToEGTree(stdtree):
#     eg_tree = SheetAssertion("SA")
#
#     transform(stdtree, eg_tree)
#
# # Root of every Existential Graph Tree is the Sheet of Assertion (SA), so that's
# # the default value of a simple statement
# class SheetAssertion(object):
#     def __init__(self, value):
#         self._value = value
#
#     @property
#     def value(self):
#         return self._value
#
# class EXAtom(EXStatement):
#     def __init__(self, value):
#         super(EXAtom, self).__init__(value)
