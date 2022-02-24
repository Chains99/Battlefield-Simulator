from abc import ABC
from dataclasses import dataclass
from typing import List


@dataclass
class AST_Node(ABC):
    pass


@dataclass
class Statement(AST_Node):
    pass


class Expression(AST_Node):
    pass


class FuncDef(AST_Node):
    def __init__(self):
        name: str
        return_type: str
        arg_names: List[str]
        arg_types: List[str]
        body: List[Statement]


@dataclass
class Script(AST_Node):
    statements: List[Statement]


@dataclass
class If(Statement):
    condition: Expression
    body: List[Statement]


@dataclass
class El_if_se(Statement):
    ifs: List[If]
    el_if_se_body: List[Statement]


@dataclass
class WhileDef(Statement):
    condition: Expression
    body: List[Statement]


@dataclass
class Decl(Statement):
    type: str
    name: str
    expression: Expression


@dataclass
class Assign(Statement):
    name: str
    expression: Expression


@dataclass
class Return(Statement):
    expression: Expression


@dataclass
class Break(Statement):
    pass


@dataclass
class Continue(Statement):
    pass


# BinaryExpressions

@dataclass
class BinaryExpression(Expression):
    op: str
    left: Expression
    right: Expression


@dataclass
class AritmeticBinaryExpression(BinaryExpression):
    pass


@dataclass
class TernaryExpression(Expression):
    left: Expression
    condition: Expression
    right: Expression


# Atomics
@dataclass
class Inversion_Symbol(Expression):
    expression: Expression


@dataclass
class Arguments(Expression):
    expression: Expression
    name: str
    args: List[Expression]


@dataclass
class Variable(Expression):
    name: str


@dataclass
class Number(Expression):
    value: str


@dataclass
class Bool(Expression):
    value: str


@dataclass
class _None(Expression):
    pass


@dataclass
class _List(Expression):
    inner_list: List[Expression]


@dataclass
class ReturnType:
    type: str


@dataclass
class Type:
    type: str


@dataclass
class Params:
    type: str
    name: str
    params: 'Params'


@dataclass
class Statements:
    statement: Statement
    statements: 'Statements'


@dataclass
class ElseDef:
    body: List[Statement]


@dataclass
class ElifDef:
    expression: Expression
    body: List[Statement]
    elif_def: 'ElifDef'
    else_def: ElseDef


@dataclass
class Expressions:
    expression: Expression
    expressions: 'Expressions'


@dataclass
class Functions:
    function: FuncDef
    functions: 'Functions'


# AST builder:

def get_functions(list_func: List, functions):
    list_func.append(functions.function)
    if functions.functions is not None:
        get_functions(list_func, functions.function)
    return list_func


def get_statements(list_statements: List, statements: Statements):
    list_statements.append(statements.statement)
    if statements.statements is not None:
        get_statements(list_statements, statements.statements)
    return list_statements


def get_params(list_params: List, params: Params):
    list_params.append((params.name, params.type))
    if params.params is not None:
        get_params(list_params, params.params)
    return list_params


def get_branch(br: El_if_se, elif_def: ElifDef):
    br.ifs.append(If(elif_def.expression, elif_def.body))
    if elif_def.elif_def is not None:
        get_branch(br, elif_def.elif_def)
    elif elif_def.else_def is not None:
        br.else_body = elif_def.else_def.body


def get_expressions(list_expressions: List, expressions: Expressions):
    list_expressions.append(expressions.expression)
    if expressions.expressions is not None:
        get_expressions(list_expressions, expressions.expressions)
    return list_expressions


def build_script_file(tokens: List[str], nodes: List):
    statements = nodes.pop()
    script = Script(get_statements([], statements))
    nodes.append(script)


def build_statements(tokens: List[str], nodes: List):
    statements = nodes.pop()
    statement = nodes.pop()
    statements = Statements(statement, statements)
    nodes.append(statements)


def build_simple_statements(tokens: List[str], nodes: List):
    statement = nodes.pop()
    statements = Statements(statement, None)
    nodes.append(statements)


def build_type(tokens: List[str], nodes: List):
    type = Type(tokens[len(tokens) - 1])
    nodes.append(type)


def build_break(tokens: List[str], nodes: List):
    nodes.append(Break())


def build_params_1(tokens: List[str], nodes: List):
    params = nodes.pop()
    type = nodes.pop()
    params = Params(type.type, tokens[len(tokens) - 2], params)
    nodes.append(params)


def build_params_2(tokens: List[str], nodes: List):
    type = nodes.pop()
    params = Params(type.type, tokens[len(tokens) - 1], None)
    nodes.append(params)


def build_func_def_1(tokens: List[str], nodes: List):
    name = tokens[len(tokens) - 8]
    block = nodes.pop()
    params = get_params([], nodes.pop())
    arg_names = [t[0] for t in params]
    arg_types = [t[1] for t in params]
    return_type = nodes.pop()
    func_def = FuncDef(name, return_type.type, arg_names,
                       arg_types, get_statements([], block))
    nodes.append(func_def)


def build_func_def_2(tokens: List[str], nodes: List):
    name = tokens[len(tokens) - 6]
    block = nodes.pop()
    return_type = nodes.pop()
    func_def = FuncDef(name, return_type.type, [], [],
                       get_statements([], block))
    nodes.append(func_def)


def build_return_type(tokens: List[str], nodes: List):
    top = tokens[len(tokens) - 1]
    if top == 'void':
        nodes.append(ReturnType(top))
    else:
        type = nodes.pop()
        nodes.append(ReturnType(type.type))


def build_continue(tokens: List[str], nodes: List):
    nodes.append(Continue())


def build_if_def_1(tokens: List[str], nodes: List):
    elif_def = nodes.pop()
    block = nodes.pop()
    expression = nodes.pop()

    if_def = If(expression, get_statements([], block))
    branch = El_if_se([if_def], None)

    get_branch(branch, elif_def)

    nodes.append(branch)


def build_if_def_2(tokens: List[str], nodes: List):
    else_def = nodes.pop()
    block = nodes.pop()
    expression = nodes.pop()

    if_def = If(expression, get_statements([], block))
    branch = El_if_se([if_def], else_def.body)

    nodes.append(branch)


def build_if_def_3(tokens: List[str], nodes: List):
    block = nodes.pop()
    expression = nodes.pop()

    if_def = If(expression, get_statements([], block))
    branch = El_if_se([if_def], None)

    nodes.append(branch)


def build_elif_def_1(tokens: List[str], nodes: List):
    elif_def = nodes.pop()
    block = nodes.pop()
    expression = nodes.pop()

    elif_def = ElifDef(expression, get_statements(
        [], block), elif_def, None)

    nodes.append(elif_def)


def build_elif_def_2(tokens: List[str], nodes: List):
    else_def = nodes.pop()
    block = nodes.pop()
    expression = nodes.pop()

    elif_def = ElifDef(expression, get_statements(
        [], block), None, else_def)

    nodes.append(elif_def)


def build_elif_def_3(tokens: List[str], nodes: List):
    block = nodes.pop()
    expression = nodes.pop()

    elif_def = ElifDef(expression, get_statements([], block), None, None)

    nodes.append(elif_def)


def build_else_def(tokens: List[str], nodes: List):
    block = nodes.pop()
    else_def = ElseDef(get_statements([], block))
    nodes.append(else_def)


def build_while_def(tokens: List[str], nodes: List):
    block = nodes.pop()
    expression = nodes.pop()

    while_def = WhileDef(expression, get_statements([], block))

    nodes.append(while_def)


def build_decl(tokens: List[str], nodes: List):
    expression = nodes.pop()
    type = nodes.pop()
    name = tokens[len(tokens) - 3]

    assign = Decl(type.type, name, expression)

    nodes.append(assign)


def build_assign(tokens: List[str], nodes: List):
    expression = nodes.pop()
    name = tokens[len(tokens) - 3]

    assign = Assign(name, expression)

    nodes.append(assign)


def build_return_1(tokens: List[str], nodes: List):
    expression = nodes.pop()
    return_stm = Return(expression)
    nodes.append(return_stm)


def build_return_2(tokens: List[str], nodes: List):
    return_stm = Return(None)
    nodes.append(return_stm)


def build_expressions_1(tokens: List[str], nodes: List):
    expressions = nodes.pop()
    expression = nodes.pop()
    expressions = Expressions(expression, expressions)
    nodes.append(expressions)


def build_expressions_2(tokens: List[str], nodes: List):
    expression = nodes.pop()
    expressions = Expressions(expression, None)
    nodes.append(expressions)


def build_ternary_expression(tokens: List[str], nodes: List):
    right = nodes.pop()
    condition = nodes.pop()
    left = nodes.pop()

    ternexp = TernaryExpression(left, condition, right)

    nodes.append(ternexp)


def build_or(tokens: List[str], nodes: List):
    right = nodes.pop()
    left = nodes.pop()

    binexp = BinaryExpression('or', left, right)

    nodes.append(binexp)


def build_and(tokens: List[str], nodes: List):
    right = nodes.pop()
    left = nodes.pop()

    binexp = BinaryExpression('and', left, right)

    nodes.append(binexp)


def build_inversion(tokens: List[str], nodes: List):
    expr = nodes.pop()
    inversion = Inversion_Symbol(expr)
    nodes.append(inversion)


def build_comparison(tokens: List[str], nodes: List):
    right = nodes.pop()
    left = nodes.pop()

    arith_exp = AritmeticBinaryExpression(tokens[len(tokens) - 2], left, right)

    nodes.append(arith_exp)


def build_aritmetic_expression(tokens: List[str], nodes: List):
    right = nodes.pop()
    left = nodes.pop()
    op = tokens[len(tokens) - 2]

    arith_exp = AritmeticBinaryExpression(op, left, right)

    nodes.append(arith_exp)


def build_basic_1(tokens: List[str], nodes: List):
    exp = nodes.pop()
    name = tokens[len(tokens) - 1]

    args = Arguments(exp, name, None)

    nodes.append(args)


def build_basic_2(tokens: List[str], nodes: List):
    expressions = nodes.pop()
    exp = nodes.pop()

    args = Arguments(exp, None, get_expressions([], expressions))

    nodes.append(args)


def build_basic_3(tokens: List[str], nodes: List):
    exp = nodes.pop()

    args = Arguments(exp, None, [])

    nodes.append(args)


def build_basic_4(tokens: List[str], nodes: List):
    exp = Variable('self')
    name = tokens[len(tokens) - 1]

    args = Arguments(exp, name, None)

    nodes.append(args)


def build_Variable(tokens: List[str], nodes: List):
    nodes.append(Variable(tokens[len(tokens) - 1]))


def build_Bool(tokens: List[str], nodes: List):
    nodes.append(Bool(tokens[len(tokens) - 1]))


def build_Number(tokens: List[str], nodes: List):
    nodes.append(Number(tokens[len(tokens) - 1]))


def build_None(tokens: List[str], nodes: List):
    nodes.append(_None())


def build_list_1(tokens: List[str], nodes: List):
    expressions = nodes.pop()
    exp_list = _List(get_expressions([], expressions))
    nodes.append(exp_list)


def build_list_2(tokens: List[str], nodes: List):
    exp_list = _List([])
    nodes.append(exp_list)


def build_functions_1(tokens: List[str], nodes: List):
    functions = nodes.pop()
    func = nodes.pop()

    functions = Functions(func, functions)

    nodes.append(functions)


def build_functions_2(tokens: List[str], nodes: List):
    func = nodes.pop()

    functions = Functions(func, None)

    nodes.append(functions)
