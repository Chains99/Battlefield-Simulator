from json import load
import json
from os.path import exists
from Language.Lexer.Token import Token, TokenType
from Language.Grammar.grammar import Grammar
from Language.Parser.lr1_aux import LR1Table
from typing import List


class LR1Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        p = grammar.get_productions()
        if not exists("action.json") or not exists("go_to.json"):
            self.table: LR1Table = LR1Table(grammar)
            with open('action.json', 'w') as fout:
                json.dump(self.table.action_table, fout)

            with open('go_to.json', 'w') as fout:
                json.dump(self.table.go_to_table, fout)

        with open("action.json") as file:
            self.actions_table = load(file)

        with open("go_to.json") as file:
            self.go_to_table = load(file)

        self.final = Token('$', '$', TokenType.Symbol)

    def parse(self, tokens: List[Token]):
        tokens.append(Token('$', '$', TokenType.Symbol))
        tokens_stack = []
        states_id_stack = [0]
        ast = []
        grammar_prod = self.grammar.get_productions()

        while len(tokens) > 0:
            token = tokens[0]
            current_state_actions = self.actions_table[states_id_stack[-1]]
            if token.value not in current_state_actions:
                raise Exception(
                    f'Unexpected token {token.value} with value {token.lexeme} and type {token.type}')

            action = current_state_actions[token.value]
            if action[0] == 'OK':
                return ast[0]
            
            #Apply a SHIFT Action
            elif action[0] == 'S':
                states_id_stack.append(action[1])
                tokens_stack.append(token.lexeme)
                tokens = tokens[1:] if len(tokens) >= 1 else []

            #Apply a REDUCE Action
            else:
                prod = grammar_prod[action[1]]
                if prod.ast_node_builder is not None:
                    prod.ast_node_builder(tokens_stack, ast)

                self.remove_prod(len(prod.symbols), states_id_stack, tokens_stack)

                state_go_to = self.go_to_table[states_id_stack[-1]]
                if prod.head.name not in state_go_to:
                    raise Exception(
                        f"Non recognized tokens sequence starting with {prod.head.name}")
                tokens_stack.append(prod.head.name)
                states_id_stack.append(state_go_to[prod.head.name])

    # method to remove production tokens and associated states from their respective stacks
    @staticmethod
    def remove_prod(counter, states, tokens):
        for i in range(counter):
            tokens.pop()
            states.pop()
