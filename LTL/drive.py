from ts import build_ts
from closure import build_closure, build_atoms
from tableau import build_tableau, prune_tableau, realizable
from behavior import build_behavior
from graph import divide_scs

def check(f, ts, AP):
    cl = set()
    build_closure(cl, f, AP)
    atoms = build_atoms(cl, AP)
    tb = build_tableau(atoms, f, AP)
    tb = prune_tableau(tb, cl, f, AP, atoms)
    bh = build_behavior(tb, ts, AP)

    scss = divide_scs(bh)
    for scs in scss:
        nodes = [a for s, a in scs]
        if realizable(cl, f, nodes, AP):
            return True
    return False

ts, formulas, AP = build_ts(input())
for f in formulas:
    print(check(f, ts, AP))