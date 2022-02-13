from Grammar.grammar import Production, Terminal, Grammar, NonTerminal
from collections import deque


# ItemLR1 to define items used on LR(1) parsing
class ItemLR:
    def __init__(self, production, index, lookahead=None):
        super().__init__(production)
        self.string = f"{production.head} --> "
        self.lookahead = lookahead
        self.index = index

        for i in range(index):
            self.string += f"{production[i]} "

        p_total = len(production)
        for i in range(index, p_total):
            self.string += f" {production[i]}"

        self.hash = hash(self.string)

        self.string += f", {self.lookahead}"

    def __hash__(self):
        return self.hash

    def __str__(self):
        return self.string


class State:

    def __init__(self, kernel):
        self.string = ""
        self.next_states = {}
        self.expected_elements = {}
        self.number = 0
        self.kernel = kernel
        self.items = set(kernel)

        for item in kernel:
            self.string += f"{item} |"

        self.hash = hash(self.string)

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def add_itemLR(self, item):
        self.items.add(item)

    def build(self, items):
        queue = deque(self.kernel)

        while len(queue) != 0:

            item = queue.popleft()
            if item.index == len(item.production):
                continue

            element = item.production[item.index]

            if element in self.expected_elements:
                self.expected_elements[element].add(item)
            else:
                self.expected_elements[element] = {item}

            if not element.is_terminal:
                for i in items[element]:
                    lookahead = item.lookahead if item.index + \
                                                  1 == len(item.production) else item.production[item.index + 1]
                    new_item = ItemLR(i.production, i.index, lookahead)
                    if new_item not in self.items:
                        self.add_itemLR(new_item)
                        queue.append(new_item)

    def go_to(self, states, states_list, initial_items, queue, elements):
        new_kernel = []

        for i in self.expected_elements[elements]:
            new_item = ItemLR(i.production, i.index + 1, i.lookahead)
            new_kernel.append(new_item)
        new_state = State(new_kernel)

        if new_state not in states:
            new_state.number = len(states)
            new_state.build(initial_items)
            states[new_state] = new_state
            states_list.append(new_state)
            queue.append(new_state)
        else:
            new_state = states[new_state]

        self.next_states[elements] = new_state


class Automata:

    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def create(self):

        start = NonTerminal('R')
        start += Production([self.grammar.first])

        initial_items = {start: [ItemLR(start[0], 0, Terminal('$'))]}

        for non_terminal in self.grammar.get_non_terminals():
            initial_items[non_terminal] = []
            for prod in non_terminal.productions:
                initial_items[non_terminal].append(ItemLR(prod, 0))

        first_el = State(initial_items[start])

        states_dict = {first_el: first_el}
        states_list = [first_el]

        queue = deque(states_list)

        while len(queue) != 0:
            state = queue.popleft()
            state.build(initial_items)
            for sym in state.expected_elements:
                state.go_to(sym, states_dict, states_list)

        return states_list


class Table_Go_To_Action:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def build(self):
        states = Automata(self.grammar).create()

        go_to = []
        action = []

        for state in states:
            state_action = {}
            state_go_to = {}
            lookA_item = {}

            # for element_item in state.items:
            #     if element_item.index == len(element_item.production):
            #         if element_item.lookahead in lookA_item:
            #             raise Exception('There has been a Reduce-Reduce conflict')
            #         lookA_item[element_item.lookahead] = element_item

            for next_element in state.next_states:
                if next_element.is_terminal:
                    state_action[next_element.name] = ('R', state.next_states[next_element].number)
                else:
                    state_go_to[next_element.name] = state.next_states[next_element].number

            go_to.append(state_go_to)

            action.append(state_action)
