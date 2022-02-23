from io import StringIO

from Language.Semantic.Visitor import visitor

class ASTtranspile:
    def __init__(self):
        self.file = StringIO(str())
        self.tabs_counter = 0

    def write(self, string: str):
        tabs = ''
        tabs += ['\t' for i in range(self.tabs_counter)]
        self.file.write(tabs + string)

    @visitor(Script)
    def transpile(self, node: Script, context):

        for class_def in node.classes:
            self.visit(class_def)

        for statement in node.statements:
            if isinstance(statement, Expression, context):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)

        return self.file.getvalue()

    @visitor(Variable)
    def transpile(self, node: Variable, context):
        return node.name

    @visitor(Number)
    def transpile(self, node: Number, context):
        return node.value

    @visitor(Bool)
    def transpile(self, node: Bool, context):
        return node.value

    @visitor(_None)
    def transpile(self, node: _None, context):
        return 'None'

    @visitor(List)
    def transpile(self, node: List, context):
        args = ', '.join(self.transpile(element) for element in node.list)
        return f'[{args}]'

    @visitor(FuncDef)
    def transpile(self, node: FuncDef, context):

        args = ', '.join(name for name in node.arg_names)
        self.write(f'def {node.name}({args}):\n')

        self.tabs_counter += 1
        for statement in node.body:
            if isinstance(statement, Expression):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)
        self.tabs_counter -= 1

    @visitor(If)
    def transpile(self, node: If, context):

        self.write(f'elif {self.visit(node.condition)}:\n')

        self.tabs_counter += 1

        for statement in node.body:
            if isinstance(statement, Expression):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)
        self.tabs_counter -= 1

    @visitor(Else)
    def transpile(self, node: Else, context):

        initial = node.ifs[0]

        self.write(f'if {self.visit(initial.condition)}:\n')

        self.tabs_counter += 1

        for statement in initial.body:
            if isinstance(statement, Expression):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)

        self.tabs_counter -= 1

        total = len(node.ifs)

        if total > 1:
            for i in range(1, total):
                self.visit(node.ifs[i])

        if node.else_body is not None:
            self.write("else:\n")
            self.tabs_counter += 1
            for statement in node.else_body:
                if isinstance(statement, Expression):
                    self.write(self.visit(statement) + "\n")
                else:
                    self.visit(statement)

            self.tabs_counter -= 1

    @visitor(WhileDef)
    def transpile(self, node: WhileDef, context):

        self.write(f'while {self.visit(node.condition)}:\n')

        self.tabs_counter += 1

        for statement in node.body:
            if isinstance(statement, Expression):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)
        self.tabs_counter -= 1

    @visitor(Decl)
    def transpile(self, node: Decl, context):
        self.write(f'{node.name} = {self.visit(node.expression)}\n')

    @visitor(Assign)
    def transpile(self, node: Assign, context):
        self.write(f'{node.name} = {self.visit(node.expression)}\n')

    @visitor(Return)
    def transpile(self, node: Return, context):
        if node.expression is None:
            self.write('return\n')
        else:
            self.write(f'return {self.visit(node.expression)}\n')

    @visitor(Continue)
    def transpile(self, node: Continue, context):
        self.write('continue\n')

    @visitor(Break)
    def transpile(self, node: Break):
        self.write('break\n')

    @visitor(NonArithmeticBinaryExpression)
    def transpile(self, node: BinaryExpression, context):

        left = self.transpile(node.left)
        right = self.transpile(node.right)

        return f'{left} {node.op} {right}'

    @visitor(AritmeticBinaryExpression)
    def visit(self, node: BinaryExpression, context):

        left = self.transpile(node.left)
        right = self.transpile(node.right)

        return f'{left} {node.op if not node.op in self.translation else self.translation[node.op]} {right}'

    @visitor(TernaryExpression)
    def transpile(self, node: TernaryExpression, context):

        left = self.transpile(node.left)
        condition = self.transpile(node.condition)
        right = self.transpile(node.right)

        return f'{left} if {condition} else {right}'

    @visitor(Arguments)
    def transpile(self, node: Arguments, context):

        exp = self.transpile(node.expression)
        if node.args is None:
            return f'{exp}.{node.name}'
        else:
            args = ', '.join(self.transpile(e) for e in node.args)

            return f'{exp}({args})'
