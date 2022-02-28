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


@dataclass
class FuncDef(AST_Node):
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
class String(Expression):
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
class BetwBrackExpression(Expression):
    expression: Expression


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


# AST builder:
def build_script_file(tokens: List[str], ast_nodes: List):
    statements = ast_nodes.pop()
    script = Script(get_statements([], statements))
    ast_nodes.append(script)


def build_statements(tokens: List[str], ast_nodes: List):
    statements = ast_nodes.pop()
    statement = ast_nodes.pop()
    statements = Statements(statement, statements)
    ast_nodes.append(statements)


def build_simple_statements(tokens: List[str], ast_nodes: List):
    statement = ast_nodes.pop()
    statements = Statements(statement, None)
    ast_nodes.append(statements)


def build_type(tokens: List[str], ast_nodes: List):
    type = Type(tokens[len(tokens) - 1])
    ast_nodes.append(type)


def build_break(tokens: List[str], ast_nodes: List):
    ast_nodes.append(Break())


def build_params_1(tokens: List[str], ast_nodes: List):
    params = ast_nodes.pop()
    type = ast_nodes.pop()
    params = Params(type.type, tokens[len(tokens) - 3], params)
    ast_nodes.append(params)


def build_params_2(tokens: List[str], ast_nodes: List):
    type = ast_nodes.pop()
    params = Params(type.type, tokens[len(tokens) - 1], None)
    ast_nodes.append(params)


def build_func_def_1(tokens: List[str], ast_nodes: List):
    name = tokens[len(tokens) - 8]
    block = ast_nodes.pop()
    params = get_params([], ast_nodes.pop())
    arg_names = [param[0] for param in params]
    arg_types = [param[1] for param in params]
    return_type = ast_nodes.pop()
    func_def = FuncDef(name, return_type.type, arg_names,
                       arg_types, get_statements([], block))

    ast_nodes.append(func_def)


def build_func_def_2(tokens: List[str], ast_nodes: List):
    name = tokens[len(tokens) - 6]
    block = ast_nodes.pop()
    return_type = ast_nodes.pop()
    func_def = FuncDef(name, return_type.type, [], [],
                       get_statements([], block))
    ast_nodes.append(func_def)


def build_fun_type(tokens: List[str], ast_nodes: List):
    token = tokens[len(tokens) - 1]
    if token == 'void':
        ast_nodes.append(ReturnType(token))
    else:
        type = ast_nodes.pop()
        ast_nodes.append(ReturnType(type.type))


def build_continue(tokens: List[str], ast_nodes: List):
    ast_nodes.append(Continue())


def build_if_def_1(tokens: List[str], ast_nodes: List):
    elif_def = ast_nodes.pop()
    block = ast_nodes.pop()
    expression = ast_nodes.pop()

    if_def = If(expression, get_statements([], block))
    branch = El_if_se([if_def], None)

    get_branch(branch, elif_def)

    ast_nodes.append(branch)


def build_if_def_2(tokens: List[str], ast_nodes: List):
    else_def = ast_nodes.pop()
    block = ast_nodes.pop()
    expression = ast_nodes.pop()

    if_def = If(expression, get_statements([], block))
    branch = El_if_se([if_def], else_def.body)

    ast_nodes.append(branch)


def build_if_def_3(tokens: List[str], ast_nodes: List):
    block = ast_nodes.pop()
    expression = ast_nodes.pop()

    if_def = If(expression, get_statements([], block))
    branch = El_if_se([if_def], None)

    ast_nodes.append(branch)


def build_elif_def_1(tokens: List[str], ast_nodes: List):
    elif_def = ast_nodes.pop()
    block = ast_nodes.pop()
    expression = ast_nodes.pop()

    elif_def = ElifDef(expression, get_statements(
        [], block), elif_def, None)

    ast_nodes.append(elif_def)


def build_elif_def_2(tokens: List[str], ast_nodes: List):
    else_def = ast_nodes.pop()
    block = ast_nodes.pop()
    expression = ast_nodes.pop()

    elif_def = ElifDef(expression, get_statements(
        [], block), None, else_def)

    ast_nodes.append(elif_def)


def build_elif_def_3(tokens: List[str], ast_nodes: List):
    block = ast_nodes.pop()
    expression = ast_nodes.pop()

    elif_def = ElifDef(expression, get_statements([], block), None, None)

    ast_nodes.append(elif_def)


def build_else_def(tokens: List[str], ast_nodes: List):
    block = ast_nodes.pop()
    else_def = ElseDef(get_statements([], block))
    ast_nodes.append(else_def)


def build_while_def(tokens: List[str], ast_nodes: List):
    block = ast_nodes.pop()
    expression = ast_nodes.pop()

    while_def = WhileDef(expression, get_statements([], block))

    ast_nodes.append(while_def)


def build_assign_1(tokens: List[str], ast_nodes: List):
    expression = ast_nodes.pop()
    type = ast_nodes.pop()
    name = tokens[len(tokens) - 3]

    assign = Decl(type.type, name, expression)

    ast_nodes.append(assign)


def build_assign_2(tokens: List[str], ast_nodes: List):
    expression = ast_nodes.pop()
    name = tokens[len(tokens) - 3]

    assign = Assign(name, expression)

    ast_nodes.append(assign)


def build_return_1(tokens: List[str], ast_nodes: List):
    expression = ast_nodes.pop()
    return_stm = Return(expression)
    ast_nodes.append(return_stm)


def build_return_2(tokens: List[str], ast_nodes: List):
    return_stm = Return(None)
    ast_nodes.append(return_stm)


def build_expressions_1(tokens: List[str], ast_nodes: List):
    expressions = ast_nodes.pop()
    expression = ast_nodes.pop()
    expressions = Expressions(expression, expressions)
    ast_nodes.append(expressions)


def build_expressions_2(tokens: List[str], ast_nodes: List):
    expression = ast_nodes.pop()
    expressions = Expressions(expression, None)
    ast_nodes.append(expressions)


def build_ternary_expression(tokens: List[str], ast_nodes: List):
    right = ast_nodes.pop()
    condition = ast_nodes.pop()
    left = ast_nodes.pop()

    ternexp = TernaryExpression(left, condition, right)

    ast_nodes.append(ternexp)


def build_or(tokens: List[str], ast_nodes: List):
    right = ast_nodes.pop()
    left = ast_nodes.pop()

    binexp = BinaryExpression('or', left, right)

    ast_nodes.append(binexp)


def build_and(tokens: List[str], ast_nodes: List):
    right = ast_nodes.pop()
    left = ast_nodes.pop()

    binexp = BinaryExpression('and', left, right)

    ast_nodes.append(binexp)


def build_inversion(tokens: List[str], ast_nodes: List):
    expr = ast_nodes.pop()
    inversion = Inversion_Symbol(expr)
    ast_nodes.append(inversion)


def build_betw_bracket_expression(tokens: List[str], ast_nodes: List):
    expression = ast_nodes.pop()
    ast_nodes.append(BetwBrackExpression(expression))


def build_arithmetic_logical_expression(tokens: List[str], ast_nodes: List):
    right = ast_nodes.pop()
    left = ast_nodes.pop()
    op = tokens[len(tokens) - 2]

    arith_log_exp = BinaryExpression(op, left, right)

    ast_nodes.append(arith_log_exp)


def build_basic_1(tokens: List[str], ast_nodes: List):
    exp = ast_nodes.pop()
    name = tokens[len(tokens) - 1]

    args = Arguments(exp, name, None)

    ast_nodes.append(args)


def build_basic_2(tokens: List[str], ast_nodes: List):
    expressions = ast_nodes.pop()
    exp = ast_nodes.pop()

    args = Arguments(exp, None, get_expressions([], expressions))

    ast_nodes.append(args)


def build_basic_3(tokens: List[str], ast_nodes: List):
    exp = ast_nodes.pop()

    args = Arguments(exp, None, [])

    ast_nodes.append(args)


def build_basic_4(tokens: List[str], ast_nodes: List):
    exp = Variable('self')
    name = tokens[len(tokens) - 1]

    args = Arguments(exp, name, None)

    ast_nodes.append(args)


def build_Variable(tokens: List[str], ast_nodes: List):
    ast_nodes.append(Variable(tokens[len(tokens) - 1]))


def build_Bool(tokens: List[str], ast_nodes: List):
    ast_nodes.append(Bool(tokens[len(tokens) - 1]))


def build_Number(tokens: List[str], ast_nodes: List):
    ast_nodes.append(Number(tokens[len(tokens) - 1]))


def build_String(tokens: List[str], ast_nodes: List):
    ast_nodes.append(String(tokens[len(tokens) - 2][0]))


def build_None(tokens: List[str], ast_nodes: List):
    ast_nodes.append(_None())


def build_list_1(tokens: List[str], ast_nodes: List):
    expressions = ast_nodes.pop()
    exp_list = _List(get_expressions([], expressions))
    ast_nodes.append(exp_list)


def build_list_2(tokens: List[str], ast_nodes: List):
    exp_list = _List([])
    ast_nodes.append(exp_list)


def build_functions_1(tokens: List[str], ast_nodes: List):
    functions = ast_nodes.pop()
    func = ast_nodes.pop()

    functions = Functions(func, functions)

    ast_nodes.append(functions)


def build_functions_2(tokens: List[str], ast_nodes: List):
    func = ast_nodes.pop()

    functions = Functions(func, None)

    ast_nodes.append(functions)
