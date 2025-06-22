class Interpreter:
    def __init__(self):
        self.env = {}

    def eval(self, node):
        if node is None:
            return
        nodetype = node[0]
        if nodetype == 'let':
            _, vtype, name, expr = node
            if name in self.env:
                raise NameError(f'Variable {name} already declared')
            value = self.eval(expr)
            # type checking
            if vtype == 'int':
                if not isinstance(value, int):
                    raise TypeError(f"{name} must be int")
            elif vtype == 'string':
                if not isinstance(value, str):
                    raise TypeError(f"{name} must be string")
            elif vtype == 'char':
                if not (isinstance(value, str) and len(value) == 1):
                    raise TypeError(f"{name} must be a char")
            elif vtype == 'bool':
                if not isinstance(value, bool):
                    raise TypeError(f"{name} must be bool")
            self.env[name] = {'type': vtype, 'value': value}
        elif nodetype == 'assign':
            _, name, expr = node
            if name not in self.env:
                raise NameError(f'Variable {name} not declared')
            value = self.eval(expr)
            vtype = self.env[name]['type']
            if vtype == 'int' and not isinstance(value, int):
                raise TypeError(f"{name} must be int")
            elif vtype == 'string' and not isinstance(value, str):
                raise TypeError(f"{name} must be string")
            elif vtype == 'char' and not (isinstance(value, str) and len(value) == 1):
                raise TypeError(f"{name} must be a char")
            elif vtype == 'bool' and not isinstance(value, bool):
                raise TypeError(f"{name} must be bool")
            self.env[name]['value'] = value
        elif nodetype == 'var':
            name = node[1]
            if name not in self.env:
                raise NameError(f'Variable {name} not defined')
            return self.env[name]['value']
        elif nodetype == 'num':
            return node[1]
        elif nodetype == 'str':
            return node[1]
        elif nodetype == 'char':
            return node[1]
        elif nodetype == 'bool':
            return node[1]
        elif nodetype == 'chap_ree':
            value = self.eval(node[1])
            print(str(value))
        elif nodetype == 'sun_oyee':
            name = node[1]
            vtype = self.env[name]['type'] if name in self.env else None
            user_input = input()
            if vtype == 'int':
                try:
                    self.env[name]['value'] = int(user_input)
                except:
                    raise ValueError(f"Input is not valid int for {name}")
            elif vtype == 'char':
                if len(user_input) == 1:
                    self.env[name]['value'] = user_input
                else:
                    raise ValueError(f"Input is not valid char for {name}")
            elif vtype == 'bool':
                self.env[name]['value'] = user_input.lower() == "true"
            elif vtype == 'string':
                self.env[name]['value'] = user_input
            else:
                self.env[name] = {'type': 'string', 'value': user_input}
        elif nodetype == 'binop':
            _, op, left, right = node
            lval = self.eval(left)
            rval = self.eval(right)
            if op == 'PLUS':
                if isinstance(lval, str) or isinstance(rval, str):
                    return str(lval) + str(rval)
                return lval + rval
            elif op == 'MINUS':
                return lval - rval
            elif op == 'TIMES':
                return lval * rval
            elif op == 'DIVIDE':
                if (isinstance(lval, int) or isinstance(lval, float)) and rval == 0:
                    raise ZeroDivisionError("Division by zero")
                return lval // rval if isinstance(lval, int) and isinstance(rval, int) else lval / rval
            elif op == 'MOD':
                if (isinstance(lval, int) or isinstance(lval, float)) and rval == 0:
                    raise ZeroDivisionError("Modulo by zero")
                return lval % rval
        elif nodetype == 'cmp':
            _, op, left, right = node
            lval = self.eval(left)
            rval = self.eval(right)
            if op == 'EQ':
                return lval == rval
            elif op == 'NE':
                return lval != rval
            elif op == 'LT':
                return lval < rval
            elif op == 'LE':
                return lval <= rval
            elif op == 'GT':
                return lval > rval
            elif op == 'GE':
                return lval >= rval
        elif nodetype == 'if':
            _, cond, true_branch, false_branch = node
            if self.eval(cond):
                for stmt in true_branch:
                    self.eval(stmt)
            else:
                for stmt in false_branch:
                    self.eval(stmt)
        elif nodetype == 'while':
            _, cond, body = node
            while self.eval(cond):
                for stmt in body:
                    self.eval(stmt)
        elif nodetype == 'do_while':
            _, cond, body = node
            while True:
                for stmt in body:
                    self.eval(stmt)
                if not self.eval(cond):
                    break

    def run(self, statements):
        for stmt in statements:
            if stmt:
                self.eval(stmt)