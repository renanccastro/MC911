import sys

from lvm.LVM import LVM

if __name__ == "__main__":
    filename = sys.argv[-1]

    print()
    print(":::::::::: :::::::::::::::: ::::::::::")
    print("::::::::::   LVM - RUNNING  ::::::::::")
    print(":::::::::: :::::::::::::::: ::::::::::")
    print()

    lvm = LVM([])
    while True:
        try:
            s = input('calc > ')
            lvm.run_instruction([x.strip() for x in s.split(',')])
        except EOFError:
            break







