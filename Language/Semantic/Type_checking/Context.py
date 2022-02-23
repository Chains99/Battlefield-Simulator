from Language.Semantic.Type_checking.Type import Type


class Context:
    """
    Context class is used to define an execution context where there are defined the vars, methods and types
    whenever a var is assigned, a type is created or a function is defined
    """

    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.childrens = {}
        self._vars = {}
        self._func = {}
        self._types = {}
        self.While_count = 0
        self.If_count = 0
        self.Else_count = 0

    def get_func(self, func):
        if self.parent is None:
            return self._func.get(func)
        else:
            if func in self._func:
                return self._func[func]
            # check for the function to be defined in a parent context
            return self.parent.get_func(func)

    def check_var_in_context(self, var):
        if self.parent is None:
            return var in self._vars
        else:
            if var in self._vars:
                return True

            return self.parent.check_var(var)

    def check_var_type(self, var, _type):
        if self.check_var_in_context(var):
            _type = self.get_type_var(var)

            # to check list type we check for the type of the first element
            if isinstance(type, list):
                _type = type[1]

            if self.get_type_var(var) == _type:
                return True
            else:
                return False

        else:
            raise Exception(f"{var} is not defined")

    def check_func_args(self, func, args):
        if self.parent is None:
            _func = self._func.get(func)
            if _func is not None:
                if len(args) == len(self._func[func][1]):
                    for i in range(len(args)):
                        if args[i] != _func[1][i] and _func[1][i] != "Type":
                            return False

                    return True

            return False

        else:
            _func = self._func.get(func)
            if _func is not None:
                if len(args) == len(self._func[func][1]):
                    for i in range(len(args)):
                        if not args[i] != _func[1][i]:
                            return False

                    return True

            return self.parent.check_func_args(func, args)

    def get_type_var(self, var):
        if self.parent is None:
            if var in self._vars:
                return [self._vars[var][0], self._vars[var][1]]
            else:
                raise Exception(f"{var} has not been defined")

        else:
            if var in self._vars:
                return [self._vars[var][0], self._vars[var][1]]
            else:
                return self.parent.get_type_var(var)

    def add_var(self, var, _type, value=""):
        type = _type
        if isinstance(_type, list):
            type = _type[1]

        if not self.check_var_type(var, type) and self.is_type_defined(type):
            self._vars[var] = ["var", type, value]

        elif var in self._vars and self._vars[var][1] == type:
            self._vars[var][2] = value

        else:
            raise Exception(f"Type {type} is not defined")

    def add_func(self, func, return_type, args, _type_args):
        if self.is_type_defined(return_type):

            if func in self._vars:
                raise Exception(f"{func} is already defined")

            self._vars[func] = ["function", None, None]
            _context = self.create_child_context(func)
            _func = [return_type, [0] * len(args), [0] * len(args)]  # func: [return type, args_type, args_name]

            for i in range(len(args)):
                if self.is_type_defined(_type_args[i]):
                    _func[2][i] = args[i]
                    _func[1][i] = _type_args[i]


                else:
                    raise Exception("Type Error")


        else:
            raise Exception("Type Error")

        self._func[func] = _func
        for i in range(len(args)):
            _context.add_var(args[i], _type_args[i])

        return _context

    def create_child_context(self, name):
        child = Context(name, self)
        self.childrens[name] = child
        return child

    def define_type(self, name, args=[], type_args=[], parent=None):
        _parent = None
        if parent is not None:
            _parent = self.get_type_object(parent)

        child = self.create_child_context(name)
        t = Type(child, name, self)
        self._types[name] = t
        self.add_func(name, name, args, type_args)
        return [t, child]

    def get_return_type(self, func):

        if self.parent is None:
            _func = self.get_func(func)
            if _func is not None:
                return _func[0]

            else:
                raise Exception(f"Function '{func}' is not defined")

        else:
            if func in self._types:
                return self._func[func][0]

            else:
                return self.parent.get_return_type(func)

    def get_type_object(self, name_type):
        name = name_type
        if isinstance(name, list):
            name = name_type[1]
        if self.parent is None:
            if name in self._types:
                return self._types[name]

            else:
                raise Exception(f"Type '{name}' is not defined")

        else:
            if name in self._types:
                return self._types[name]

            else:
                return self.parent.get_type_object(name)

    # check if the type it's defined
    def is_type_defined(self, name):
        if self.parent is None:
            return name in self._types

        else:
            if name in self._types:
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
