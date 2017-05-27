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
        m = self.M.pop()
        self.M.changeTop(self.M.peek() + m)

    def run_sub(self,parameters):
        # Subtract M[sp-1]=M[sp-1]-M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() - m)
        
    def run_mul(self,parameters):
        # Multiply M[sp-1]=M[sp-1]*M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() * m)
        
    def run_div(self,parameters):
        # Division M[sp-1]=M[sp-1]/M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() / m)

    def run_mod(self,parameters):
        # Modulus M[sp-1]=M[sp-1]%M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() % k)

    def run_neg(self,parameters):
        # Negate M[sp]=-M[sp]
        self.check_parameters(0, parameters)
        self.M.changeTop(-self.M.peek())

    def run_abs(self,parameters):
        # Absolute Value M[sp]=abs(M[sp])
        self.check_parameters(0, parameters)
        self.M.changeTop(abs(self.M.peek()))

    def run_and(self,parameters):
        # Logical And M[sp-1]=M[sp-1]andM[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() and m)        

    def run_lor(self,parameters):
        # Logical Or M[sp-1]=M[sp-1]orM[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() or m)        

    def run_not(self,parameters):
        # Logical Not M[sp]= notM[sp]
        self.check_parameters(0, parameters)
        self.M.changeTop(not self.M.peek())        

    def run_les(self,parameters):
        # Less M[sp-1]=M[sp-1]<M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() < m)        

    def run_leq(self,parameters):
        # Less or Equal M[sp-1]=M[sp-1]<=M[sp]; sp=sp-1       
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() <= m)        

    def run_grt(self,parameters):
        # Greater M[sp-1]=M[sp-1]>M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() > m)        

    def run_gre(self,parameters):
        # Greater or Equal M[sp-1]=M[sp-1]>=M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() >= m)        

    def run_equ(self,parameters):
        # Equal M[sp-1]=M[sp-1]==M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() == m)            

    def run_neq(self,parameters):
        # Not Equal M[sp-1]=M[sp-1]!=M[sp]; sp=sp-1
        self.check_parameters(0, parameters)
        m = self.M.pop()
        self.M.changeTop(self.M.peek() != m)            

    def run_jmp(self,parameters):
        # Jump pc=p 
        self.check_parameters(1, parameters)
        self.pc = int(parameters[0])-1
        
    def run_jof(self,parameters):
        # Jum on False if not M[sp]: pc=p else: pc=pc+1; sp=sp-1
        self.check_parameters(1, parameters)
        if not self.M.pop() :
            self.pc = int(parameters[0])

    def run_alc(self, parameters):
        # Allocate memory sp=sp+n
        self.check_parameters(1, parameters)
        n = int(parameters[0])
        for a in range(0,n):
            self.M.push(0)

    def run_dlc(self,parameters):
        # Deallocate memory sp=sp-n
        self.check_parameters(1, parameters)
        n = int(parameters[0])
        for a in range(0,n):
            self.M.pop()

    def run_cfu(self,parameters):
        # Call Function sp=sp+1; M[sp]=pc+1; pc=p
        self.check_parameters(1, parameters)
        self.M.push(self.pc+1)
        self.pc = int(parameters[0])-1

    def run_enf(self,parameters):
        # Enter Function sp=sp+1; M[sp]=D[k]; D[k]=sp+1
        self.check_parameters(1, parameters)
        k = int(parameters[0])
        self.M.push(self.D[k])
        self.D[k] = self.M.pointer()+1

    def run_ret(self,parameters):
        # Return from Function D[k]=M[sp]; pc=M[sp-1]; sp=sp-(n+2)
        self.check_parameters(2, parameters)
        k = int(parameters[0])
        n = int(parameters[1])
        self.D[k] = self.M.pop()
        self.pc = self.M.pop()-1
        for a in range(0,n):
            self.M.pop()
        
    def run_idx(self,parameters):
        # Index M[sp-1]=M[sp-1]+M[sp]*k; sp=sp-1
        self.check_parameters(1, parameters)
        k = int(parameters[0])
        m = self.M.pop()
        self.M.changeTop(self.M.peek() + m * k)

    def run_grc(self,parameters):
        # Get(Load) Reference Contents M[sp]=M[M[sp]]
        self.check_parameters(0, parameters)
        self.M.changeTop(self.M[self.M[self.M.peek()]])

    def run_lmv(self,parameters):
        # Load multiple values t=M[sp]; M[sp:sp+k]=M[t:t+k]; sp+=(k-1)
        self.check_parameters(1, parameters)
        k = int(parameters[0])
        m = self.M.pop()
        for a in range(0,k):
            self.M.push(self.M[m+a])

    def run_smv(self,parameters):
        # Store multiple Values t=M[sp-k]; M[t:t+k]=M[sp-k+1:sp+1]; sp-=(k+1)
        self.check_parameters(1, parameters)
        k = int(parameters[0])
        m = self.M[self.M.pointer()-k]
        for a in reversed(range(0,k)):
            self.M[m+a] = self.M.pop()        
        self.M.pop()

    def run_smr(self,parameters):
        # Store multiple References t1=M[sp-1]; t2=M[sp]; M[t1:t1+k]=M[t2:t2+k]; sp-=1
        self.check_parameters(1, parameters)
        k = int(parameters[0])
        m2 = self.M.pop()
        m1 = self.M.peek()
        for a in range(0,k):
            self.M[m1+k] = self.M[m2+k]
    
    def run_sts(self,parameters):
        # Store string constant on reference adr=M[sp]; M[adr]=len(H[k]); for c in H[k]: adr=adr+1 M[adr]=c; sp=sp-1
        self.check_parameters(1, parameters)
        k = int(parameters[0])
        m = self.M.pop()
        self.M[m] = len(self.H[k])
        for c in self.H[k] :
            m = m+1
            self.M[m] = c

    def run_rdv(self, parameters):
        # Read single Value sp=sp+1; M[sp]=input()
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

