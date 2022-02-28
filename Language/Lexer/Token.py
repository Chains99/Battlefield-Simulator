import enum


class TokenType(enum.Enum):
    Unknown = 1
    Number = 2
    Text = 3
    Keyword = 4
    Identifier = "Identifier"
    Symbol = "Symbol"
    EOF = "EOF"


class Token:
    def __init__(self, value, lexeme, type, location=0):
        self.type = type
        self.value = value
        self.lexeme = lexeme
        self.location = location

    def __str__(self):
        return f"({self.value}, {self.type})"


class TokenValues:
    # Keywords
    Def = "def"
    Return = "return"
    If = "if"
    Else = "else"
    Elif = "elif"
    While = "while"

    # Types
    Map = "Map"
    Soldier = "Soldier"
    Weapon = "Weapon"
    Number = "number"
    String = "string"
    Bool = "bool"

    _True = "true"
    _False = "false"

    number = "number"

    # Arithmetic Operators
    Add = "+"  # +
    Sub = "-"  # -
    Mul = "*"  # *
    Div = "/"  # /
    Mod = "%"  # %
    Pow = "^"  # ^

    # Comparative Operators
    Less = "<"  # <
    LessOrEquals = "<="  # <=
    Greater = ">"  # >
    GreaterOrEquals = ">="  # >=
    Equals = "=="  # ==
    NotEquals = "!="  # !=

    # Logical Operators
    And = "and"  # and
    Or = "or"  # or
    Not = "not"  # !
    dot = "dot"  # .

    # Assignment
    Assign = "="  # =

    # Separators
    ValueSeparator = ","  # ,
    StatementSeparator = ";"  # ;

    # Text
    QuotationMarks = '"'  # "
    QuotationMarksS = "'"  # '

    # Others
    TwoPoints = ":"  #:

    #
    OpenBracket = "("  # (
    ClosedBracket = ")"  # )
    OpenCurlyBraces = "{"  # {
    ClosedCurlyBraces = "}"  # }
    OpenStraightBracket = "["  # [
    ClosedStraightBracket = "]"  # ]

    #
    Print = "Print"  # print

    #
    List = "List"  # list

    def __init__(self):
        pass
