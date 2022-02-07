import Lexer.LexycalAnalisis
from Lexer.TokenManager import Token_Manager
from Core.Core import Output_info


class lexer():
    def __init__(self):
        self.analyser = Lexer.LexycalAnalisis.LexicalAnalyzer()
        self.output_info = Output_info()

    def get_token_manager(self, filename, code):
        errors = []
        tokens = self.analyser.get_tokens(filename, code, errors)
        for error in errors:
            self.output_info.add_error(error)
        return Token_Manager(tokens)
