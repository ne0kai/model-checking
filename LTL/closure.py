from match import match

def build_closure(closure, f, AP):
    if f[0] == '(' and f[-1] == ')':
        f = f[2: len(f) - 2]
    closure.add(f)
    op, f1, f2 = match(f, AP)
    if op == 'not':
        if f1[0] == '(' and f1[-1] == ')':
            f1 = f1[2: len(f) - 2]
        closure.add(f1)
    else:
        closure.add('not ( ' + f + ' )')
    if op == None:
        pass
    elif op == 'and':
        build_closure(closure, f1, AP)
        build_closure(closure, f2, AP)
    elif op == 'X' or 'not':
        build_closure(closure, f1, AP)
    elif op == 'U':
        closure.add('X ( ' + f + ' )')
        closure.add('not ( X ( ' + f + ' ) )')
        build_closure(closure, f1, AP)
        build_closure(closure, f2, AP)
    else:
        raise ValueError(op, f1, f2)

def determine(f, atom, AP):
    if f[0] == '(' and f[-1] == ')':
        f = f[2: len(f) - 2]
    if f in atom:
        return True
    op, f1, f2 = match(f, AP)
    if op == 'not':
        return not determine(f1, atom, AP)
    elif op == 'and':
        return determine(f1, atom, AP) and determine(f2, atom, AP)
    elif op == 'U':
        return determine(f1, atom, AP) or determine('X ( ' + f + ' )', atom, AP)
    else:
        return False

def build_atoms(closure, AP):
    basics = set()
    for f in closure:
        op, f1, f2 = match(f, AP)
        if op == None or op == 'X':
            basics.add(f)
    basics = list(basics)
    n = len(basics)
    atoms = [set() for k in range(2**n)]
    for i in range(n):
        interval = 2**i
        p = basics[i]
        for j in range(2**n):
            if j % (interval * 2) < interval:
                atoms[j].add(p)
            else:
                atoms[j].add('not ( ' + p + ' )')
    for atom in atoms:
        for f in closure.difference(atom):
            if determine(f, atom, AP):
                atom.add(f)
    frozenatoms = [frozenset(atom) for atom in atoms]
    return frozenatoms