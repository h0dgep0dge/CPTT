from lex import Lexer
from parse import Parser,UnexpectedEnd,UnexpectedToken

while True:
    try:
        line = input("> ")
    except EOFError:
        print("See you!")
        exit()
    if line.strip() == '':
        continue
    l = Lexer(line)
    tokens = l.all_tokens()
    p = Parser(tokens)
    try:
        p.expr()
        print(p.pop())
    except UnexpectedToken as e:
        print("Unexpected character",e.args[0].value)
        print(line)
        print(" " * (e.args[0].col-1) + "^")
    except UnexpectedEnd as e:
        print("Unexpected end of line")
