from match import match
from graph import *

class Tableau(Graph):
    def __init__(self, nodes, mat, f):
        super().__init__(nodes, mat)
        self._init = [atom for atom in nodes if f in atom]

    def get_init(self):
        return self._init

def build_tableau(atoms, f, AP):
    
    def edge_exist(a, b, AP):
        for f in a:
            op, f1, f2 = match(f, AP)
            if op == 'X' and f1 not in b:
                return False
        for f in b:
            if f in AP and 'X ( ' + f + ' )' not in a:
                return False
        return True
    
    n = len(atoms)
    mat = [[1 if edge_exist(atoms[i], atoms[j], AP) else 0\
        for j in range(n)] for i in range(n)]
    tableau = Tableau(atoms, mat, f)
    return tableau

def realizable(closure, f, nodes, AP):
    def realizable0(f, nodes):
        for atom in nodes:
            if f in atom:
                return True
        return False
    for f in closure:
        op, f1, f2 = match(f, AP)
        if op == 'U' and not realizable0(f2, nodes) and \
        not realizable0('not ( ' + f + ' )', nodes):
            return False
    return True

def prune_tableau(tableau, closure, f, AP, atoms):

    def reachable(tableau, nodes):#if nodes is f-reachable
        for node in nodes:
            vi = tableau.get_index(node)
            for init in tableau.get_init():
                vj = tableau.get_index(init)
                if vi in DFS_graph(tableau, vj):
                    return True
        return False

    def isterminate(tableau, nodes):
        for node in nodes:
            v = tableau.get_index(node)
            for u, w in tableau.out_edges(v):
                if tableau.get_vertex(u) not in nodes:
                    return False
        return True

    scss = divide_scs(tableau)
    for nodes in scss:
        if not reachable(tableau, nodes):
            for v in nodes:
                tableau.del_vertex(v)
        if isterminate(tableau, nodes) and not realizable(closure, f, nodes, AP):
            for v in nodes:
                tableau.del_vertex(v)

    return tableau