class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def accept(self, kind):
        if self.current()[0] == kind:
            self.pos += 1
            return True
        return False

    def expect(self, kind):
        if not self.accept(kind):
            raise SyntaxError(f'Expected {kind} at pos {self.pos}, got {self.current()}')

    def parse(self):
        statements = []
        while self.current()[0] != 'EOF':
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def statement(self):
        if self.accept('TOH'):
            vtype = None
            if self.accept('TU_INT'):
                vtype = 'int'
            elif self.accept('TU_CHAR'):
                vtype = 'char'
            elif self.accept('TU_STRING'):
                vtype = 'string'
            elif self.accept('TU_BOOL'):
                vtype = 'bool'
            else:
                raise SyntaxError("Expected data type after 'ToH'")
            name = self.current()[1]
            self.expect('IDENT')
            self.expect('ASSIGN')
            expr = self.expr()
            return ('let', vtype, name, expr)
        elif self.accept('CHAP_REE'):
            self.expect('LPAREN')
            expr = self.expr()
            self.expect('RPAREN')
            return ('chap_ree', expr)
        elif self.accept('SUN_OYEE'):
            self.expect('LPAREN')
            name = self.current()[1]
            self.expect('IDENT')
            self.expect('RPAREN')
            return ('sun_oyee', name)
        elif self.accept('AGAR'):
            cond = self.expr()
            self.expect('LBRACE')
            true_branch = []
            while not self.accept('RBRACE'):
                stmt = self.statement()
                if stmt is not None:
                    true_branch.append(stmt)
            false_branch = []
            if self.accept('NAHI_TO'):
                self.expect('LBRACE')
                while not self.accept('RBRACE'):
                    stmt = self.statement()
                    if stmt is not None:
                        false_branch.append(stmt)
            return ('if', cond, true_branch, false_branch)
        elif self.accept('JAB_TAK'):
            cond = self.expr()
            self.expect('LBRACE')
            body = []
            while not self.accept('RBRACE'):
                stmt = self.statement()
                if stmt is not None:
                    body.append(stmt)
            return ('while', cond, body)
        elif self.accept('KARO'):
            self.expect('LBRACE')
            body = []
            while not self.accept('RBRACE'):
                stmt = self.statement()
                if stmt is not None:
                    body.append(stmt)
            self.expect('JAB_TAK')
            self.expect('LPAREN')
            cond = self.expr()
            self.expect('RPAREN')
            return ('do_while', cond, body)
        elif (self.current()[0] == 'IDENT' and
              self.pos + 1 < len(self.tokens) and
              self.tokens[self.pos + 1][0] == 'ASSIGN'):
            name = self.current()[1]
            self.expect('IDENT')
            self.expect('ASSIGN')
            expr = self.expr()
            return ('assign', name, expr)
        else:
            if self.current()[0] in ('RBRACE', 'EOF'):
                return None
            raise SyntaxError(f'Unexpected token: {self.current()}')

    def expr(self):
        return self.compare()

    def compare(self):
        node = self.add()
        while self.current()[0] in ('EQ', 'NE', 'LE', 'LT', 'GE', 'GT'):
            op = self.current()[0]
            self.accept(op)
            right = self.add()
            node = ('cmp', op, node, right)
        return node

    def add(self):
        node = self.mul()
        while self.current()[0] in ('PLUS', 'MINUS'):
            op = self.current()[0]
            self.accept(op)
            right = self.mul()
            node = ('binop', op, node, right)
        return node

    def mul(self):
        node = self.atom()
        while self.current()[0] in ('TIMES', 'DIVIDE', 'MOD'):
            op = self.current()[0]
            self.accept(op)
            right = self.atom()
            node = ('binop', op, node, right)
        return node

    def atom(self):
        tok, value = self.current()
        if tok == 'NUMBER':
            self.accept('NUMBER')
            return ('num', value)
        elif tok == 'TRUE':
            self.accept('TRUE')
            return ('bool', True)
        elif tok == 'FALSE':
            self.accept('FALSE')
            return ('bool', False)
        elif tok == 'CHAR':
            self.accept('CHAR')
            return ('char', value)
        elif tok == 'STRING':
            self.accept('STRING')
            return ('str', value)
        elif tok == 'IDENT':
            self.accept('IDENT')
            return ('var', value)
        elif tok == 'LPAREN':
            self.accept('LPAREN')
            node = self.expr()
            self.expect('RPAREN')
            return node
        else:
            raise SyntaxError(f'Unexpected token: {self.current()}')