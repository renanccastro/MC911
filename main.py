import sys

from Parser import Parser
from Tokenizer import Tokenizer
from semantic.NodeVisitor import NodeVisitor

if __name__ == "__main__" :
    filename = sys.argv[-1]
    tokenizer = Tokenizer()
    parser = Parser()
    visitor = NodeVisitor()

    if filename != 'main.py' :

        with open(filename, 'r') as content_file:
            content = content_file.read()
            tokenizer.build()
            parser.build()
            result = parser.parser.parse(content, tracking=True)
            print(result)
            ast = visitor.visit(result)
                        
    else :
    
        while True:
            try:
                s = input('calc > ')
            except EOFError:
                break
            if not s: continue
            tokenizer.tokenize(s)
            parser.build()
            result = parser.parser.parse(s)
            print(result)
            ast = visitor.visit(result)

