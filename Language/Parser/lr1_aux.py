from Language.Grammar.grammar import Grammar, Symbol, Terminal, NonTerminal, Production
from Language.Parser.lr1_item import LR1Item
from typing import Dict, List, Tuple, Set


class NFA:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.extended_grammar()

        start = self.grammar.start

        initial_items = {start: [LR1Item(start.productions[0], 0, Terminal('$', '$'))]}

        for non_term in self.grammar.non_terminal_list:
            initial_items[non_term] = []
            for prod in non_term.productions:
                initial_items[non_term].append(LR1Item(prod, 0))

        initial_state = State(initial_items[start])
        initial_state.build(initial_items)

        list_states = [initial_state]
        dict_states = {initial_state: initial_state}
        list_states_aux = list_states[:]

        while len(list_states_aux) != 0:
            state = list_states_aux[0]
            list_states_aux = list_states_aux[1:] if len(list_states_aux) >= 1 else []

            for sym in state.expected_symbols:
                state.go_to(sym, dict_states, list_states, list_states_aux, initial_items)

        self.list_states = list_states

    def extended_grammar(self):
        new_production = Production([self.grammar.start])
        new_production.set_builder(self.grammar.start.productions[0].get_ast_node_builder())
        new_non_terminal = NonTerminal('S', [new_production])
        new_production.head = new_non_terminal
        self.grammar.start = new_non_terminal
        self.grammar.non_terminal_list.append(new_non_terminal)


class State:
    def __init__(self, items: List[LR1Item]):
        self.list_items: List[LR1Item] = items
        self._repr = "".join(f"{item} |" for item in items)
        self.items = set(items)
        self.nexts: Dict[Symbol, State] = {}
        self.expected_symbols: Dict[Symbol, Set[LR1Item]] = {}
        self.number: int = 0
        self.hash: int = hash(self._repr)

    def __hash__(self):
        return self.hash

    def __eq__(self, o):
        if isinstance(o, State):
            return self._repr == o._repr
        return False

    def __repr__(self):
        return self._repr

    def __str__(self):
        return self._repr

    def add_item(self, item: LR1Item):
        self.items.add(item)

    def build(self, initial_items: Dict[NonTerminal,List[LR1Item]]):
        aux = self.list_items[:]

        while len(self.list_items) != 0:
            item = aux[0]
            aux = aux[1:] if len(aux) >= 1 else []
            sym = item.get_symbol_at_dot()

            sym =item.get_symbol_at_dot()

            if sym is None:
                continue
            if sym in self.expected_symbols:
                self.expected_symbols[sym].add(item)
            else:
                self.expected_symbols[sym] = {item}

            if not sym.is_terminal():
                for i in initial_items[sym]:
                    lookahead = item.lookahead if item.dot_index + \
                                                  1 == len(item.production.symbols) else item.production.symbols[
                        item.dot_index + 1]
                    new_item = LR1Item(i.production, i.dot_index, lookahead)
                    if new_item not in self.items:
                        self.add_item(new_item)
                        aux.append(new_item)

    def go_to(self, sym: Symbol, dict_states, list_states, q: List, initial_items):
        new_items = []

        for i in self.expected_symbols[sym]:
            new_item = LR1Item(i.production, i.dot_index + 1, i.lookahead)
            new_items.append(new_item)
        new_state = State(new_items)

        if new_state not in dict_states:
            new_state.number = len(dict_states)
            new_state.build(initial_items)
            dict_states[new_state] = new_state
            list_states.append(new_state)
            q.append(new_state)
        else:
            new_state = dict_states[new_state]

        self.nexts[sym] = new_state


class LR1Table:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        nfa = NFA(self.grammar)

        states = nfa.list_states

        self.action_table = []
        self.go_to_table = []

        for state in states:
            state_action: Dict[str, Tuple[str, int]] = {}
            state_go_to: Dict[str, int] = {}

            for symbol in state.nexts:
                if symbol.is_terminal():
                    state_action[symbol.name] = ('S', state.nexts[symbol].number)
                else:
                    state_go_to[symbol.name] = state.nexts[symbol].number

            dict_lookahead_item: Dict[Terminal, LR1Item] = {}
            for item in state.items:
                if item.dot_index == len(item.production.symbols):
                    if item.lookahead in dict_lookahead_item:
                        raise Exception('Reduce-Reduce Conflict')
                    dict_lookahead_item[item.lookahead] = item

            for l in dict_lookahead_item:
                if l in state_action:
                    raise Exception('Shift-Reduce Conflict ')
                state_action[l.name] = ('R', dict_lookahead_item[l].production.id)
                if l.name == '$' and dict_lookahead_item[l].production.head.name == 'S':
                    state_action[l.name] = ('OK', 0)
