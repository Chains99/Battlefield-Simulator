def _qualname(obj):
    # return the path to the given obj method
    return obj.__module__ + '.' + obj.__qualname__


def dec_class(obj):
    name = _qualname(obj)
    return name[:name.rfind('.')]


_functions = {}


def _visitor_dec(self, arg, *args):
    method = _functions[(_qualname(type(self)), type(arg))]
    return method(self, arg, args[0])


def visitor(arg_type):
    def decorator(fun):
        declaring_class = dec_class(fun)
        _functions[(declaring_class, arg_type)] = fun

        # Replace all decorated methods with _visitor_dec
        return _visitor_dec

    return decorator
