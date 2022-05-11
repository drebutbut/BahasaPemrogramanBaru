import lexerbpb
import parserbpb
import interpreterbpb

from sys import *

lexer = lexerbpb.lexerbpb()
parser = parserbpb.parserbpb()
env = {}

file = open(argv[1])
text = file.readlines()

for line in text:
    tree = parser.parse(lexer.tokenize(line))
    interpreterbpb.bpbeksekusi(tree, env)
