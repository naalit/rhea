import re
import sys
import ast

def isfloat(value):
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True

def isint(value):
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True

def isname(value):
    return bool(re.match(r'[^#\t\n \$0-9]+', value))

def iskeyword(name):
    return name == 'var' or name == 'val' or name == 'actor' or name == 'class'

class Parser(object):
    def __init__(self):
        self.source = ''
        self.indent = 0
        self.loc = 0
        self.iloc = 0 # Sort of a tentative location. We save it for error reporting, but it's possible we're trying to parse something that's not there, in which case we'll go back to `loc`.

    def isalone(self):
        return self.source[self.loc].isspace()

    def parse(self, source):
        self.source = source
        tree = ast.Program([])
        while True:
            tree.append(self.parse_expr())
            self.skip_indent()
        return tree

    def skip_line(self):
        while self.source[self.loc] != '\n':
            self.loc += 1
        self.loc += 1

    def skip_whitespace(self): # Doesn't skip newlines, those are important
        while self.source[self.loc] == ' ' or self.source[self.loc] == '\t':
            self.loc += 1

    def parse_name(self, name): # We see a name at the start of an expression! Now what?
        char = self.source[self.loc]
        next_name = char
        self.iloc = self.loc
        while True:
            self.iloc += 1
            char = self.source[self.iloc]
            next_name += char
            print next_name + str(self.isalone())
            if self.isalone():
                if isname(next_name) and not iskeyword(next_name): # Message send
                    self.loc = self.iloc
                    args = []
                    self.skip_whitespace()
                    while self.source[self.loc] != '\n' and self.source[self.loc] != ')' and self.source[self.loc] != '#':
                        print next_name
                        args += self.parse_expr()
                        self.skip_whitespace()
                    try:
                        args.remove(None)
                    except:
                        pass
                    return ast.Send(subject=name, callee=next_name, args=args)
                else: # Lookup
                    return ast.Lookup(name)

    def parse_var(self):
        return self.parse_initialize(False)

    def parse_val(self):
        return self.parse_initialize(True)

    def parse_initialize(self, val):
        name = ''
        while True:
            self.loc += 1
            char = self.source[self.loc]
            name += char
            if self.isalone():
                if not isname(name):
                    print("Parse Error: 'var' or 'val' not followed by a name at location " + str(self.loc) + ': \n' + self.source[self.loc:self.loc+20])
                    sys.exit(1)
                self.skip_whitespace()
                if self.source[self.loc] != '=':
                    return ast.Declaration(val, name) # TODO: Type
                self.loc += 1
                self.skip_whitespace()
                expr = self.parse_expr()
                ast.index[name] = expr
                ast.vals[name] = val
                return ast.Initialization(val, name, expr)

    def skip_indent(self): # Returns whether the required indent was reached
        current_indent = 0
        while current_indent < self.indent:
            if self.source[self.loc] == '\t':
                current_indent += 1
                self.loc += 1
                continue
            elif self.source[self.loc] == ' ':
                for i in range(4):
                    if self.source[self.loc == ' ']:
                        self.loc += 1
                    else:
                        print('Parse Error: space indent not a multiple of four at location ' + str(self.loc) + ': \n' + self.source[self.loc:self.loc+20])
                        sys.exit(1)
                current_indent += 1
                continue
            elif self.source[self.loc] == '\n':
                current_indent = 0
                self.loc += 1
                continue
            else:
                return False
        return True

    def parse_actor(self):
        print 'Got here, at least'
        self.skip_whitespace()
        if not self.source[self.loc] == '\n':
            print("Parse Error: 'actor' followed by something else that shouldn't be there at location " + str(self.loc) + ': \n' + self.source[self.loc:self.loc+20])
            sys.exit(1)
        self.loc += 1
        self.indent = 1
        body = []
        while self.skip_indent(): # That elegance is why skip_indent returns like it does
            current_expr = self.parse_expr()
            if isinstance(current_expr, ast.Actor):
                print('Parse Error: actor definition not allowed inside of another actor definition at location ' + str(self.loc) + ': \n' + self.source[self.loc:self.loc+20])
                sys.exit(1)
            body += [current_expr]
        self.indent = 0
        return ast.Actor(body)

    def parse_expr(self, comments_allowed=True):
        self.skip_whitespace()
        char = ''
        print(char)
        name = char
        while True:
            char = self.source[self.loc]
            self.loc += 1
            name += char
            print(name)
            if char == '#':
                if comments_allowed:
                    print('Skipping comment')
                    name = ''
                    self.skip_line()
                else:
                    return None
            if self.isalone():
                name = name.strip()
                print name + ' is alone'
                if isint(name):
                    return ast.IntLiteral(name)
                elif isfloat(name):
                    return ast.FloatLiteral(name)
                elif name == 'actor':
                    return self.parse_actor()
                elif name == 'class':
                    return self.parse_class()
                elif name == 'var':
                    return self.parse_var()
                elif name == 'val':
                    return self.parse_val()
                elif isname(name):
                    return self.parse_name(name)
                else:
                    print('Parse Error: unrecognized token at location ' + str(self.loc) + ': \n' + self.source[self.loc:self.loc+20])
                    sys.exit(1)
