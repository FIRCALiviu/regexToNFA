import copy

class nfa: # "#" is the symbol for lamda and @ for the empty set 
    def __init__(self,s=None):
        if s is None:
            self.delta={}
            self.initial_state=0
            self.final_states=[]
            self.states=[0]
        elif s =='':
            raise ValueError
        else:
            if s=='@':
                self.delta={}
                self.initial_state=0
                self.final_states=[]
                self.states=[0]
            elif s=="#":
                self.initial_state=0
                self.final_states=[0]
                self.delta={}
                self.states=[0]
            else:
                self.initial_state=0
                self.final_states=[1]
                self.delta={0:{s:[1]}}
                self.states=[0,1]

    def update(self,s):
        if s=="":
            raise ValueError("cannot initialize a graph with empty string")
        if s=='@':
            self.delta={}
            self.initial_state=0
            self.final_states=[]
            self.states=[0]
        elif s=="#":
            self.initial_state=0
            self.final_states=[0]
            self.delta={}
            self.states=[0]
        else:
            self.initial_state=0
            self.final_states=[1]
            self.delta={0:{s:[1]}}
            self.states=[0,1]
    def __getitem__(self,key):
        return self.delta[key]


    def __str__(self):
        return str(self.delta)+"\nfinal states:"+ str(self.final_states)+"\nInitial state:" +str(self.initial_state)+"\nAll states: "+str(self.states)
    def __add__(self,x):
        new=nfa()
        new.states=[]
        M=max(x.states)+1
        new.delta=copy.deepcopy(x.delta)
        for first_state in self.delta.keys():
            new.delta[first_state+M]={}
            for edge in self.delta[first_state]:
                new[first_state+M][edge]=[last_state+M for last_state in self.delta[first_state][edge]]
                


        new.final_states.extend([final_state+M for final_state in self.final_states])
        new.final_states.extend(x.final_states)
        new.states.extend([final_state+M for final_state in self.states])
        new.states.extend(x.states)
        new.initial_state=max(new.states)+1
        new.states.append(new.initial_state)
        new.delta[new.initial_state]={"#":[self.initial_state+M,x.initial_state]}

        return new
    def __mul__(self,x):
        new = nfa()
        new.states=[]
        new.delta=copy.deepcopy(self.delta)
        M=max(self.states)+1
        
        new.final_states=[final_state+M for final_state in x.final_states]
        for first_state in x.delta.keys():
            new.delta[first_state+M]={}
            for edge in x.delta[first_state]:
                new[first_state+M][edge]=[final_state+M for final_state in x.delta[first_state][edge]]
        for final_state in self.final_states:
            if new.delta.get(final_state) is None:
                new.delta[final_state]={"#":[x.initial_state+M]}
            elif new.delta[final_state].get('#') is None:
                new.delta[final_state]['#']=[x.initial_state+M]
            else:
                new.delta[final_state]['#'].append(x.initial_state+M)
                
        new.initial_state=self.initial_state
        new.final_states=[final_state+M for final_state in x.final_states]
        new.states.extend(self.states)
        new.states.extend([final_state+M for final_state in x.states])
        return new
    def __invert__(self):
        new = nfa()
        
        new.final_states=self.final_states.copy()
        new.states=self.states.copy()
        new.delta=copy.deepcopy(self.delta)
        M=max(self.states)+1
        new.initial_state=M
        for state in self.final_states:
            if new.delta.get(state) is None:
                new.delta[state]={'#':[M]}
            elif new.delta[state].get("#") is None:
                new.delta[state]['#']=[M]
            else:
                new.delta[state]['#'].append(M)
        new.delta[M]={'#':[self.initial_state]}
        new.final_states.append(M)
        new.states.append(M)
        return new
class evaluator:
    def __init__(self,message):
        if message.lower()=="n":
            self.split=False
        elif message.lower()=="y":
            self.split=True
        else:
            raise ValueError
    @staticmethod
    def __evalnosplit(message):
        message=message.replace(" ","")
        message=message.replace("*","~")
        message=message.replace(".","*")
        tokens=[]
        for char in message:
            if char.isalpha() or char =='@' or char == '#':
                tokens.append("nfa('{}')".format(char))
            else:
                tokens.append(char)
        

        return eval("".join(tokens))
        
    @staticmethod
    def __evalWsplit(message):
        message=message.replace("*","~")
        message=message.replace(".","*")
        tokens=message.split()
        for i,token in enumerate(tokens):
            if token not in "()~+*":
                tokens[i]="nfa('{}')".format(token)
        
        return eval("".join(tokens))


    
    def eval(self,s):
        if self.split==False:
            return evaluator.__evalnosplit(s)
        else:
            return evaluator.__evalWsplit(s)

        
if __name__ == "__main__":
    a,b=nfa("a"),nfa("b")
    print(~a*a)
    
