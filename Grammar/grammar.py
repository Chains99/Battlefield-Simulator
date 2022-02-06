from typing import List, Dict


class Terminal:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class Production:

    def __init__(self, terminals: List[Terminal]):
        self.terminals = terminals


class NonTerminal:
    def __init__(self, name: str, prodsList: List[Production]):
        self.name = name
        self.productions = prodsList

    def __iadd__(self, prod: Production):
        self.add(prod)
        return self


class Grammar:
    def __init__(self, nonTList: List[NonTerminal]):
        self.nonTList = nonTList


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
statements = NonTerminal('statements')
statement = NonTerminal('statement')
comparision = NonTerminal('comparision')
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
