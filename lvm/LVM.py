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
        self.instructions = []
        self.label = {}

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
            self.instructions.append(tuple)
            self.pc = self.pc + 1
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
        # Load constant sp=sp+1; M[sp]=k
        self.check_parameters(1,parameters)
        self.M.push(int(parameters[0]))

    def run_ldv(self, parameters):
        # Load value sp=sp+1; M[sp]=M[D[i]+j]
        self.check_parameters(2, parameters)
        i = int(parameters[0])
        j = int(parameters[1])
        self.M.push(self.M[self.D[i]+j])

    def run_ldr(self, parameters):
        # Load reference sp=sp+1; M[sp]=D[i]+j
        self.check_parameters(2, parameters)
        i = int(parameters[0])
        j = int(parameters[1])
        self.M.push(self.D[i]+j)

    def run_stv(self,parameters):
        # Store value M[D[i]+j]=M[sp]; sp=sp-1
        self.check_parameters(2, parameters)
        i = int(parameters[0])
        j = int(parameters[1])
        self.M.items[self.D[i]+j] = self.M.peek()
        self.M.pop()

    def run_lrv(self,parameters):
        # Load reference value sp=sp+1; M[sp]=M[M[D[i]+j]]
        self.check_parameters(2, parameters)
        i = int(parameters[0])
        j = int(parameters[1])
        self.M.push(self.M[self.M[self.D[i]+j]])

    def run_srv(self,parameters):
        # Store reference value M[M[D[i]+j]]=M[sp]; sp=sp-1
        self.check_parameters(2, parameters)
        i = int(parameters[0])
        j = int(parameters[1])
        self.M.items[self.M[self.D[i]+j]] = self.M.peek()
        self.M.pop()                

    def run_add(self,parameters):
        # Add M[sp-1]=M[sp-1]+M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        k = self.M.pop()
        self.M.changeTop(k + self.M.peek())

    def run_sub(self,parameters):
        # Subtract M[sp-1]=M[sp-1]-M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        k = self.M.pop()
        self.M.changeTop(k - self.M.peek())
        
    def run_mul(self,parameters):
        # Multiply M[sp-1]=M[sp-1]*M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        k = self.M.pop()
        self.M.changeTop(k * self.M.peek())
        
    def run_div(self,parameters):
        # Division M[sp-1]=M[sp-1]/M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        k = self.M.pop()
        self.M.changeTop(k / self.M.peek())

    def run_mod(self,parameters):
        # Modulus M[sp-1]=M[sp-1]%M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        k = self.M.pop()
        self.M.changeTop(k % self.M.peek())

    def run_neg(self,parameters):
        pass
    def run_abs(self,parameters):
        pass
    def run_and(self,parameters):
        pass
    def run_lor(self,parameters):
        pass
    def run_not(self,parameters):
        pass
    def run_les(self,parameters):
        pass
    def run_leq(self,parameters):
        pass       
    def run_grt(self,parameters):
        pass        
    def run_gre(self,parameters):
        pass        
    def run_equ(self,parameters):
        pass        
    def run_neq(self,parameters):
        pass        
    def run_jmp(self,parameters):
        pass        
    def run_jop(self,parameters):
        pass

    def run_alc(self, parameters):
        self.check_parameters(1, parameters)
        i = int(parameters[0])
        for a in range(0,i):
            self.M.push(0)

    def run_dlc(self,parameters):
        pass
    def run_cfu(self,parameters):
        pass
    def run_enf(self,parameters):
        pass
    def run_ret(self,parameters):
        pass
    def run_idx(self,parameters):
        pass
    def run_grc(self,parameters):
        pass
    def run_lmv(self,parameters):
        pass
    def run_smv(self,parameters):
        pass
    def run_smr(self,parameters):
        pass
    def run_sts(self,parameters):
        pass

    def run_rdv(self, parameters):
        # (’rdv’)  # Read single Value sp=sp+1; M[sp]=input()
        self.check_parameters(0, parameters)
        self.M.push(int(input()))

    def run_rds(self,parameters):
        pass
    def run_prv(self,parameters):
        pass
    def run_prt(self,parameters):
        pass
    def run_prc(self,parameters):
        pass
    def run_prs(self,parameters):
        pass
    def run_stp(self,parameters):
        pass

    def run_lbl(self, parameters):
        self.check_parameters(1, parameters)
        self.label[parameters[0]] = self.pc
        
    def run_nop(self,parameters):
        pass
    def run_end(self,parameters):
        pass

