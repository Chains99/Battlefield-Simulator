from abc import ABCMeta,abstractmethod
from Language.Grammar.grammar import Grammar
from Language.Lexer.Token import Token
from typing import List


class Parser(metaclass=ABCMeta):
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    @abstractmethod
    def parse(self, token_list: List[Token]):
        pass