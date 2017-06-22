import sys

from Parser import Parser
from Tokenizer import Tokenizer
from lvm.LVM import LVM
from semantic.CodeGenerator import CodeGenerator
from semantic.NodeVisitor import NodeVisitor
from pprint import pprint

if __name__ == "__main__" :
    filename = sys.argv[-1]
    tokenizer = Tokenizer()
    parser = Parser()
    visitor = NodeVisitor()
    generator = CodeGenerator()
    lvm = LVM(False)
    if filename != 'main.py' :

        with open(filename, 'r') as content_file:
            content = content_file.read()
            tokenizer.build()
            parser.build()
            print()
            print(":::::::::: :::::::::::::::: ::::::::::")
            print(":::::::::: Parser and Lexer ::::::::::")
            print(":::::::::: :::::::::::::::: ::::::::::")
            print()
            result = parser.parser.parse(content, tracking=True)
            print()
            print(":::::::::: ::::::::::::::::::::::::::: ::::::::::")
            print(":::::::::: Visiting and Decorating AST ::::::::::")
            print(":::::::::: ::::::::::::::::::::::::::: ::::::::::")
            print()
            visitor.visit(result)
            visitor.visit_print(result)
            print()
            print(":::::::::: ::::::::::: ::::::::::")
            print(":::::::::: MAKING CODE ::::::::::")
            print(":::::::::: ::::::::::: ::::::::::")
            print()

            generator.generate(result)
            pprint(generator.environment.stack)
            pprint(generator.environment.H)
            pprint(generator.environment.code)

            print()
            print(":::::::::: ::::::::::: ::::::::::")
            print(":::::::::: RUN    CODE ::::::::::")
            print(":::::::::: ::::::::::: ::::::::::")
            print()

            lvm.run_program(generator.environment.code,
                            generator.environment.H)

    else :
    
        while True:
            try:
                s = input('calc > ')
            except EOFError:
                break
            if not s: continue
            tokenizer.tokenize(s)
            parser.build()
            print("Parser and Lexer")
            result = parser.parser.parse(s)
            print(result)
            ast = visitor.visit(result)
            print("Visiting and Decorating AST")
            visitor.visit_print(result)

