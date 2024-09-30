def match(f, AP):#f is string of LTL formula, AP is a set of Atomic Properties
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
            return (op, f[0], None)
        raise ValueError(op, pos)
    elif op == 'not':
        return (op, ' '.join(f[1:]), None)
    elif op == 'and':
        return (op, ' '.join(f[:pos]), ' '.join(f[pos + 1:]))
    elif op == 'X':
        return (op, ' '.join(f[1:]), None)
    elif op == 'U':
        return (op, ' '.join(f[:pos]), ' '.join(f[pos + 1:]))
    else:
        raise ValueError(op, pos)