from Language.Semantic.Type_checking.Context import Context

class Type:
    def __init__(self, context: Context, name: str, parent=None):
        self.name: str = name
        self.attributes = {}
        self.methods = {}
        self.parent: Type = parent
        self.context: Context = context

        if parent is not None:

            # add functions defined in parents context
            for _function in parent.context._func_context:
                self.context._func[_function] = parent.context._func_context[_function]

            parent_context = parent.context

            # add the parent vars
            for var in parent_context._var_context:
                self.context._vars[var] = parent_context._var_context[var]

            # add the parent types
            for t_context in parent_context._type_context:
                self.context._types[t_context] = parent_context._type_context[t_context]

            # add the parent methods
            for p_methods in parent.methods:
                self.methods[p_methods] = parent.methods[p_methods]

            # add the parent attributes
            for p_atributes in parent.attributes:
                self.attributes[p_atributes] = parent.attributes[p_atributes]

    def get_type_attribute(self, attribute_key):
        if attribute_key in self.attributes:
            _type = self.attributes[attribute_key]

            if _type == "func":
                _type = self.methods[attribute_key][0]
            return _type

        else:
            raise Exception(
                f"type '{self.name}' has no attribute '{attribute_key}'")

    def get_methods(self, method):
        if method in self.methods:
            return self.methods[method]

    def get_attributes(self, attribute_key):
        if attribute_key in self.attributes:
            return self.attributes[attribute_key]

    def add_attribute(self, name, _type, attribute=None):
        self.attributes[name] = [attribute, _type]
        self.context.add_var(name, _type, attribute)

    def define_method(self, name, return_t, arguments, argument_types):
        self.methods[name] = [return_t, arguments, argument_types]
        # self.attributes[name] = [name, "func"]
        return self.context.add_func(name, return_t, arguments,
                                     argument_types)  # we define a funct saving it return type,
        # it's arguments and argument types

    def is_method(self, name):
        return name in self.methods

    def is_attribute(self, key):
        return key in self.attributes
