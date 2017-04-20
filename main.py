from Tokenizer import Tokenizer
from Parser import Parser
import sys



if __name__ == "__main__":
    filename = sys.argv[-1]
    tokenizer = Tokenizer()
    parser = Parser()

    if filename != 'main.py':

        with open(filename, 'r') as content_file:
            content = content_file.read()
            tokenizer.tokenize(content)
            parser.build()
            result = parser.parser.parse(content)
            print(result)        


    # TODO: TROCAR PARA LER DE UM ARQUIVO, POR ENQUANTO TA PEGANDO DO CONSOLE PRA TESTES
    # not working... =(
    # with open(filename, 'r') as content_file:
    #     content = content_file.read()
    #     tokenizer.tokenize(content)
    #     parser.parse(content, lexer=tokenizer)
            
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
