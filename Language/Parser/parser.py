from Language.Grammar.grammar import Grammar
from typing import List
from Language.Lexer.Token import Token, TokenType


class LR1Parser:
    def __init__(self, grammar: Grammar, actions_table, go_to_table):
        self.grammar = grammar
        self.actions_table = actions_table
        self.go_to_table = go_to_table
        self.final = Token('$', '$', TokenType.Symbol)

    def parse(self, tokens: List[Token]):
        tokens.append(Token('$', '$', TokenType.Symbol))
        tokens_stack = []
        states_id_stack = [0]
        nodes = []

        while len(tokens) > 0:
            token = tokens[0]

            current_state_actions = self.actions_table[states_id_stack[-1]]

            if token.value not in current_state_actions:
                raise Exception(
                    f'Unexpected token {token.value} with value {token.lexeme} and type {token.type}')

            grammar_prod = self.grammar.get_productions()

            action = current_state_actions[token.value]
            if action[0] == 'S':
                states_id_stack.append(action[1])
                tokens_stack.append(token.lexeme)
                tokens = tokens[1:]
            else:
                prod = grammar_prod[action[1]]
                if prod.ast_node_builder is not None:
                    prod.ast_node_builder(tokens_stack, nodes)

                self.remove_prod(len(prod), states_id_stack, tokens_stack)

                state_go_to = self.go_to_table[states_id_stack[-1]]
                if prod.head.name not in state_go_to:
                    raise Exception(
                        f"Non recognized tokens sequence starting with {prod.head.name}")
                tokens_stack.append(prod.head.name)
                states_id_stack.append(state_go_to[prod.head.name])

            if action[0] == 'OK':
                return nodes[0]

    # method to remove production tokens and asociated states from their respective stacks
    @staticmethod
    def remove_prod(counter, states, tokens):
        for i in range(counter):
            tokens.pop()
            states.pop()