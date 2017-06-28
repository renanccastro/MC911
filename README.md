# MC911


Compilador para LYA em MC911.

### Autores

Renan Camargo de Castro    RA 147775

Wendrey Lustosa Cardoso    RA 148234

### Modo de uso

~~~
usage: main.py [-h] [--debuglvm] [--print-tree] [--hide-code] filename

Compiler and LVM for LYA, developed by Renan and Wendrey.

positional arguments:
  filename      file to be compiled and executed

optional arguments:
  -h, --help    show this help message and exit
  --debuglvm    run lvm in debug mode (default: no)
  --print-tree  print decorated tree (default: no)
  --hide-code   dont show generated code, only run program (default: no)
~~~

Comando: __python3 main.py <input_file>__ .

Alguns exemplos estão localizados no diretório __lya_examples__.

A AST é impressa caso se use --print-tree, mas aconselha-se usar o PYCHARM para analisar a AST.

Para maiores informações
 
__python3 main.py -h__ .
