from lex import TokenType

p = lambda *pargs, **nargs : print(*pargs,**nargs,end='')

class UnexpectedToken(Exception):
    pass

class UnexpectedEnd(Exception):
    pass

class Parser:
    SYMBOLS = {
        "pi":3.141592653589793,
        "e":2.718281828459045
    }

    def __init__(self,tokens):
        self.tokens = tokens
        self.ptr = 0
        self.len = len(tokens)
        self.stack = []
    
    def push(self,value):
        self.stack.append(value)
    
    def pop(self):
        v = self.stack[-1]
        del self.stack[-1]
        return v
    
    def add(self):
        r = self.pop()
        self.push(self.pop()+r)
        
    def sub(self):
        r = self.pop()
        self.push(self.pop()-r)
    
    def mult(self):
        r = self.pop()
        self.push(self.pop()*r)
        
    def div(self):
        r = self.pop()
        self.push(self.pop()/r)
    
    def is_empty(self):
        return self.ptr >= self.len

    def is_not_empty(self):
        return not self.is_empty()
    
    def peek(self):
        if self.is_empty():
            return None
        return self.tokens[self.ptr]
    
    def chop(self):
        v = self.peek()
        if v is not None:
            self.ptr += 1
        return v
    
    def expect(self,tokenType):
        if self.is_empty():
            raise UnexpectedEnd()
        if self.peek().type is tokenType:
            return self.chop()
        raise UnexpectedToken(self.chop())

    def check(self,tokenType):
        if self.is_empty():
            return False
        return self.peek().type is tokenType
    
    def expr(self):
        '''
        expr -> term rexpr
        '''
        self.term()
        self.rexpr()
    
    def rexpr(self):
        '''
        rexpr -> + term {add} rexpr
               | - term {sub} rexpr
               | ϵ
        '''
        if self.check(TokenType.PLUS):
            self.expect(TokenType.PLUS)
            self.term()
            self.add()
            self.rexpr()
            return
        if self.check(TokenType.MINUS):
            self.expect(TokenType.MINUS)
            self.term()
            self.sub()
            self.rexpr()
            return
        "episilon"
    
    def term(self):
        '''
        term -> factor rterm
        '''
        self.factor()
        self.rterm()
    
    def rterm(self):
        '''
        rterm -> + factor {mult} rterm
               | - factor {div} rterm
               | ϵ
        '''
        if self.check(TokenType.STAR):
            self.expect(TokenType.STAR)
            self.factor()
            self.mult()
            self.rterm()
            return
        if self.check(TokenType.SLASH):
            self.expect(TokenType.SLASH)
            self.factor()
            self.div()
            self.rterm()
            return
        "episilon"
    
    def factor(self):
        '''
        factor -> number {push number}
                | - {push 0} factor {sub}
                | ident {push SYMBOLS[ident]}
                | ( expr )
        '''
        if self.check(TokenType.MINUS):
            self.expect(TokenType.MINUS)
            self.push(0)
            self.factor()
            self.sub()
            return
        if self.check(TokenType.NUMBER):
            self.push(float(self.expect(TokenType.NUMBER).value))
            return
        if self.check(TokenType.IDENT):
            id = self.expect(TokenType.IDENT)
            if id.value not in self.SYMBOLS:
                raise UnexpectedToken(id)
            self.push(self.SYMBOLS[id.value])
            return
        if self.check(TokenType.LPAREN):
            self.expect(TokenType.LPAREN)
            self.expr()
            self.expect(TokenType.RPAREN)
            return
        raise UnexpectedToken(self.chop())
    

