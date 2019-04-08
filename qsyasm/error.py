class ParseError(Exception):
    def __init__(self, msg, lexpos, lineno):
        super(ParseError, self).__init__(msg)
        self.msg = msg
        self.lexpos = lexpos
        self.lineno = lineno


class QsyASMError(RuntimeError):
    pass
