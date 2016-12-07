import functools
import re

import pyeda.inter as pinter

def get_operand(G, F, operand):
    name, ind = operand[0], int(operand[1:]) - 1
    if name == 'G':
        g = G[ind]
        if g is None:
            raise ValueError("G operand {} is referenced before assignment".format(ind + 1))
        return g
    return F[ind]

def assign(left, right, operand):
    if operand == '+':
        return left | right
    else:
        return left & right

def read_file(path):
    with open(path) as inp:
        count_G, count_F = (int(x) for x in inp.readline().split())
        G = [None for _ in range(count_G)]
        F = [pinter.exprvar("F" + str(i)) for i in range(count_F)]
        probs = [float(x) for x in inp.readline().split()]
        if len(probs) != count_F:
            raise ValueError("Wrong number of probabilities!")
        for ind, s in enumerate(inp):
            s = s.split()
            if not re.search(r"^G[\d]+:$", s[0]):
                raise TypeError("Not 'G%number%:' expression at string {}".format(ind + 1))
            
            G_ind = int(s[0][1:-1]) - 1
            
            if not 0 <= G_ind < count_G:
                raise ValueError("G index {} is out of range".format(G_ind + 1))
            if not re.search("^[F,G][\d]+$", s[1]):
                raise TypeError("Wrong first operand at string {}".format(ind + 1))
            if not re.search("^[F,G][\d]+$", s[3]):
                raise TypeError("Wrong second operand at string {}".format(ind + 1))
            if s[2] not in ("+", "*"):
                raise TypeError("Operator at string {} is not among '+' or '*'".format(ind + 1))
            
            left = get_operand(G, F, s[1])
            right = get_operand(G, F, s[3])
            G[G_ind] = assign(left, right, s[2])
    return F, G, probs

def evaluate_dnf(dnf, values):
    conjucts = re.findall("And\(.+?\)", dnf)
    conj_indexes = [set(int(x) for x in re.findall('[\d]+', a)) for a in conjucts]
    return sum(functools.reduce(lambda x, y: x*y,
        [values[i] for i in conj_ind]) for conj_ind in conj_indexes)

if __name__ == "__main__":
    path = "input.txt"
    F, G, probs = read_file(path)
    DNF = G[-1].to_dnf()
    print("Final DNF: ", DNF)
    print("Probability: ", evaluate_dnf(str(DNF), probs))
