from sly import Lexer
from sly import Parser

class lexerDasar(Lexer):
    tokens = {NAMA, ANGKA, STRING, JIKA, MAKA, LAIN, UNTUK, FUNC, HINGGA, SAMADENGAN}
    ignore = '\t '

    literals = {'=', '+', '-', '/', '*', '(', ')', ',', ';', '<', '>', '<=', '>=', '%'}

    #Definisi Token
    JIKA = r'JIKA'
    MAKA = r'MAKA'
    LAIN = r'LAIN'
    UNTUK = r'UNTUK'
    FUNC = r'FUNC'
    HINGGA = r'HINGGA'
    SAMADENGAN = r'=='
    NAMA = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    @_(r'\d+')
    def ANGKA(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

class parserDasar(Parser):
    tokens = lexerDasar.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = { }

    @_('')
    def statement(self, p):
        pass

    @_('UNTUK var_assign HINGGA expr MAKA statement')
    def statement(self, p):
        return('untuk_loop', ('untuk_loop_setup', p.var_assign, p.expr), p.statement)
    
    @_('JIKA condition MAKA statement LAIN statement')
    def statement(self, p):
        return('jika', p.condition, ('branch', p.statement0, p.statement1))
    
    @_('FUNC NAMA "(" ")" statement')
    def statement(self, p):
        return('fungsi', p.name, p.statement)
    
    @_('NAMA "(" ")"')
    def statement(self, p):
        return('panggilFungsi', p.NAMA)
    
    @_('expr SAMADENGAN expr')
    def condition(self, p):
        return('samadengan', p.expr0, p.expr1)
    
    @_('var_assign')
    def statement(self, p):
        return p.var_assign
    
    @_('NAMA "=" expr')
    def var_assign(self, p):
        return('var_assign', p.NAMA, p.expr)

    @_('NAMA "=" STRING')
    def var_assign(self, p):
        return('var_assign', p.NAMA, p.STRING)
    
    @_('expr')
    def statement(self, p):
        return(p.expr)
    
    @_('expr "+" expr')
    def expr(self, p):
        return ('tambah', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('kurang', p.expr0, p.expr1)
    
    @_('expr "/" expr')
    def expr(self, p):
        return ('bagi', p.expr0, p.expr1)
    
    @_('expr "*" expr')
    def expr(self, p):
        return ('kali', p.expr0, p.expr1)
    
    @_('expr "%" expr')
    def expr(self, p):
        return ('mod', p.expr0, p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return('less', p.expr0, p.expr1)

    @_('expr ">" expr')
    def expr(self, p):
        return('greater', p.expr0, p.expr1)
    
    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr
    
    @_('NAMA')
    def expr(self, p):
        return('var', p.NAMA)
    
    @_('ANGKA')
    def expr(self, p):
        return('num', p.ANGKA)

class bpbExecute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)
    
    def walkTree(self, node):
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node
        
        if node is None:
            return None
        
        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])
        
        if node[0] == 'num':
            return node[1]
        
        if node[0] == 'str':
            return node[1]
        
        if node[0] == 'jika':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])
        
        if node[0] == 'samadengan':
            return self.walkTree(node[1]) == self.walkTree(node[2])
        
        if node[0] == 'fungsi':
            self.env[node[1]] = node[2]
        
        if node[0] == 'panggilFungsi':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Fungsi belum didefinisikan '%s'" % node[1])
                return 0
        
        if node[0] == 'tambah':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'kurang':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'kali':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'bagi':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        
        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]
        
        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Variable '" + node[1] + "' belum didefinisikan!")
                return 0
        
        if node[0] == 'untuk_loop':
            if node[1][0] == 'untuk_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limir+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]
        
        if node[0] == 'untuk_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))

if __name__ == '__main__':
    lexer = lexerDasar()
    parser = parserDasar()
    env = {}
    while True:
        try:
            text = input('bpb> ')
        except EOFError:
            print("Program Error")
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            bpbExecute(tree, env)
