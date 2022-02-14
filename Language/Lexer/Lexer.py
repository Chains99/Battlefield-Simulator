from Language.Lexer import LexycalAnalisis
from Language.Lexer.TokenManager import Token_Manager
from Language.Core.Core import Output_info
from Language.Core import Adders
from Language.Lexer.Token import TokenValues


class lexer():
    def __init__(self):
        self.analyser = LexycalAnalisis.LexicalAnalyzer()

        keywords = [
            ("if", TokenValues.If),
            ("else", TokenValues.Else),
            ("Weapon", TokenValues.Weapon),
            ("Soldier", TokenValues.Soldier),
            ("Map", TokenValues.Map),
            ("print", TokenValues.Print),
            ("and", TokenValues.And),
            ("or", TokenValues.Or),
            ("not", TokenValues.Not),
            ("return", TokenValues.Return)
        ]
        Adders.register_keywords(self.analyser, keywords)

        operators = [
            ("+", TokenValues.Add),
            ("*", TokenValues.Mul),
            ("-", TokenValues.Sub),
            ("/", TokenValues.Div),
            ("%", TokenValues.Mod),
            ("<", TokenValues.Less),
            ("<=", TokenValues.LessOrEquals),
            (">", TokenValues.Greater),
            (">=", TokenValues.GreaterOrEquals),
            ("==", TokenValues.Equals),
            ("!=", TokenValues.NotEquals),
            ("=", TokenValues.Assign),
            (",", TokenValues.ValueSeparator),
            (";", TokenValues.StatementSeparator),
            ("(", TokenValues.OpenBracket),
            (")", TokenValues.ClosedBracket),
            ("{", TokenValues.OpenCurlyBraces),
            ("}", TokenValues.ClosedCurlyBraces),
            ("[", TokenValues.OpenStraightBracket),
            ("]", TokenValues.ClosedStraightBracket)
        ]
        Adders.register_operators(self.analyser, operators)
        self.analyser.register_text('"', '"', True)
        self.output_info = Output_info()

    def get_token_manager(self, filename, code):
        errors = []
        tokens = self.analyser.get_tokens(filename, code, errors)
        for error in errors:
            self.output_info.add_error(error)
        return Token_Manager(tokens)
