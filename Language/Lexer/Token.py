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
        self.location = location

    def __str__(self):
        return f"({self.value}, {self.type})"


class TokenValues:
    # Keywords
    Soldier = "Soldier"
    Weapon = "Weapon"
    Map = "Map"
    If = "If"
    Else = "Else"
    Return = "Return"

    # Arithmetic Operators
    Add = "Addition"  # +
    Sub = "Subtract"  # -
    Mul = "Multiplication"  # *
    Div = "Division"  # /
    Mod = "Modulus"  # %

    # Comparative Operators
    Less = "Less"  # <
    LessOrEquals = "LEqual"  # <=
    Greater = "Greater"  # >
    GreaterOrEquals = "GEqual"  # >=
    Equals = "Equals"  # ==
    NotEquals = "NEquals"  # !=

    # Logical Operators
    And = "And"  # and
    Or = "Or"  # or
    Not = "Not"  # !
    # self.Dots = "Dots"

    # Assignment
    Assign = "Assign"  # =

    # Separators
    ValueSeparator = "ValueSeparator"  # ,
    StatementSeparator = "StatementSeparator"  # ;

    #
    OpenBracket = "OpenBracket"  # (
    ClosedBracket = "ClosedBracket"  # )
    OpenCurlyBraces = "OpenCurlyBraces"  # {
    ClosedCurlyBraces = "ClosedCurlyBraces"  # }
    OpenStraightBracket = "StraightBracket"  # [
    ClosedStraightBracket = "ClosedStraightBracket"  # ]

    #
    Print = "Print"  # print

    #
    Sequence = "Sequence"  # sequence

    def __init__(self):
        pass
