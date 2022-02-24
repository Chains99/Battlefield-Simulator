from abc import ABCMeta,abstractmethod
from syntax_analyzer.bfs_grammar.grammar import Grammar
from lexical_analyzer.Token import Token
from typing import List


class Parser(metaclass=ABCMeta):
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    @abstractmethod
    def parse(self, token_list: List[Token]) -> AST:
        pass