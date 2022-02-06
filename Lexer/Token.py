import enum


class TokenType(enum.Enum):
    Unknown = 1
    Number = 2
    Text = 3
    Keyword = 4
    Identifier = 5
    Symbol = 6


class Token:
    def __init__(self, type, value, location):
        self.value = value
        self.type = type
        self.location=location


class TokenValues:
    def __init__(self, type, value):
        # Arithmetic Operators
        self.Add = "Addition"  # +
        self.Sub = "Subtract"  # -
        self.Mul = "Multiplication"  # *
        self.Div = "Division"  # /
        self.Mod = "Modulus"  # %

        # Comparative Operators
        self.Less = "Less"  # <
        self.LessOrEquals = "LEqual"  # <=
        self.Greater = "Greater"  # >
        self.GreaterOrEquals = "GEqual"  # >=
        self.Equals = "Equals"  # ==
        self.NotEquals = "NEquals"  # !=

        # Logical Operators
        self.And = "And"  # and
        self.Or = "Or"  # or
        self.Not = "Not"  # !
        # self.Dots = "Dots"

        # Assignment
        self.Assign = "Assign"  # =

        # Separators
        self.ValueSeparator = "ValueSeparator"  # ,
        self.StatementSeparator = "StatementSeparator"  # ;

        #
        self.OpenBracket = "OpenBracket"  # (
        self.ClosedBracket = "ClosedBracket"  # )
        self.OpenCurlyBraces = "OpenCurlyBraces"  # {
        self.ClosedCurlyBraces = "ClosedCurlyBraces"  # }
        self.OpenStraightBracket = "StraightBracket"  # [
        self.ClosedStraightBracket = "ClosedStraightBracket"  # ]

        #
        self.Print = "Print"  # print

        #
        self.Sequence = "Sequence"  # sequence
