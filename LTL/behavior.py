from graph import Graph
from match import match
from stack import SStack

def corresponding(s, a, AP):
    ops = {'X', 'not', 'U'}
    for f in a:
        if f == s or f == 'True':
            continue
        op, f1, f2 = match(f, AP)
        if f1[0] == '(' and f1[-1] == ')':
            f1 = f1[2: len(f1) - 2]
        if op == 'not' and f1 == s:
            return False
        if not op in ops:
            return False
    return True

def build_behavior(tableau, ts, AP):
    st = SStack()
    nodes = []
    for a in tableau.get_init():
        for s in ts.get_init():
            if corresponding(s, a, AP):
                nodes.append((s, a))
                st.push((s, a))
    mat = [[0] * len(nodes) for i in nodes]
    behavior = Graph(nodes, mat)
    while not st.is_empty():
        s, a = st.pop()
        for s1, w in ts.out_edges(ts.get_index(s)):
            s1 = ts.get_vertex(s1)
            for a1, w1 in tableau.out_edges(tableau.get_index(a)):
                a1 = tableau.get_vertex(a1)
                if corresponding(s1, a1, AP):
                    if not behavior.vertex_exist((s1, a1)):
                        behavior.add_vertex((s1, a1))
                        st.push((s1, a1))
                    behavior.add_edge((s, a), (s1, a1))
    return behavior