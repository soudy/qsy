import ply.yacc as yacc
import itertools
import numpy as np

from . import tokens
from .instruction import Instruction
from .error import ParseError


class QsyASMParser:
    tokens = tokens
    precedence = (
        ('left', 'PLUS', 'MIN'),
        ('left', 'MUL', 'DIV'),
        ('left', 'POW'),
        ('right', 'UMIN')
    )
    variables = {
        'pi': np.pi
    }

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
        '''instruction : normal_instruction
                       | adjoint_instruction'''
        p[0] = p[1]

    def p_normal_instruction(self, p):
        '''normal_instruction : term argument_list
                              | param_term argument_list'''
        p[0] = Instruction(p[1], p[2], p.lineno(0), p.lexpos(0))

    def p_adjoint_instruction(self, p):
        'adjoint_instruction : ADJ normal_instruction'
        instr = p[2]

        if not instr.is_gate():
            raise ParseError('Invalid operation "{}" for adjoint'.format(instr.op_name),
                             p.lexpos(2), p.lineno(2))

        instr.toggle_adjoint()
        p[0] = instr

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
        'param_term : IDENT LPAREN expression RPAREN'
        p[0] = (p[1], p[3])

    def p_argument_list(self, p):
        'argument_list : term'
        p[0] = [p[1]]

    def p_argument_list_args(self, p):
        'argument_list : term COMMA argument_list'
        p[0] = [p[1]]
        p[0] += p[3]

    def p_expression_bin_op(self, p):
        '''expression : expression PLUS expression
                      | expression MIN expression
                      | expression DIV expression
                      | expression POW expression
                      | expression MUL expression'''
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '/':
            if p[3] == 0.0:
                raise ParseError('Division by zero', p.lexpos(2), p.lineno(2))
            p[0] = p[1] / p[3]
        elif p[2] == '**':
            p[0] = p[1] ** p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]

    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_integer(self, p):
        'expression : INTEGER'
        p[0] = p[1]

    def p_expression_float(self, p):
        'expression : FLOAT'
        p[0] = p[1]

    def p_expression_unary_min(self, p):
        'expression : MIN expression %prec UMIN'
        p[0] = -p[2]

    def p_expression_ident(self, p):
        'expression : IDENT'
        if p[1] not in self.variables:
            raise ParseError(
                'Undefined variable "{}"'.format(p[1]),
                p.lexpos(1), p.lineno(1)
            )

        p[0] = self.variables[p[1]]

    def p_error(self, p):
        raise ParseError('Unexpected "{}"'.format(p.type), p.lexpos, p.lineno)

    def parse(self, s):
        return self.parser.parse(s, debug=False, tracking=True)
