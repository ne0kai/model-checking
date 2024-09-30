class GraphError(TypeError):
    pass

class Graph:
    def __init__(self, nodes, mat):
        vnum = len(mat)
        for x in mat:
            if len(x) != vnum:
                raise ValueError("Argument for 'Graph'.")
        self._nodes = list(nodes)
        self._mat = [mat[i] for i in range(vnum)]
        self._vnum = vnum

    def vertex_num(self):
        return self._vnum

    def _invalid(self, v):
        return 0 > v or v >= self._vnum

    def vertex_exist(self, val):
        return val in self._nodes

    def add_vertex(self, val=None):
        if val in self._nodes:
            return
        self._vnum += 1
        self._nodes.append(val)
        for row in self._mat:
            row.append(0)
        self._mat.append([0] * self._vnum)

    def add_edge(self, vi, vj, val=1):
        vi = self._nodes.index(vi)
        vj = self._nodes.index(vj)
        self._mat[vi][vj] = val

    def del_vertex(self, val):
        v = self._nodes.index(val)
        for row in self._mat:
            row[v] = None
        self._mat[v] = [None] * self._vnum

    def get_vertex(self, v):
        return self._nodes[v]

    def get_index(self, val):
        return self._nodes.index(val)

    def get_edge(self, vi, vj):
        if self._invalid(vi) or self._invalid(vj):
            raise GraphError
        return self._mat[vi][vj]

    def out_edges(self, vi):
        if 0 > vi or vi >= self._vnum:
            raise GraphError
        return self._out_edges(self._mat[vi])

    @staticmethod
    def _out_edges(row):
        edges = []
        for i in range(len(row)):
            if row[i] != 0:
                edges.append((i, row[i]))
        return edges

from stack import SStack

def DFS_graph(graph, v0):
    vnum = graph.vertex_num()
    visited = [0] * vnum
    visited[v0] = 1
    dfs_seq = [v0]
    st = SStack()
    st.push((0, graph.out_edges(v0)))
    while not st.is_empty():
        i, edges = st.pop()
        if i < len(edges):
            v, e = edges[i]
            st.push((i + 1, edges))
            if not visited[v]:
                dfs_seq.append(v)
                visited[v] = 1
                st.push((0, graph.out_edges(v)))
    return dfs_seq

def divide_scs(graph):
    scss = []
    vnum = graph.vertex_num()
    visited = [None] * vnum
    def scs(graph, v):
        nonlocal visited, nodes
        for u, w in graph.out_edges(v):
            if not visited[u] and graph.get_edge(u, v):
                nodes.add(graph.get_vertex(u))
                visited[u] = 1
                scs(graph, u)
    for v in range(vnum):
        if not visited[v]:
            nodes = set()
            scs(graph, v)
            scss.append(nodes)
    return scss

# m = [[0, 1, 1, 0, 1], \
#      [1, 0, 1, 0, 0], \
#      [1, 1, 0, 0, 0], \
#      [0, 0, 0, 0, 1], \
#      [0, 0, 0, 1, 0]]

# nodes = 'abcde'
# g = Graph(nodes, m)
# g.add_vertex('f')
# print(g._mat, g._nodes)
# print(divide_scs(g))