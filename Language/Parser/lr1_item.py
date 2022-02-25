from Language.Grammar.grammar import Production,Symbol

class LR1Item:
    def __init__(self, production: Production, dot_index: int, lookahead:str=None):
        self.production=production
        self.dot_index=dot_index
        self.lookahead=lookahead
        self._repr=None
    
    def __repr__(self) -> str:
        if not self._repr:
            return self._repr
        
        repr_ = f"{self.production.head} -> "
        repr_ += " ".join(str(i) for i in self.production.symbols[: self.dot_pos])
        repr_ += " . "
        repr_ += " ".join(str(i) for i in self.production.symbols[self.dot_pos :])

        if not self.lookahead:
            repr_ += f" [{self.lookahead}]"

        self._repr = f"LRItem({repr_})"

        return self._repr
    
    def get_symbol_at_dot(self)->Symbol:
        if self.dot_index<len(self.production.symbols):
            return self.production.symbols[self.dot_index]
        return None


    def __hash__(self):
        return hash(self.__repr__())


    