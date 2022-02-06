import enum


class CompilingError:
    def __init__(self, location, error_code, argument):
        self.location = location
        self.error_code = error_code
        self.argument = argument


class ErrorCode(enum.Enum):
    none = 1
    expected = 2
    invalid = 3
    unknown = 4


class Code_Location:
    def __init__(self, filename, line, column):
        self.filename = filename
        self.line = line
        self.column = column


class Output_info():
    def __init__(self):
        self.errors = []

    def add_error(self, error):
        self.errors.append(error)

    def add_unexpected_token_error(self, location, token):
        self.errors.append(CompilingError(location, token))

