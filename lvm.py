import sys

from lvm.LVM import LVM
import json
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
            if filename == 'lvm.py':
                s = input('calc > ')
                lvm.run_instruction([x.strip() for x in s.split(',')])
            else:
                with open(filename) as dataFile:
                    data = json.load(dataFile)
                    lvm.run_program(data["instructions"], data["heap"])

        except EOFError:
            break







