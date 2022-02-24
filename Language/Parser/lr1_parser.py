from copy import error
from Language.Parser.parser import Parser
from Language.Grammar.grammar import Grammar,Terminal,Production,Symbol
from Language.Parser.lr1_parser import LR1Table
from Language.Lexer.Token import Token
from typing import List, Deque, Tuple


class LR1Parser(Parser):
    def __init__(self, grammar: Grammar):
        super().__init__(grammar)
        self.table=LR1Table(grammar)

    def parse(self, token_list: Deque[Token]):
        table = self.lr1_table
        stack: List[Tuple[Symbol, int]] = []
        i = 0
        while len(token_list)>0:
            token = token_list[i]

            current_state = stack[-1][1] if stack else 0
            table_val = table[current_state, token.type]
            
            if table_val == "OK":
                break
            if isinstance(table_val, int):
                term = Terminal(token.type, value=token.value)
                stack.append((term, table_val))
                i += 1
            elif isinstance(table_val, Production):
                reduce_prod = table_val
                # Pop from stack the necessary items
                items_needed = len(reduce_prod.symbols)
                items = []
                if items_needed != 0:
                    stack, items = stack[:-items_needed], stack[-items_needed:]
                items = [item[0].ast for item in items]

                # Apply reduction
                new_head = reduce_prod.head.copy()
                new_head.set_ast(reduce_prod.build_ast(items))


                # Check next state
                left_state = stack[-1][1] if stack else 0
                next_state = table[left_state, reduce_prod.head.name]

                # Push to stack the new item
                stack.append((new_head, next_state))
            elif table_val is None:
                raise error(f"Unexpected token", token)

        if len(stack) != 1:
            raise ValueError(f"Dirty stack at the end of the parsing. Stack: {stack}")
        return stack[-1][0].ast