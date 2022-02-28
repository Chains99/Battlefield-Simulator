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
    Number = "Number"
    String = "String"
    Bool = "Bool"
    Void = "Void"


    _True = "true"
    _False = "false"
    _None = "none"

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
    Dot = "."  # .
    #
    OpenBracket = "("  # (
    ClosedBracket = ")"  # )
    OpenCurlyBraces = "{"  # {
    ClosedCurlyBraces = "}"  # }
    OpenStraightBracket = "["  # [
    ClosedStraightBracket = "]"  # ]

    #
    Print = "print"  # print

    #
    List = "list"  # list

    def __init__(self):
        pass
