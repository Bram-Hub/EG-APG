from __future__ import print_function
import statement

tokens = (
    # meaningful symbols
    'NOT',
    'AND',
    'OR',
    'IMPLICATION',
    'BICONDITIONAL',
    'CONTRADICTION',
    'ID',

    # non-meaningful symbols
    'LPAREN',
    'RPAREN'
)

t_ID  = r'[a-zA-Z]'
t_NOT = r'~'
t_AND = r'&'
t_OR  = r'\|'
t_IMPLICATION = r'-'
t_BICONDITIONAL = r'='
t_CONTRADICTION = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# ignored characters
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# lexer
import ply.lex as lex
lexer = lex.lex()

# Grammar
# S: ! | E
# E: A -> E | A -> ! | A <--> E | A
# A: B|A | B & A | B
# B: ~B | C
# C: (E) | id

# parsing rules
precedence = (
    ('left','AND','OR',
            'IMPLICATION',
            'BICONDITIONAL',
            'CONTRADICTION'),
    ('right', 'NOT')
)

def p_statement_contradiction(t):
    'statement : CONTRADICTION'
    t[0] = statement.ContradictionStatement()
    tree = t[0] # Not sure what to do about attribute rules
def p_statement_expression(t):
    'statement : expression'
    t[0] = t[1]
    tree = t[0]

def p_expression_implication(t):
    'expression : binary IMPLICATION expression'
    t[0] = statement.BinaryStatement("-", t[1], t[3])
def p_expression_contrasubproof(t):
    'expression : binary IMPLICATION CONTRADICTION'
    t[0] = statement.BinaryStatement("-", t[1],
                                     statement.ContradictionStatement())

def p_expression_biconditional(t):
    'expression : binary BICONDITIONAL expression'
    t[0] = statement.BinaryStatement("=", t[1], t[3])
def p_expression_pass(t):
    'expression : binary'
    t[0] = t[1]

def p_binary_or(t):
    'binary : unary OR binary'
    t[0] = statement.BinaryStatement("|", t[1], t[3])
def p_binary_and(t):
    'binary : unary AND binary'
    t[0] = statement.BinaryStatement("&", t[1], t[3])
def p_binary_pass(t):
    'binary : unary'
    t[0] = t[1]

def p_unary_neg(t):
    'unary : NOT unary'
    t[0] = statement.UnaryStatement("~", t[2])
def p_unary_pass(t):
    'unary : root'
    t[0] = t[1]

def p_root_paren(t):
    'root : LPAREN expression RPAREN'
    t[0] = t[2]
def p_root_id(t):
    'root : ID'
    t[0] = statement.IdStatement(t[1])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

def parse_sentence(s):
    ret = parser.parse(s)
    print("DEBUG")
    statement.print_tree(ret)
    return ret
