from sly import Parser

import lexerbpb

class parserbpb(Parser):
    # Mendapatkan token dari lexer
    tokens = lexerbpb.lexerbpb.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = { }
        
    # Grammar rules
    @_('')
    def statement(self, p):
        pass

    @_('VAR')
    def expr(self, p):
        return ('var', p.VAR)

    @_('ANGKA')
    def expr(self, p):
        return ('angka', p.ANGKA)

    @_('expr')
    def statement(self, p):
        return(p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('tambah', p.expr0, p.expr1)
    
    @_('expr "-" expr')
    def expr(self, p):
        return ('kurang', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('kali', p.expr0, p.expr1)
    
    @_('expr "/" expr')
    def expr(self, p):
        return ('bagi', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr
    
    @_('UNTUK assign HINGGA expr MAKA statement')
    def statement(self, p):
        return('for_loop', ('for_loop_setup', p.assign, p.expr), p.statement)

    @_('JIKA condition MAKA statement LAIN statement')
    def statement(self, p):
        return('if_stmt', p.condition, ('branch', p.statement0, p.statement1))
    
    @_('FUNC VAR "(" ")" LAKUKAN statement')
    def statement(self, p):
        return('func_def', p.VAR, p.statement)
    
    @_('VAR "(" ")"')
    def statement(self, p):
        return('func_call', p.VAR)
    
    @_('expr SAMADENGAN expr')
    def condition(self, p):
        return('condition_samadengan', p.expr0, p.expr1)

    @_('assign')
    def statement(self, p):
        return p.assign
    
    @_('VAR "=" expr')
    def assign(self, p):
        return('assign', p.VAR, p.expr)
    
    @_('VAR "=" STRING')
    def assign(self, p):
        return('var_assign', p.VAR, p.STRING)
    
    @_('CETAK expr')
    def expr(self, p):
        return('cetak', p.expr)
    
    @_('CETAK STRING')
    def statement(self, p):
        return('cetak', p.STRING)

    @_('expr LDSD expr')
    def expr(self, p):
        return('ldsd', p.expr0, p.expr1)
    
    @_('expr KDSD expr')
    def expr(self, p):
        return('kdsd', p.expr0, p.expr1)
    
    @_('expr LD expr')
    def expr(self, p):
        return('ld', p.expr0, p.expr1)

    @_('expr KD expr')
    def expr(self, p):
        return('kd', p.expr0, p.expr1)

    @_('expr TIDAKSAMA expr')
    def expr(self, p):
        return('tidaksama', p.expr0, p.expr1)
    
    @_('expr MOD expr')
    def expr(self, p):
        return('mod', p.expr0, p.expr1)

if __name__ == '__main__':
    lexer = lexerbpb.lexerbpb()
    parser = parserbpb()
    env = {}

    while True:
        try:
            text = input('bpbparser > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
