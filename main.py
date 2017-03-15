from Tokenizer import Tokenizer
import sys



if __name__ == "__main__":
    filename = sys.argv[-1]
    tokenizer = Tokenizer()

    with open(filename, 'r') as content_file:
        content = content_file.read()
        tokenizer.tokenize(content)