from lib2to3.pgen2 import grammar
from typing import Set,Dict,List
from Language.Grammar.grammar import Grammar,Production,Symbol,NonTerminal, Terminal, bfs_start
from Language.Parser.lr1_item import LR1Item
import json

class LR1Table:
    def __init__(self,grammar: Grammar):
        self.grammar=grammar
        self.first=None
        self.follow=None
        self._hash=None
        self.dict_states_id: Dict[int,List[LR1Item]]={}
        self.dict_states_hash={}
        self.dict_clousure_hash={}
        self.dict_lr1_items={}
        self.extend_grammar()

        return self.build_table()

    
    def build_table(self):
        self.first=self.calculate_first()
        self.follow=self.calculate_follow()
        lr1_items=self.get_all_lr1_items()

    def extend_grammar():
        new_production=Production(bfs_start)
        new_non_terminal=NonTerminal('S', list(new_production))

    
    def get_all_lr1_items(self):
        lr1_items = []
        self._item_prods = {}
        for prod in self.grammar.get_productions():
            for dot_pos in range(len(prod.symbols) + 1):
                item_prod = prod
                slr_item = LR1Item(item_prod, dot_pos)
                lr1_items.append(slr_item)
                if prod.head not in self._item_prods:
                    self._item_prods[prod.head] = []
                self._item_prods[prod.head.name].append(item_prod)
        return lr1_items

    def calculate_first(self):
        first = {prod.head.name: Set[Terminal] for prod in self.grammar.get_productions()}
        prod_first = {prod: Set[Terminal] for prod in self.grammar.get_productions()}

        change = True
        while change:
            change = False
            for prod in self.grammar.get_productions():
                head=prod.head
                head_name=prod.head.name
                for item in prod.symbols:
                    if item.is_terminal:
                        change |= first[head_name].add(item)
                        prod_first[prod].add(item)
                        break
                    if item != head:
                        change |= first[head.name].update(first[item.name])
                        prod_first[prod].update(first[item.name])
                    if "EPS" not in first[head.name]:
                        break
        return first       

    def calculate_follow(self):
        if first is None:
            first = self.calculate_first()

            follow = {non_term.name: Set[Terminal] for non_term in self.grammar.non_terminal_list}
            follow[bfs_start.name].add(Terminal("$"))

            change = True
            while change:
                change = False
                for prod in self.grammar.get_productions():
                    prod_head=prod.head
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

    def get_no_state(self,items:Set[LR1Item]) -> int: 
        hash_ = self.get_items_hash(items)
        if hash_ in self.dict_states_hash:
            return self.dict_states_hash[hash_]
        number = len(self.dict_states_id)
        self.dict_states_id[number] = items
        self.dict_states_hash[hash_] = number
        return number

    def build_table(self):
        self.first= self.calculate_first()
        self.follow=self.calculate_follow()

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
                rest = item.production.symbols[item.dot_index + 1 :]
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

    def is_in_first(self):
        pass

    def get_items_hash(self,items:Set[LR1Item]):
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

        