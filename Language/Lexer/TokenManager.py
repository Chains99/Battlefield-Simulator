class Token_Manager:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = 0

    def eot(self):
        return self.current_pos == len(self.tokens)

    def can_look_ahead(self, k):
        return len(self.tokens) - self.current_pos > k

    def look_ahead(self, k):
        return self.tokens[self.current_pos + k]

    def current(self):
        return self.tokens[self.current_pos]

    def next_token(self):
        if self.current_pos < len(self.tokens):
            self.current_pos += 1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        tokens = ""
        for token in self.tokens:
            tokens += token.__str__() + ', '
        return tokens
