import sys

from Parser import Parser
from Tokenizer import Tokenizer
from lvm.LVM import LVM
from semantic.CodeGenerator import CodeGenerator
from semantic.NodeVisitor import NodeVisitor
from pprint import pprint
import argparse


parser = argparse.ArgumentParser(description='Compiler and LVM for LYA, developed by Renan and Wendrey.')
parser.add_argument('filename', metavar='filename', type=str, nargs=1,
                    help='file to be compiled and executed')
parser.add_argument('--debuglvm', dest='debuglvm', action='store_const',
                    const=True, default=False,
                    help='run lvm in debug mode (default: no)')
parser.add_argument('--print-tree', dest='printtree', action='store_const',
                    const=True, default=False,
                    help='print decorated tree (default: no)')
parser.add_argument('--hide-code', dest='hidecode', action='store_const',
                    const=True, default=False,
                    help='dont show generated code, only run program (default: no)')


args = parser.parse_args()


if __name__ == "__main__" :
    filename = args.filename[0]
    tokenizer = Tokenizer()
    parser = Parser()
    visitor = NodeVisitor()
    generator = CodeGenerator()
    lvm = LVM(args.debuglvm)
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
            if args.printtree:
                visitor.visit_print(result)
            print()
            print(":::::::::: ::::::::::: ::::::::::")
            print(":::::::::: MAKING CODE ::::::::::")
            print(":::::::::: ::::::::::: ::::::::::")
            print()

            try:
                generator.generate(result)
                if not args.hidecode:
                    pprint(generator.environment.stack)
                    pprint(generator.environment.H)
                    pprint(generator.environment.code)
            except Exception:
                print("Sorry, you program has unrecoverable errors. Fix them and try again.")
                sys.exit(1)

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

