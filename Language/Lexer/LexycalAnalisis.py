from typing import List

from Language.Core.Core import CompilingError, Code_Location
from Language.Core.Core import ErrorCode
from Language.Lexer.Token import Token, TokenType


class token_reader:
    def __init__(self, file_name, code):
        self.file_name = file_name
        self.code = code
        self.lastLB = -1
        self.pos = 0
        self.line = 1

    def get_codelocation(self):
        return Code_Location(self.file_name, self.line, self.pos - self.lastLB)

    def peek(self):
        if (self.pos < 0 or self.pos >= len(self.code)):
            return
        return self.code[self.pos]

    def eof(self):
        return self.pos >= len(self.code)

    def eol(self):
        return self.eof() or self.code[self.pos] == '\n'

    def ends_with(self, prefix):
        if self.pos + len(prefix) > len(self.code):
            return False
        for i in range(0, len(prefix)):
            if self.code[self.pos + i] != prefix[i]:
                return False
        return True

    def read_any(self):
        if self.eof:
            pass

        if self.eof():
            self.line += 1
            self.lastLB = self.pos
        self.pos += 1
        return self.code[self.pos - 1]

    def read_blank(self):
        if str.isspace(self.peek()):
            self.read_any()
            return True
        return False

    def read_until(self, end, allowLB, text):
        text[0] = ""
        while not self.match(end):
            if not allowLB and (self.eof() or self.eol()):
                return False
            text[0] += self.read_any()
        return True

    def match(self, prefix):
        if self.ends_with(prefix):
            self.pos += len(prefix)
            return True
        return False

    def is_valid_character(self, char, is_first_char):
        return char == '_' or (str.isalpha(char) if is_first_char else str.isalnum(char))

    def read_number(self, number):
        number[0] = ""
        while not self.eol() and str.isnumeric(self.peek()):
            number[0] += self.read_any()
        if (not self.eol() and self.match('.')):
            number[0] += '.'
            while not self.eol() and str.isdigit(self.peek()):
                number[0] += self.read_any()
        if len(number[0]) == 0:
            return False

        while not self.eol() and str.isalnum(self.peek()):
            number[0] += self.read_any()
        return len(number[0]) > 0

    def read_id(self, id):
        id[0] = ""
        while not self.eol() and self.is_valid_character(self.peek(), len(id[0]) == 0):
            id[0] += self.read_any()
        return len(id) > 0


class LexicalAnalyzer:
    def __init__(self):
        self.operators = {}
        self.keywordsDic = {}
        self.list_keywords = []
        self.comments = {}
        self.texts = {}
        self.allowLB = {}

    def register_operator(self, op, tokenValue):
        self.operators[op] = tokenValue

    def register_keyword(self, keyword, tokenValue):
        self.keywordsDic[keyword] = tokenValue

    # Associates a comment starting delimiter with its correspondent ending delimiter

    def register_comment(self, start, end):
        self.comments[start] = end

    # Associates a text literal starting delimiter with their correspondent ending delimiter and the multiline support
    def register_text(self, start, end, allowLB):
        self.texts[start] = end
        self.allowLB[start] = allowLB

    # Matches a comment part in the code and read from the stream all the comment content.
    # The comment is discarded and errors is updated with new errors if detected.
    def match_comment(self, stream, errors):
        for start in sorted(self.comments.keys(), key=lambda start: len(start), reverse=True):
            comment = [""]
            if stream.match(start):
                if not stream.ReadUntil(self.comments.get(start), True, comment):
                    errors.append(CompilingError(stream.location, ErrorCode.expected, self.comments.get(start)))
                return True
        return False

    def match_text(self, stream, tokens: List, errors):
        for start in sorted(self.texts.keys(), key=lambda start: len(start), reverse=True):
            text = [""]
            if stream.match(start):
                if not stream.read_until(self.texts.get(start), self.allowLB.get(start), text):
                    errors.append(CompilingError(stream.location, ErrorCode.expected, self.comments.get(start)))
                tokens.append(Token("String", text, TokenType.Text, stream.get_codelocation))
                return True
        return False

    def match_symbol(self, stream, tokens: List):
        for op in sorted(self.operators.keys(), key=lambda op: len(op), reverse=True):
            if stream.match(op):
                tokens.append(Token(self.operators.get(op), op, TokenType.Symbol, stream.get_codelocation))
                return True
        return False

    def get_tokens(self, file_name, code, errors):
        tokens = []
        stream = token_reader(file_name, code)

        while not stream.eof():
            element = [""]

            if stream.read_blank():
                continue

            elif self.match_symbol(stream, tokens):
                continue

            elif self.match_text(stream, tokens, errors):
                continue

            elif self.match_comment(stream, errors):
                continue

            elif stream.read_number(element):
                number = 0
                if not element[0].replace('.', '', 1).isdigit():
                    errors.Add(CompilingError(stream.get_codelocation(), ErrorCode.invalid, "Number format"))
                tokens.append(Token("number", element[0], TokenType.Number,
                                    stream.get_codelocation()))
                continue

            elif stream.read_id(element):
                if self.keywordsDic.get(element[0]) is not None:
                    tokens.append(Token(self.keywordsDic.get(element[0]), element[0], TokenType.Keyword,
                                        stream.get_codelocation()))
                else:
                    tokens.append(Token('Identifier', element[0], TokenType.Identifier, stream.get_codelocation()))
                continue

            unknown_str = stream.read_any()
            errors.Add(CompilingError(stream.get_codelocation(), ErrorCode.unknown, unknown_str))
        return tokens
