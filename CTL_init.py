def LTL(in_file_name,out_file_name):
    class SStack():
        def __init__(self):
            self.elems = []
        def push(self,a):
            self.elems.append(a)
        def pop(self):
            if self.elems == []:
                raise ValueError
            return self.elems.pop()
        def top(self):
            if self.elems == []:
                raise ValueError
            return self.elems[-1]
        def is_empty(self):
            return self.elems == []
        
    labels= ['True']
    class state:
        def __init__(self,Name):
            self.name = Name
            self.label = set()
        def add_label(self,n):
            self.label.add(n)
        def check_label(self,n):
            return n in self.label

    class TS:
        def __init__(self):
            self.all_state = set()
            self.init_state = set()
            self.transition = {}
        def add_state(self,s):
            self.all_state.add(s)
            s.add_label(new_label(s.name))
            s.add_label(0)
        def add_init_state(self,s):
            self.init_state.add(s)
        def add_transition(self,t,s1,s2):
            if self.transition.get(s2) == None:
                self.transition[s2] = [s1]
            else:
                if not s1 in self.transition[s2]:
                    self.transition[s2].append(s1)
        def label_state(self,num,num1,num2 = None,sign = None):
            
            if sign == 'not':
                for s in self.all_state:
                    if not s.check_label(num1):
                        s.add_label(num)
            elif sign == 'and':
                num,num_ = num
                for s in self.all_state:
                    if s.check_label(num1) and s.check_label(num2):
                        s.add_label(num)
                        s.add_label(num_)
            elif sign == 'EX':
                for s in self.all_state:
                    if s.check_label(num1):
                        if self.transition.get(s) != None:
                            for s_pre in self.transition[s]:
                                s_pre.add_label(num)
            elif sign == 'EG':
                sub = set()
                for s in self.all_state:
                    if s.check_label(num1):
                        sub.add(s)
                pre_count = 0
                count = 1
                while count != pre_count and len(sub) > 0:
                    pre_count = count
                    for s in sub:
                        if self.transition.get(s) != None:
                            for ss in self.transition[s]:
                                if ss in sub:
                                    break
                            else:
                                sub.remove(s)
                                count += 1
                for s in sub:
                    s.add_label(num)
                        
            elif sign == 'EU':
                for s in self.all_state:
                    if s.check_label(num2):
                        s.add_label(num)
                        st = SStack()
                        if self.transition.get(s) != None:
                            st.push((0,self.transition[s]))
                        while not st.is_empty():
                            i, edges = st.pop()
                            if edges and i < len(edges):
                                v = edges[i]
                                st.push((i+1,edges))
                                if not v.check_label(num):
                                    v.add_label(num)
                                    if self.transition.get(v) != None:
                                        st.push((0,self.transition[v]))

    def new_label(l):
        if l in labels:
            return labels.index(l)
        else:
            labels.append(l)
            return len(labels)-1
    def anti(s):
        pass
    
    #读入文件&初始化
    ts = TS()
    formulas = []
    inf = open(in_file_name)
#    out_f = open(out_file_name,'w')
    line0 = inf.readline()
    line0 = line0.split()
    line1 = inf.readline()
    line1 = line1.split()
    for s_name in line0:
        s = state(s_name)
        ts.add_state(s)
        if s_name in line1:
            ts.add_init_state(s)
    for line in inf:
        if line.isspace():
            break
        t,s1_name,s2_name = line.split()
        flag = 0
        for s in ts.all_state:
            if s.name == s1_name:
                s1 = s
                flag += 1
            if s.name == s2_name:
                s2 = s
                flag += 1
            if flag == 2:
                break
        ts.add_transition(t,s1,s2)
    
    for line in inf:
        formulas.append(line)
    inf.close()
    
    for f in formulas:
        if not f or f.isspace():
            continue
        f = f.split()
        f.reverse()
        st0 = SStack()
        for i in f:
            st0.push(i)
        st_ = SStack() 
        operation = []
        operation_str = []
        while not st0.is_empty():
            a = st0.pop()
            if a == ')':
    
                lst = []
                while st_.top() != '(':
                    lst.append(st_.pop())
                st_.pop()
                st_.push('*')
                lst.reverse()
                operation.append(lst)
            else:
                st_.push(a)
        lst = []
        while not st_.is_empty():
            lst.append(st_.pop())
        lst.reverse()
        operation.append(lst)
        for j in range(len(operation)):
            op = operation[j]
            if '*' in op:
                llst = op[0:op.index('*')]+['(']+[operation_str[j-1]]+[')']+op[op.index('*')+1:]
                operation_str.append(' '.join(llst))
            else:
                operation_str.append(' '.join(op))
            if len(op) == 2:
                if op[1] == '*':
                    ts.label_state(new_label(operation_str[j]),new_label(operation_str[j-1]),None,op[0])
                else:
                    ts.label_state(new_label(operation_str[j]),new_label(op[1]),None,op[0])
            elif len(op) == 3:
                tmpa = new_label(operation_str[j])
                if op[0] == '*' and op[2] == '*':
                    if op[1] == 'and':
                        tmpa = (tmpa,new_label('( '+op[2]+' ) and ( '+ op[0]+' )'))
                    ts.label_state(tmpa,new_label(operation_str[j-2]),new_label(operation_str[j-1]),op[1])
                elif op[0] == '*' and op[2] != '*':
                    if op[1] == 'and':
                        tmpa = (tmpa,new_label(op[2]+' and ( '+ op[0]+' )'))
                    ts.label_state(tmpa,new_label(operation_str[j-1]),new_label(op[2]),op[1])
                elif op[0] != '*' and op[2] == '*':
                    if op[1] == 'and':
                        tmpa = (tmpa,new_label('( '+op[2]+' ) and '+ op[0]))
                    ts.label_state(tmpa,new_label(op[0]),new_label(operation_str[j-1]),op[1])
                else:
                    if op[1] == 'and':
                        tmpa = (tmpa,new_label(op[2]+' and '+ op[0]))
                    ts.label_state(tmpa,new_label(op[0]),new_label(op[2]),op[1])
#        for i_s in ts.init_state:
#            if not i_s.check_label(labels.index(operation_str[-1])):
#                out_f.write('False   '+'?'+'   \n')
#                break
#        else:
#            out_f.write('True\n')
#    out_f.close()                
        for i_s in ts.init_state:
            if not i_s.check_label(labels.index(operation_str[-1])):
                print('False')
                break
        else:
            print('True')
                

    
LTL('a.txt',None)    