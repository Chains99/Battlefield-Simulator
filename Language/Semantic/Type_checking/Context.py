class Context:
    """
    Context class is used to define an execution context where there are defined the vars, methods and types
    whenever a var is assigned, a type is created or a function is defined
    """

    def __init__(self, name: str, parent=None, func=None, _while: bool = None):
        self.name = name
        self.parent = parent
        self.childrens = {}
        self._vars = {}
        self._func = {}
        self._types = {}
        self.ifs = 0
        self.func = func
        self._while = None
        self.logical_ops = {'<=', '==', '>=', '!=', '>', '<'}

    def get_func(self, func):
        if self.parent is None:
            return self._func.get(func)
        else:
            if func in self._func:
                return self._func[func]
            # check for the function to be defined in a parent context
            return self.parent.get_func(func)

    def check_var_in_context(self, var, check_parent=True):
        if self.parent is None:
            return var in self._vars
        else:
            if var in self._vars:
                return True
            if (check_parent):
                return self.parent.check_var_in_context(var)
            else:
                return False

    def check_var_type(self, var, _type):
        if self.check_var_in_context(var):
            _type = self.get_type_var(var)
            if self.get_type_var(var) == _type:
                return True
            else:
                return False
        else:
            raise Exception(f"{var} is not defined")

    def get_type(self, name: str):
        if self.parent is None:
            _type = self._types.get(name)
            if _type is None:
                raise Exception(f'Type {name} is not defined')
            return _type
        else:
            return self.parent.get_type(name)

    def check_func_args(self, func, args):
        if self.parent is None:
            if func is not None:
                if len(args) == len(func.arg_names):
                    for i in range(len(args)):
                        if args[i] != func.arg_types[i] and (func.arg_types[i] != 'List' == args[i].split(' ')[0]) and \
                                func.arg_types[i] != "Type":
                            return False

                    return True

            return False

        else:
            _func = self._func.get(func.name)
            if _func is not None:
                if len(args) == len(self._func[func][1]):
                    for i in range(len(args)):
                        if not args[i] != _func[1][i]:
                            return False
                    return True
            return self.parent.check_func_args(func, args)

    def get_type_var(self, var):
        if var in self._vars:
            return self._vars[var][1] if self._vars[var][0] != 'function' else 'function'
        elif self.parent is not None:
            return self.parent.get_type_var(var)
        else:
            raise Exception(f"{var} has not been defined")

    def add_var(self, var, _type, value="", aux=True):
        if not self.check_var_in_context(var, aux):
            if self.is_type_defined(_type):
                self._vars[var] = ["var", _type, value]
            else:
                raise Exception(f"Type {_type} is not defined")
        else:
            raise Exception(f"Var {var} is already defined")

    def add_func(self, func):
        if self.is_type_defined(func.return_type):
            if func.name in self._vars:
                raise Exception(f"{func.name} is already defined")

            self._vars[func.name] = ["function", func.return_type, func]
            self._func[f'{func.name}'] = func
            _context = self.create_child_context(func.name)
            if (func.name == 'run'):
                print()
            for i in range(len(func.arg_names)):
                if self.is_type_defined(func.arg_types[i].split(' ')[0]):
                    name = func.arg_names[i]
                    _type = func.arg_types[i]
                    _context.add_var(name, _type, aux=False)
                else:
                    raise Exception(f"Type {func.arg_types[i]} is not defined")
        else:
            raise Exception(f"Type {func.return_type} is not defined")
        self._func[f'{func.name}'] = func
        return _context

    def in_while_context(self):
        if self._while is not None:
            return self._while
        if self.name == 'while':
            self._while = True
        elif self.parent is not None:
            self._while = self.parent.in_while_context()
        else:
            self._while = False
        return self._while

    def create_child_context(self, name):
        func = None
        _type = ''
        if (self.check_var_in_context(name)):
            _type = self.get_type_var(name)
        if _type == 'function':
            func = self._func.get(name)
        child = Context(name, self, func if func is not None else self.func)
        self.childrens[name] = child
        return child

    def get_return_type(self, func_name):
        if self.parent is None:
            _func = self.get_func(func_name)
            if _func is not None:
                return _func[0]

            else:
                raise Exception(f"Function '{func_name}' is not defined")

        else:
            if func_name in self._types:
                return self._func[func_name][0]

            else:
                return self.parent.get_return_type(func_name)

    # check if the type it's defined
    def is_type_defined(self, name):
        if self.parent is None:
            return name.split(' ')[0] in self._types

        else:
            if name.split(' ')[0] in self._types:
                return True

            else:
                return self.parent.is_type_defined(name)

    # check if the context parent name's coincide with the given one
    def is_context_parent(self, name):
        if self.parent is None:
            return self.name == name

        else:
            if self.parent.name == name:
                return True

            return self.parent.is_context_parent

    # search for the parent context recursively if it isn't the context parent or it's the current context
    def get_context_parent(self, name):
        if self.parent is None and self.name == name:
            return self

        else:
            if self.parent.name == name:
                return self.parent

            return self.parent.get_context_parent(name)

    def get_context_child(self, name):
        child = self.childrens.get(name)
        return child if child is not None else self
