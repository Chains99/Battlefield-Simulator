from Language.lexer.Lexer import lexer

code = "a = 5+4;"
lex = lexer()
b = lex.get_token_manager("H", code)
print("a")
