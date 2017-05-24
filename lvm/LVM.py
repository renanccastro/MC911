from lvm.Stack import Stack


class IncompleteInstruction(Exception):
    pass



class LVM():
    def __init__(self, H):
        super().__init__()
        self.pc = 0
        self.P = []
        self.M = Stack()
        self.D = []
        self.H = H

    def print_stats(self):
        print()
        print(":::::::::: :::::::::::::::: ::::::::::")
        print("REGISTERS: SP: {}    PC: {}".format(self.M.pointer(),self.pc))
        print("STACK:     P:  {}    M:  {}    D:  {}     H: {}".format(self.P,self.M,self.D,self.H))
        print(":::::::::: :::::::::::::::: ::::::::::")
        print()

    def check_parameters(self, number, array):
        if len(array) != number:
            raise IncompleteInstruction("ERROR: expected {} parameters, got {}".format(number, len(array)))

    def run_instruction(self, tuple):
        try:
            method = getattr(self, "run_{}".format(tuple[0]))
            method(tuple[1:])
            self.print_stats()
        except IncompleteInstruction as e:
            print(e.args[0])
        except AttributeError:
            print("Not supported instruction: {}".format(tuple[0]))
        except Exception as e:
            print(e)

    def run_stp(self, parameters):
        self.sp = -1
        self.M = Stack()
        self.D = [0]
        print(parameters)


    def run_ldc(self, parameters):
        # Load constant sp = sp + 1; M[sp] = k
        self.check_parameters(1,parameters)
        self.M.push(int(parameters[0]))

    def run_ldv(self, parameters):
        # Load value sp=sp+1;  M[sp]=M[D[i]+j]
        self.check_parameters(2, parameters)
        i = int(parameters[0])
        j = int(parameters[1])
        self.M.push(self.M[self.D[i]+j])

    def run_ldr(self, parameters):
        # Load reference sp = sp + 1; M[sp] = D[i] + j
        self.check_parameters(2, parameters)
        i = int(parameters[0])
        j = int(parameters[1])
        self.M.push(self.D[i] + j)

    def run_stv(self,parameters):
        # Store value M[D[i] + j] = M[sp]; sp = sp - 1
        self.check_parameters(2, parameters)
        i = int(parameters[0])
        j = int(parameters[1])
        self.M[self.D[i] + j] = self.M.peek()
        self.M.pop()
        
    def run_add(self,parameters):
        self.check_parameters(0, parameters)
        j = self.M.pop()
        self.M.changeTop(j + self.M.peek())
