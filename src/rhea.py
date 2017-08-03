from parsimonious.grammar import Grammar, NodeVisitor


class Rhea(NodeVisitor):

    def parse(self, source):
        grammar = '\n'.join(v.__doc__ for k, v in vars(self.__class__).items()
                            if not k.startswith('__') and hasattr(v, '__doc__')
                            and getattr(v, '__doc__'))
        return Grammar(grammar)['program'].parse(source)

    def visit_program(self, node, children):
        'program = (_ (comment / expression / newline))*'
        return children

    def visit_function(self, node, children):
        'function = "fun" _ ("(" _ param* ")")? _ (expression / ((_ (comment / expression / newline))* _ "end"))'
        return f"Function {children[1]} with parameters {children[6][2]}"

    def visit_params(self, node, children):
        'param = name _ ":" _ name _'

    def visit_newline(self, node, children):
        'newline = ~"\\n"'

    def visit_comment(self, node, children):
        'comment = ~"#.*\\n"'

    def visit_expression(self, node, children): # Expressions are statements that return a value
        'expression = _ (assignment / function / operator / call / literal) _'
        return children[1]

    def visit_operator(self, node, children):
        'operator = (call / literal) (add / sub / mul / div) expression'
        return f"Operator {children[1]} with lhs {children[0]} and rhs {children[2]}"

    def visit_add(self, node, children):
        'add = "+" _'
        return 'Add'

    def visit_sub(self, node, children):
        'sub = "-" _'
        return 'Sub'

    def visit_mul(self, node, children):
        'mul = "*" _'
        return 'Mul'

    def visit_div(self, node, children):
        'div = "/" _'
        return 'Div'

    def visit_assignment(self, node, children):
        'assignment = define? name "=" _ expression'
        return f"Assigned {children[1]} to {children[4]}, with def '{children[0]}'"

    def visit_literal(self, node, children):
        'literal = int / float'
        return children[0]

    def visit_call(self, node, children): # Function calls AND variable reads
        'call = (name name expression*) / (name expression*)' # subject? callee objects*
        return f"Call: {node.text.strip()}"

    def visit_name(self, node, children):
        'name = ~"[a-zA-Z_][a-zA-Z_0-9]+" _'
        return node.text.strip()

    def visit_int(self, node, children):
        'int = ~"[0-9]+" _'
        return int(node.text.strip())

    def visit_float(self, node, children):
        'float = ~"[0-9]\.[0-9]+" _'
        return float(node.text.strip())

    def visit_define(self, node, children):
        'define = "def" _'
        return 'def'

    def visit__(self, node, children):
        '_ = ~"[\\t ]*"'

    def visit_(self, node, children):
        return children

input = """def joe = 3 * 24 # Variable
#24 + (23 - 245)*23
1
2
    def stuff = 3
    fun(x: Int) x + 3 # Function
# Let's call `stuff`!
stuff 3
# Comment
23/4 - joe
    joe = 3
"""

def clean(lis):
    return [x for x in lis if x]

rhea = Rhea()
e = rhea.parse(input)
print(e)
lis = rhea.visit(e)
lis = [clean([clean(y) for y in clean(x)]) for x in clean(lis)]
lis = [clean([clean(y) for y in clean(x)]) for x in clean(lis)]
lis = [item[0] for sublist in lis for q in sublist for item in q]
print(lis)
