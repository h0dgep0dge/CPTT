from enum import Enum
import readline
import string

class TokenType(Enum):
    MINUS = 0
    PLUS = 1
    STAR = 2
    SLASH = 3
    LPAREN = 4
    RPAREN = 5
    NUMBER = 6
    IDENT = 7
    UNKNOWN = 100

class Token:
    def __init__(self,tokenType,value,line,col):
        self.type = tokenType
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token( {self.type.name} , {self.value} )"

class Lexer:
    def __init__(self,source):
        self.source = source
        self.len = len(source)
        self.ptr = 0
        self.line = 1
        self.col = 1
    
    def is_empty(self):
        return self.ptr >= self.len

    def is_not_empty(self):
        return not self.is_empty()

    def peek(self):
        if self.is_empty():
            return None
        return self.source[self.ptr]
    
    def chop(self):
        v = self.peek()
        if v is None:
            return v
        self.ptr += 1
        if v == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return v

    def single_token(self,tokenType):
        line,col = (self.line,self.col)
        return Token(tokenType,self.chop(),line,col)

    def number(self):
        start = self.ptr
        while self.is_not_empty() and self.peek() in string.digits:
            self.chop()
        if self.is_not_empty() and self.peek() == '.':
            self.chop()
            while self.is_not_empty() and self.peek() in string.digits:
                self.chop()
        len = self.ptr - start
        return Token(TokenType.NUMBER,self.source[start:self.ptr],self.line,self.col-len)
        

    def ident(self):
        start = self.ptr
        while self.is_not_empty() and self.peek() in string.ascii_letters:
            self.chop()
        len = self.ptr - start
        return Token(TokenType.IDENT,self.source[start:self.ptr],self.line,self.col-len)

    def next_token(self):
        while self.is_not_empty() and self.peek().isspace():
            self.chop()
        if self.is_empty():
            return None
        match self.peek():
            case '-':
                return self.single_token(TokenType.MINUS)
            case '+':
                return self.single_token(TokenType.PLUS)
            case '*':
                return self.single_token(TokenType.STAR)
            case '/':
                return self.single_token(TokenType.SLASH)
            case '(':
                return self.single_token(TokenType.LPAREN)
            case ')':
                return self.single_token(TokenType.RPAREN)
        if self.peek() in "0123456789":
            return self.number()
        if self.peek() in string.ascii_letters:
            return self.ident()
        return Token(TokenType.UNKNOWN,self.chop(),self.line,self.col)
    
    def all_tokens(self):
        tokens = []
        token = self.next_token()
        while token is not None:
            tokens.append(token)
            token = self.next_token()
        return tokens
