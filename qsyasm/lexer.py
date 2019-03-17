import ply.lex as lex
from .error import ParseError

class QsyASMLexer:
    tokens = (
        'INTEGER',
        'IDENT',
        'COMMA',
        'LBRACKET',
        'RBRACKET',
        'LPAREN',
        'RPAREN',
        'LABEL',
        'IF',
        'NEWLINE'
    )

    t_IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_LABEL = r'\.' + t_IDENT
    t_COMMA = r','
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_IF = r'if'

    t_ignore = '\t\r '
    t_ignore_COMMENT = r';.*'

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_error(self, t):
        raise ParseError('Unknown token \'{}\''.format(t.value[0]), t)

lexer = QsyASMLexer()