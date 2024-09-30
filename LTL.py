class BuchiNode():
    def __init__(name, incoming)


LTLSet = {}
NodeSet={}

Nodes = set()
Incoming = {}
Now = {}
Next = {}

def create_graph(LTL):
    expand({f}, set(), set(), {init})
    return (Nodes, Now, Incoming)

def expand(curr, old, nxt, incoming):
    global Nodes, Incoming, Now, Next
    if not curr:
        flag = False
        for q in Nodes:
            if Next[q] == nxt and Now[q] == old:
                Incoming[q].update(incoming)
                flag = True
                break
        if not flag:
            q = new_node()
            Nodes.add(q)
            Incoming[q] = incoming
            Now[q] = old
            Next[q] = nxt
            expand(Next(q), set(), set(), {q})
    else:
        f = curr.pop()
        old.add(f)
        indicator, f1, f2 = match(f)
        if indicator == 0:
            if f == 'False' or neg(f) in old:
                continue
            else:
                expand(curr, old, nxt, incoming)
        elif indicator == 1:
            expand(curr.union({f1, f2}.difference(old), old, nxt, incoming))
        elif indicator == 2:
            expand(curr, old, nxt.union{f1}, incoming)
        else:
            expand(curr.union(curr1(f).difference(old), old, nxt.union(next1(f)), incoming))
            expand(curr.union(curr2(f).difference(old), old, nxt, incoming))
    return

def match(f, AP):#f is string of LTL formula, AP is a set of Atomic Properties
    if f[0] == '(' and f[-1] == ')':
        f = f[2: len(f) - 2]
    f = f.split()
    operators = {'and', 'not', 'X', 'U'}
    paren = 0
    op = None
    pos = 0
    for i in range(len(f)):
        if f[i] in operators and paren == 0:
            op, pos = f[i], i 
        elif f[i] == '(':
            paren += 1
        elif f[i] == ')':
            paren -= 1
        else:
            continue

    if op == None:
        if f[0] == 'True' or f[0] in AP:
            return (0, None, None)
        raise ValueError(op, pos)
    elif op == 'not' and f[1] in AP:
        return (0, None, None)
    elif op == 'and':
        return (1, ' '.join(f[:pos]), ' '.join(f[pos + 1:]))
    elif op == 'X':
        return (2, ' '.join(f[1:]), None)
    elif op == 'U':
        return (3, ' '.join(f[:pos]), ' '.join(f[pos + 1:]))
    else:
        raise ValueError(op, pos)