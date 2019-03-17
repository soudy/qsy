class ParseError(Exception):
    def __init__(self, msg, token):
        super(ParseError, self).__init__(msg)
        self.msg = msg
        self.token = token

class ProgramError(Exception):
    pass
