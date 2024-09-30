from graph import Graph

class TS(Graph):
    def __init__(self, inits, nodes, mat, unconn=0):
        super().__init__(nodes, mat)
        self._init = inits
    
    def get_init(self):
        return self._init

def build_ts(in_file_name):
    formulas = []
    inf = open(in_file_name)
    states = inf.readline().strip().split()
    inits = inf.readline().strip().split()
    mat = [[0] * len(states) for i in states]
    ts = TS(inits, states, mat)

    for line in inf:
        if line.isspace():
            break
        t,s1,s2 = line.strip().split()
        ts.add_edge(s1,s2,t)
    
    for line in inf:
        formulas.append(line.strip())
    inf.close()

    return ts, formulas, states