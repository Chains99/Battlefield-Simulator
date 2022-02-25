def _qualname(obj):
    # return the path to the given obj method
    return obj.__module__ + '.' + obj.__qualname__


def _class(obj):
    name = _qualname(obj)
    return name[:name.rfind('.')]


_methods = {}


def _visitor_impl(self, arg, *args):
    method = _methods[(_qualname(type(self)), type(arg))]
    return method(self, arg, args[0])


def visitor(arg_type):
    def decorator(fun):
        declaring_class = _class(fun)
        _methods[(declaring_class, arg_type)] = fun

        # Replace all decorated methods with _visitor_impl
        return _visitor_impl

    return decorator
