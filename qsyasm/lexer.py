import ply.lex as lex
from .error import ParseError


class QsyASMLexer:
    tokens = (
        'INTEGER',
        'FLOAT',
        'IDENT',
        'COMMA',
        'LBRACKET',
        'RBRACKET',
        'LPAREN',
        'RPAREN',
        'PLUS',
        'MIN',
        'DIV',
        'POW',
        'MUL',
        'NEWLINE',
        'ADJ'
    )

    reserved = {
        'adj': 'ADJ'
    }

    t_COMMA = r','
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_PLUS = r'\+'
    t_MIN = r'-'
    t_DIV = r'/'
    t_POW = r'\*\*'
    t_MUL = r'\*'

    t_ignore = '\t\r '
    t_ignore_COMMENT = r';.*'

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_IDENT(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENT')
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_FLOAT(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
        return t

    def t_error(self, t):
        raise ParseError('Unknown token "{}"'.format(t.value[0]), t)


lexer = QsyASMLexer()
