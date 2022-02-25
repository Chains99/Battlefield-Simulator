from Language.Lexer.Token import Token, TokenType
from Language.Lexer.Token import Token
from typing import Set, Dict, List, Tuple, Union
from Language.Grammar.grammar import Grammar, Production, Symbol, NonTerminal, Terminal
from Language.Parser.lr1_item import LR1Item


class LR1Table:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.first: Dict[str, Set[Terminal]] = None
        self.follow: Dict[str, Set[Terminal]] = None
        self._hash = None
        self.dict_states_id: Dict[int, List[LR1Item]] = {}
        self.dict_states_hash = {}
        self.dict_clousure_hash = {}
        self.dict_lr1_items: Dict[Production, int, Terminal] = {}
        self.dict_item_prods = {}
        self.extend_grammar()
        self.build_table()

    def build_table(self):
        self.first = self.calculate_first()
        self.follow = self.calculate_follow()
        lr1_items = self.get_all_lr1_items()

        self.dict_lr1_items = {}
        for item in lr1_items:
            for follow in self.follow[item.production.head.name]:
                new_lr_item = LR1Item(item.production, item.dot_index, follow)
                self.dict_lr1_items[item.production, item.dot_index, follow] = new_lr_item

        init_state = self.closure(
            {
                self.dict_lr1_items[
                    self.grammar.start.productions[0],
                    0,
                    list(self.follow[self.grammar.start.name])[0],
                ]
            }
        )

        self.dict_states_id = {0: init_state}

        lr1_table: Dict[Tuple[int, str], Union[str, int, Production]] = {}
        current_state = 0
        while current_state < len(self.dict_states_id):
            state = self.dict_states_id[current_state]
            for item in state:
                if item.get_symbol_at_dot() is None:
                    val = "OK" if item.production.head.name == "S`" else item.prod
                    table_key = (current_state, item.lookahead.name)
                else:
                    val = self.go_to(current_state, item.get_symbol_at_dot())
                    table_key = (current_state, item.get_symbol_at_dot)

                cont_val = lr1_table.get(table_key, None)

                if cont_val is not None and cont_val != val:
                    raise ValueError(
                        f"LR1 table already contains "
                        f"{table_key} -> {cont_val.__repr__()}  *** {val.__repr__()}"
                    )
                lr1_table[table_key] = val
            current_state += 1
        self._table = lr1_table

    def extend_grammar(self):
        new_production = Production([self.grammar.start])
        new_production.set_builder(self.grammar.start.productions[0].get_ast_node_builder())
        new_non_terminal = NonTerminal('S', [new_production])
        new_production.head = new_non_terminal
        self.grammar.start = new_non_terminal
        self.grammar.non_terminal_list.append(new_non_terminal)

    def get_all_lr1_items(self) -> List[LR1Item]:
        lr1_items = []
        self.dict_item_prods = {}
        for prod in self.grammar.get_productions():
            for dot_pos in range(len(prod.symbols) + 1):
                item_prod = prod
                slr_item = LR1Item(item_prod, dot_pos)
                lr1_items.append(slr_item)
                if prod.head not in self.dict_item_prods:
                    self.dict_item_prods[prod.head] = []
                self.dict_item_prods[prod.head].append(item_prod)
        return lr1_items

    def calculate_first(self):
        first = {prod.head.name: prod.head._terminals_set for prod in self.grammar.get_productions()}
        prod_first = {prod: prod.head._terminals_set for prod in self.grammar.get_productions()}

        change = True
        while change:
            change = False
            for prod in self.grammar.get_productions():
                head = prod.head
                head_name = prod.head.name

                for item in prod.symbols:
                    if item.is_terminal():
                        set_ = first[head_name]
                        len_set_before = len(set_)
                        set_.add(item)
                        len_set_after = len(set_)
                        change |= len_set_before != len_set_after
                        prod_first[prod].add(item)
                        break

                    if item != head:
                        set_ = first[item.name]
                        len_set_before = len(set_)
                        set_.update(first[item.name])
                        len_set_after = len(set_)
                        change |= len_set_before != len_set_after
                        prod_first[prod].update(first[item.name])

                    if "EPS" not in first[head.name]:
                        break
        return first

    def calculate_follow(self, first=None):
        if first is None:
            first = self.calculate_first()

            follow = {non_term.name: non_term._terminals_set for non_term in self.grammar.non_terminal_list}
            follow[self.grammar.start.name].add(Terminal("$", "$"))

            change = True
            while change:
                change = False
                for prod in self.grammar.get_productions():
                    prod_head = prod.head
                    for i, item in enumerate(prod.symbols):
                        next_item = prod.symbols[i + 1] if i + 1 < len(prod.symbols) else None
                        if item.is_terminal:
                            continue
                        if next_item is None:
                            change |= follow[item.name].update(follow[prod_head] - "EPS")
                        elif next_item.is_terminal:
                            change |= follow[item.name].add(next_item)
                        else:
                            change |= follow[item.name].update(first[next_item] - "EPS")
                            if "EPS" in first[next_item]:
                                change |= follow[item.name].update(follow[prod_head] - "EPS")
            return follow

    def get_no_state(self, items: Set[LR1Item]) -> int:
        hash_ = self.get_items_hash(items)
        if hash_ in self.dict_states_hash:
            return self.dict_states_hash[hash_]
        number = len(self.dict_states_id)
        self.dict_states_id[number] = items
        self.dict_states_hash[hash_] = number
        return number

    def closure(self, items: Set[LR1Item]):
        hash = self.get_items_hash(items)
        if hash in self.dict_clousure_hash:
            return self.dict_clousure_hash[hash]
        closure = items
        change = True
        while change:
            change = False
            new = set()
            for item in closure:
                next_item = item.get_symbol_at_dot()
                if next_item is None or next_item.is_terminal:
                    continue
                lookahead = item.lookahead
                rest = item.production.symbols[item.dot_index + 1:]
                rest.append(lookahead)
                for prod in self._item_prods[next_item.name]:
                    for fol in self._follow[next_item]:
                        if not self.is_in_first(fol, *rest):
                            continue
                        lr_item = self._lr_items[prod, 0, fol]
                        if lr_item not in closure:
                            new.add(lr_item)
                            change = True
            closure.update(new)
        self.dict_clousure_hash[hash] = closure
        return closure

    def is_in_first(self, terminal, symbols):
        for symbol in symbols:
            if isinstance(symbol, Symbol) and symbol.is_terminal:
                return symbol == terminal
            if terminal in self.first[symbol]:
                return True
            if "EPS" not in self.first[symbol]:
                break
        return False

    def get_items_hash(self, items: Set[LR1Item]):
        return sum(hash(i) for i in items)

    def go_to(self, state_id: int, symbol: Symbol):
        lr1_items = self.dict_states_id[state_id]
        new_items_set = {
            self.dict_lr1_items[item.production, item.dot_index + 1, item.lookahead]
            for item in lr1_items
            if item.get_symbol_at_dot() == symbol
        }
        clausure = self.closure(new_items_set)
        return self.get_no_state(clausure)

    def __getitem__(self, key):
        return self._table.get(key, None)


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
