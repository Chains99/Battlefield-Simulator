from typing import List, Dict, Set
from abc import ABCMeta, abstractmethod

class Symbol(metaclass=ABCMeta):
    def __init__(self,name:str) -> None:
        self.name=name

    def is_terminal(self) -> bool:
        return isinstance(self,Terminal)

    def __repr__(self) -> str:
        return self.name
    
    def __hash__(self) -> int:
        return self.__repr__()

    @abstractmethod
    def copy(self):
        pass


class Terminal(Symbol):
    def __init__(self, name: str, value: str) -> None:
        super().__init__(name)
        self.value=value
    
    def copy(self):
        return Terminal(self.name, self.value)

    def __repr__(self) -> str:
        return f"T-{super().__repr__()}"


class Production:

    def __init__(self, symbols: List[Symbol],):
        self.head: NonTerminal = None
        self.symbols: List[Symbol] = symbols

    def get_terminals(self) -> Set[Terminal]:
        terminals: Set = {}
        for symbol in self.symbols:
            if(isinstance(symbol,Terminal)):
                terminals.update(symbol)
        return terminals
        
    
    def copy(self):
        pass


class NonTerminal(Symbol):
    def __init__(self, name: str, prodsList: List[Production]):
        self.name = name
        self.productions = prodsList
        self._terminals_set: Set={}

    def __iadd__(self, prod: Production):
        self.productions.append(prod)
        self._terminals_set.update(prod.get_terminals())
        prod.head=self
        return self


class Grammar:
    def __init__(self, non_terminal_list: List[NonTerminal]):
        self.non_terminal_list = non_terminal_list
    
    def get_productions(self) -> List[Production]:
        prods=[]
        for non_term in self.non_terminal_list:
            prods.extend(non_term.productions)
        return prods

    def get_terminals(self) -> Set[Terminal]:
        terminals={}
        for non_term in self.non_terminal_list:
            terminals.update(non_term._terminals_set)
        return terminals

    


# GRAMMAR

# Terminals
semicolon_t = Terminal(';', ';')
comma_t = Terminal(',', ',')
if_t = Terminal('if', 'if')
else_t = Terminal('else', 'else')
elif_t = Terminal('elif', 'elif')
def_t = Terminal('def', 'def')
true_t = Terminal('true', 'true')
false_t = Terminal('false', 'false')
while_t = Terminal('while', 'while')
break_t = Terminal('break', 'break')
return_t = Terminal('return', 'return')
fun_type = Terminal('fun_type', 'fun_type')
name_t = Terminal('name', 'name')
bool_t = Terminal('bool', 'bool')
void_t = Terminal('void', 'void')
is_t = Terminal('is', 'is')
assign_t = Terminal('=', '=')
add_t = Terminal('+', '+')
sub_t = Terminal('-', '-')
mul_t = Terminal('*', '*')
div_t = Terminal('/', '/')
mod_t = Terminal('%', '%')
eq_t = Terminal('==', '==')
ne_t = Terminal('!=', '!=')
lt_t = Terminal('<', '<')
gt_t = Terminal('>', '>')
le_t = Terminal('<=', '<=')
ge_t = Terminal('>=', '>=')
and_t = Terminal('and', 'and')
or_t = Terminal('or', 'or')
not_t = Terminal('not', 'not')
openBracket_t = Terminal('(', '(')
closedBracket_t = Terminal(')', ')')
openCurlyBraces_t = Terminal('{', '{')
closedCurlyBraces_t = Terminal('}', '}')
openStraightBracket_t = Terminal('[', '[')
closedStraightBracket_t = Terminal(']', ']')

# NonTerminals
bfs_start=NonTerminal('bfs_start')
statements = NonTerminal('statements')
statement = NonTerminal('statement')
comparison = NonTerminal('comparison')
expression = NonTerminal('expression')
expressions = NonTerminal('expressions')
assign = NonTerminal('assign')
fun_def = NonTerminal('fun_def')
fun_type + NonTerminal('fun_type')
if_def = NonTerminal('if_def')
elif_def = NonTerminal('elif_def')
else_def = NonTerminal('else_def')
while_def = NonTerminal('while_def')
type_nt = NonTerminal('type', 'type')
atom = NonTerminal('atom')
params = NonTerminal('params')


# grammar start
bfs_start += Production(statements)

# Productions

# statements
statements += Production([statement, semicolon_t, statements])
statements += Production([statement, semicolon_t])

statement += Production([fun_def])
statement += Production([while_def])
statement += Production([break_t])
statement += Production([if_def])
statement += Production([assign])
statement += Production([expressions])

expressions += Production([expression, comma_t, expressions])
expressions += Production([expression])

# Function Definition
fun_def += Production([def_t, fun_type, name_t, openBracket_t, params, closedBracket_t, openCurlyBraces_t, statements,
                       closedCurlyBraces_t])
fun_def += Production(
    [def_t, fun_type, name_t, openBracket_t, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t])

# Function Type
fun_type += Production([type_nt])
fun_type += Production([void_t])

# Function Params
params += Production([type_nt, name_t, comma_t, params])
params += Production([type_nt, name_t])

# if Definition
if_def += Production([if_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t, elif_def])
if_def += Production(
    [if_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t, else_def])
if_def += Production(
    [if_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t])

# elif Definition
elif_def += Production(
    [elif_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t, elif_def])
elif_def += Production(
    [elif_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t, else_def])
elif_def += Production(
    [elif_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t])

# else Definition
else_def += Production([else_t, openCurlyBraces_t, statements, closedCurlyBraces_t])

# while Definition
while_def += Production(
    [while_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t])

type_nt += Production([bool_t])
type_nt += Production([name_t])
