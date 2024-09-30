# class LTLtree:
#     def __init__(self, data=None, left=None, right=None):
#         self._data = data
#         self._left = left
#         self._right = right
#     def is_empty(self):
#         return self._data is None
#     def root(self):
#         return self._data
#     def left(self):
#         return self._left
#     def right(self):
#         return self._left
#     def set_root(self, data):
#         self._data = data
#     def set_left(self, left):
#         self._left = left
#     def set_right(self, right):
#         self._right = right

class LTLtree:
    def __init__(self, data=None, left=None, right=None):
        self._data = data
        self._left = left
        self._right = right
    def is_empty(self):
        return self._data is None
    def root(self):
        return self._data
    def left(self):
        return self._left
    def right(self):
        return self._left
    def set_root(self, data):
        self._data = data
    def set_left(self, left):
        self._left = left
    def set_right(self, right):
        self._right = right

    def __str__(self):
        preorder(self, )

def preorder(t, proc):
    if t is None:
        return
    proc(t.root())
    preorder(t.left(), proc)
    preorder(t.right(), proc)        
t = LTLtree(1)
print(t.root())
print(LTLtree(1))
print(LTLtree(1, LTLtree(2), LTLtree(3)))

# def build_LTLtree(f, t, AP):
#     if f[0] == '(' and f[-1] == ')':
#         f = f[2: len(f) - 2]
#     f = f.split()
#     operators = {'and', 'not', 'X', 'U'}
#     paren = 0
#     op = None
#     pos = 0
#     for i in range(len(f)):
#         if f[i] in operators and paren == 0:
#             op, pos = f[i], i 
#         elif f[i] == '(':
#             paren += 1
#         elif f[i] == ')':
#             paren -= 1
#         else:
#             continue

#     if op == None:
#         if f[0] == 'True' or f[0] in AP:
#             t.set_root(f[0])
#         else:
#             raise ValueError(op, pos)
#     elif op == 'not' and f[1] in AP:
#         t.set_root('not')
#         t.set_left('f[1]')
#     elif op == 'and':
#         t.set_root('and')
#         t.set_left(LTLtree()); t.set_right(LTLtree())
#         build_LTLtree(' '.join(f[:pos]), t.left(), AP)
#         build_LTLtree(' '.join(f[pos + 1:]), t.right(), AP)
#     elif op == 'X':
#         t.set_root('X')
#         t.set_left(LTLtree())
#         build_LTLtree(' '.join(f[1:]), t.left(), AP)
#     elif op == 'U':
#         t.set_root('U')
#         t.set_left(LTLtree()); t.set_right(LTLtree())
#         build_LTLtree(' '.join(f[:pos]), t.left(), AP)
#         build_LTLtree(' '.join(f[pos + 1:]), t.right(), AP)
#     else:
#         raise ValueError(op, pos)

# AP = {'a', 'b', 'c', 'd'}
# while True:
#     f = input()
#     if f == 'quit':
#         break
#     t = LTLtree()
#     build_LTLtree(f, t, AP)
#     print(t)