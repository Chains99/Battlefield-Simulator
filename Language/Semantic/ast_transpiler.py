from Language.Parser.ast import Script, Expression, Variable, Number, Bool, _None, _List, FuncDef, If, El_if_se, \
    WhileDef, Decl, Assign, Return, Continue, Break, BinaryExpression, TernaryExpression, \
    BetwBrackExpression, String, Basic
from Language.Semantic.Type_checking.context import Context
from Language.Semantic.Visitor import visitor


class ASTtranspiler:
    def __init__(self):
        self.code = ''
        self.tabs_counter = 0

    def write_code(self, text: str):
        tabs = ''
        for i in range(self.tabs_counter):
            tabs += '\t'
        self.code += tabs + text

    @visitor(Script)
    def transpile(self, node: Script, context: Context):
        for statement in node.statements:
            if isinstance(statement, Expression):
                self.write_code(self.transpile(statement, context) + "\n")
            else:
                self.transpile(statement, context)

        return self.code

    @visitor(Variable)
    def transpile(self, node: Variable, context: Context):
        return node.name

    @visitor(Number)
    def transpile(self, node: Number, context: Context):
        return node.value

    @visitor(Bool)
    def transpile(self, node: Bool, context: Context):
        return node.value

    @visitor(String)
    def transpile(self, node: String, context: Context):
        return r'"' + f"{node.value}" + r'"'

    @visitor(_None)
    def transpile(self, node: _None, context: Context):
        return 'None'

    @visitor(_List)
    def transpile(self, node: _List, context: Context):
        args = ', '.join(self.transpile(element, context) for element in node.inner_list)
        return f'[{args}]'

    @visitor(FuncDef)
    def transpile(self, node: FuncDef, context: Context):
        node.check_semantic(context)
        args = ', '.join(name for name in node.arg_names)
        self.write_code(f'def {node.name}({args}):\n')
        context = context.get_context_child(node.name)
        self.tabs_counter += 1
        for statement in node.body:
            if isinstance(statement, Expression):
                self.write_code(self.transpile(statement, context) + "\n")
            else:
                self.transpile(statement, context)
        self.tabs_counter -= 1

    @visitor(If)
    def transpile(self, node: If, context: Context):
        node.check_semantic(context)
        self.write_code(f'elif {self.transpile(node.condition, context)}:\n')
        self.tabs_counter += 1
        context = context.create_child_context('If')
        for statement in node.body:
            if isinstance(statement, Expression):
                self.write_code(self.transpile(statement, context) + "\n")
            else:
                self.transpile(statement, context)
        self.tabs_counter -= 1

    @visitor(El_if_se)
    def transpile(self, node: El_if_se, context: Context):
        node.check_semantic(context)
        first_if = node.ifs[0]
        self.write_code(f'if {self.transpile(first_if.condition, context)}:\n')
        context = context.create_child_context('If')
        self.tabs_counter += 1
        for statement in first_if.body:
            if isinstance(statement, Expression):
                self.write_code(self.transpile(statement, context) + "\n")
            else:
                self.transpile(statement, context)

        self.tabs_counter -= 1

        total = len(node.ifs)

        if total > 1:
            for i in range(1, total):
                self.transpile(node.ifs[i], context)

        if node.el_if_se_body is not None:
            self.write_code("else:\n")
            self.tabs_counter += 1
            context = context.create_child_context('el_if_se_')
            for statement in node.el_if_se_body:
                if isinstance(statement, Expression):
                    self.write_code(self.transpile(statement, context) + "\n")
                else:
                    self.transpile(statement, context)

            self.tabs_counter -= 1

    @visitor(WhileDef)
    def transpile(self, node: WhileDef, context: Context):

        self.write_code(f'while {self.transpile(node.condition, context)}:\n')

        self.tabs_counter += 1

        for statement in node.body:
            if isinstance(statement, Expression):
                self.write_code(self.transpile(statement, context) + "\n")
            else:
                self.transpile(statement, context)
        self.tabs_counter -= 1

    @visitor(Decl)
    def transpile(self, node: Decl, context: Context):
        node.check_semantic(context)
        self.write_code(f'{node.name} = {self.transpile(node.expression, context)}\n')

    @visitor(Assign)
    def transpile(self, node: Assign, context: Context):
        node.check_semantic(context)
        self.write_code(f'{node.name} = {self.transpile(node.expression, context)}\n')

    @visitor(Return)
    def transpile(self, node: Return, context: Context):
        node.check_semantic(context)
        if node.expression is None:
            self.write_code('return\n')
        else:
            self.write_code(f'return {self.transpile(node.expression, context)}\n')

    @visitor(Continue)
    def transpile(self, node: Continue, context: Context):
        node.check_semantic(context)
        self.write_code('continue\n')

    @visitor(Break)
    def transpile(self, node: Break, context: Context):
        node.check_semantic(context)
        self.write_code('break\n')

    @visitor(BetwBrackExpression)
    def visit(self, node: BetwBrackExpression, context: Context):
        return f'({self.visit(node.expression, context)})'

    @visitor(BinaryExpression)
    def transpile(self, node: BinaryExpression, context: Context):
        left = self.transpile(node.left, context)
        right = self.transpile(node.right, context)

        return f'{left} {node.op if node.op != "^" else "**"} {right}'

    @visitor(TernaryExpression)
    def transpile(self, node: TernaryExpression, context: Context):

        left = self.transpile(node.left, context)
        condition = self.transpile(node.condition)
        right = self.transpile(node.right, context)

        return f'{left} if {condition} else {right}'

    @visitor(Basic)
    def transpile(self, node: Basic, context: Context):
        node.check_semantic(context)
        exp = self.transpile(node.expression, context)
        if node.args is None:
            return f'{exp}.{node.name}'
        elif node.expression.type.split(' ')[0] == 'function':
            args = ', '.join(self.transpile(element, context) for element in node.args)
            return f'{exp}({args})'
        else:
            arg = self.transpile(node.args[0], context)
            return f'{exp}[{arg}]'
