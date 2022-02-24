from typing import List, Dict, Set, Optional, Callable
from abc import ABCMeta, abstractmethod

from language.parser.ast import build_statements, build_simple_statements, build_break, build_continue, \
    build_ternary_expression, build_expressions_1, build_expressions_2, build_func_def_1, build_func_def_2, \
    build_if_def_1, build_if_def_2, build_if_def_3, build_elif_def_1, build_elif_def_2, build_elif_def_3, \
    build_else_def, build_while_def, build_and, build_or, build_inversion, build_comparison, build_aritmetic_expression, \
    build_basic_1, build_basic_2, build_basic_3, build_Variable, build_Bool, build_None, build_Number, build_list_1, \
    build_list_2


class Symbol(metaclass=ABCMeta):
    def __init__(self, name: str) -> None:
        self.name = name
        self.ast = None

    def is_terminal(self) -> bool:
        return isinstance(self, Terminal)

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def ast(self):
        if self.is_terminal:
            return self
        return self.ast

    @abstractmethod
    def copy(self):
        pass


class Terminal(Symbol):
    def __init__(self, name: str, value: str) -> None:
        super().__init__(name)
        self.value = value

    def copy(self):
        return Terminal(self.name, self.value)

    def __repr__(self) -> str:
        return f"T-{super().__repr__()}"


class Production:

    def __init__(self, symbols: List[Symbol], ast_node_builder=None):
        self.head: NonTerminal = None
        self.symbols: List[Symbol] = symbols
        ast_node_builder = ast_node_builder

    def get_terminals(self) -> Set[Terminal]:
        terminals: Set = set()
        for symbol in self.symbols:
            if (isinstance(symbol, Terminal)):
                terminals.update(symbol)
        return terminals

    def set_builder(self, func: Callable):
        self.ast_node_builder = func

    def get_ast_node_builder(self):
        if self.ast_node_builder is None:
            raise ValueError("Builder function not set.")
        return self.set_builder

    def copy(self):
        pass


class NonTerminal(Symbol):
    def __init__(self, name: str, prodsList: Optional[List[Production]]):
        super().__init__(name)
        self.name = name
        self.productions = prodsList
        self._terminals_set: Set = set()

    def __iadd__(self, prod: Production):
        self.productions.append(prod)
        self._terminals_set.update(prod.get_terminals())
        prod.head = self
        return self

    def set_ast(self, ast):
        self._ast = ast


class Grammar:
    def __init__(self, non_terminal_list: List[NonTerminal]):
        self.non_terminal_list = non_terminal_list

    def get_productions(self) -> List[Production]:
        prods = []
        for non_term in self.non_terminal_list:
            prods.extend(non_term.productions)
        return prods

    def get_terminals(self) -> Set[Terminal]:
        terminals = set()
        for non_term in self.non_terminal_list:
            terminals.update(non_term._terminals_set)
        return terminals


# GRAMMAR

# Terminals
eof = Terminal("EOF", "EOF")
identifier = ('IDENTIFIER')
semicolon_t = Terminal(';', ';')
comma_t = Terminal(',', ',')
none_t = Terminal('None', 'None')
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
number_t = Terminal('Number', 'Number')
name_t = Terminal('name', 'name')
bool_t = Terminal('bool', 'bool')
void_t = Terminal('void', 'void')
is_t = Terminal('is', 'is')
assign_t = Terminal('=', '=')
dot = Terminal('.', '.')
add_t = Terminal('+', '+')
sub_t = Terminal('-', '-')
mul_t = Terminal('*', '*')
div_t = Terminal('/', '/')
pow_t = Terminal("^", "^")
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
continue_t = Terminal('continue', 'continue')
list_t = Terminal('List', 'List')

# NonTerminals
pow_nt = NonTerminal("pow")
disjunction = NonTerminal("disjunction")
conjunction = NonTerminal("conjunction")
inversion = NonTerminal("inversion")
bfs_start = NonTerminal('bfs_start')
statements = NonTerminal('statements')
statement = NonTerminal('statement')
comparison = NonTerminal('comparison')
expression = NonTerminal('expression')
expressions = NonTerminal('expressions')
assign = NonTerminal('assign')
fun_def = NonTerminal('fun_def')
if_def = NonTerminal('if_def')
elif_def = NonTerminal('elif_def')
else_def = NonTerminal('else_def')
while_def = NonTerminal('while_def')
type_nt = NonTerminal('type')
atom = NonTerminal('atom')
params = NonTerminal('params')
sum_nt = NonTerminal("sum")
term = NonTerminal('term')
factor = NonTerminal('factor')
basic = NonTerminal('basic')

# grammar start
bfs_start += Production(statements)

# Productions

# statements
statements += Production([statement, semicolon_t, statements], build_statements)
statements += Production([statement, semicolon_t], build_simple_statements)

statement += Production([fun_def])
statement += Production([while_def])
statement += Production([break_t], build_break)
statement += Production([if_def])
statement += Production([assign])
statement += Production([expressions])
statement += Production([continue_t], build_continue)

expression += Production([disjunction, if_t, disjunction,
                          else_t, expression], build_ternary_expression)
expression += Production([disjunction])

expressions += Production([expression, comma_t, expressions], build_expressions_1)
expressions += Production([expression], build_expressions_2)

# Function Definition
fun_def += Production([def_t, fun_type, name_t, openBracket_t, params, closedBracket_t, openCurlyBraces_t, statements,
                       closedCurlyBraces_t], build_func_def_1)
fun_def += Production(
    [def_t, fun_type, name_t, openBracket_t, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t],
    build_func_def_2)

# Function Type
fun_type += Production([type_nt])
fun_type += Production([void_t])

# Function Params
params += Production([type_nt, name_t, comma_t, params])
params += Production([type_nt, name_t])

# if Definition
if_def += Production([if_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t, elif_def],
                     build_if_def_1)
if_def += Production(
    [if_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t, else_def],
    build_if_def_2)
if_def += Production(
    [if_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t],
    build_if_def_3)

# elif Definition
elif_def += Production(
    [elif_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t, elif_def],
    build_elif_def_1)
elif_def += Production(
    [elif_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t, else_def],
    build_elif_def_2)
elif_def += Production(
    [elif_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t],
    build_elif_def_3)

# else Definition
else_def += Production([else_t, openCurlyBraces_t, statements, closedCurlyBraces_t], build_else_def)

# while Definition
while_def += Production(
    [while_t, openBracket_t, expression, closedBracket_t, openCurlyBraces_t, statements, closedCurlyBraces_t],
    build_while_def)

type_nt += Production([bool_t])
type_nt += Production([name_t])

# logical accumulators
disjunction += Production([conjunction, or_t, disjunction], build_or)
disjunction += Production([conjunction])

conjunction += Production([inversion, and_t, conjunction], build_and)
conjunction += Production([inversion])

inversion += Production([not_t, inversion], build_inversion)
inversion += Production([comparison])

comparison += Production([sum_nt, eq_t, sum_nt], build_comparison)
comparison += Production([sum_nt, ne_t, sum_nt], build_comparison)
comparison += Production([sum_nt, le_t, sum_nt], build_comparison)
comparison += Production([sum_nt, lt_t, sum_nt], build_comparison)
comparison += Production([sum_nt, ge_t, sum_nt], build_comparison)
comparison += Production([sum_nt, gt_t, sum_nt], build_comparison)
comparison += Production([sum_nt])

sum_nt += Production([sum_nt, add_t, term], build_aritmetic_expression)
sum_nt += Production([sum_nt, sub_t, term], build_aritmetic_expression)
sum_nt += Production([term])

# arithmetic accumulators
term += Production([term, mul_t, factor], build_aritmetic_expression)
term += Production([term, div_t, factor], build_aritmetic_expression)
term += Production([term, mod_t, factor], build_aritmetic_expression)
term += Production([factor])

factor += Production([add_t, factor])
factor += Production([sub_t, factor])
factor += Production([pow_t])

pow_nt += Production([basic, pow_t, factor], build_aritmetic_expression)
pow_nt += Production([basic])

# basic indexing and attributes consultation
basic += Production([basic, dot, identifier], build_basic_1)
basic += Production([basic, openBracket_t, expressions, closedBracket_t], build_basic_2)
basic += Production([basic, openBracket_t, closedBracket_t], build_basic_3)
basic += Production([atom])

# atomic types
atom += Production([identifier], build_Variable)
atom += Production([true_t], build_Bool)
atom += Production([false_t], build_Bool)
atom += Production([none_t], build_None)
atom += Production([number_t], build_Number)
atom += Production([list_t])

list_t += Production([openStraightBracket_t, expressions, closedStraightBracket_t], build_list_1)
list_t += Production([openStraightBracket_t, closedStraightBracket_t], build_list_2)