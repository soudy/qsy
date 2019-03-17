import ply.yacc as yacc
import itertools

from . import tokens
from .instruction import Instruction
from .error import ParseError

class QsyASMParser:
    tokens = tokens

    def __init__(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_program(self, p):
        '''program : program instruction
                   | instruction'''
        if len(p) == 2 and p[1]:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = p[1]

            if not p[0]:
                p[0] = []

            if p[2]:
                p[0] += [p[2]]

    def p_instruction(self, p):
        '''instruction : term argument_list
                       | param_term argument_list'''
        p[0] = Instruction(p[1], p[2], p.lineno(0), p.lexpos(0))

    def p_instruction_newline(self, p):
        'instruction : NEWLINE'
        pass

    def p_term(self, p):
        '''term : IDENT
                | INTEGER
                | lookup'''
        p[0] = p[1]

    def p_lookup(self, p):
        'lookup : IDENT LBRACKET INTEGER RBRACKET'
        p[0] = (p[1], p[3])

    def p_param_term(self, p):
        'param_term : IDENT LPAREN argument_list RPAREN'
        p[0] = (p[1], p[3])

    def p_argument_list(self, p):
        'argument_list : term'
        p[0] = [p[1]]

    def p_argument_list_args(self, p):
        'argument_list : term COMMA argument_list'
        p[0] = [p[1]]
        p[0] += p[3]

    def p_error(self, p):
        raise ParseError('Unexpected \'{}\''.format(p.type), p)

    def parse(self, s):
        return self.parser.parse(s, debug=False, tracking=True)
