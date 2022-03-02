from Language.Parser.ast import FuncDef
from Language.Semantic.Type_checking.Context import Context


class Type:
    def __init__(self, context: Context, name: str):
        self.name: str = name
        self.attributes = {}
        self.functions = {}
        self.context: Context = context.create_child_context(name)
        context._types[self.name] = self

    def get_type_attribute(self, attribute_key):
        if attribute_key in self.attributes:
            _type = self.attributes[attribute_key]

            if _type == "func":
                _type = self.functions[attribute_key][0]
            return _type

        else:
            raise Exception(
                f"type '{self.name}' has no attribute '{attribute_key}'")

    def get_function(self, method):
        if method in self.functions:
            return self.context.get_func(method)

    def get_attribute(self, attribute_key):
        if attribute_key in self.attributes:
            return self.context.get_type_var(attribute_key)

    def add_attribute(self, name, _type, attribute=None):
        self.attributes[name] = [attribute, _type]
        self.context.add_var(name, _type, attribute)

    def define_function(self, name, return_t, arguments, argument_types):
        self.functions[name] = [return_t, arguments, argument_types]
        return self.context.add_func(FuncDef(name, return_t, arguments,
                                             argument_types, None))  # we define a funct saving it return type,


    def contains_func(self, name):
        return name in self.functions

    def contains_attribute(self, key):
        return key in self.attributes
