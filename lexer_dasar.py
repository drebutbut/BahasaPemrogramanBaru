from sly import Lexer

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

if __name__ == '__main__':
    lexer = lexerDasar()
    env = {}
    while True:
        try:
            text = input('bpb> ')
        except EOFError:
            print("Program Error")
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)
