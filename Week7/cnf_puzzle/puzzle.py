import argparse
import itertools
import os
import sys
import numpy as np
from pysat.solvers import Glucose3

def readMat(path):
    f = open(path, 'rt')
    h, w = map(int, f.readline().strip().split())
    assert h > 0 and w > 0
    mat = np.zeros((h, w), dtype=int)
    for ih in range(h):
        iw = 0
        for it in f.readline().strip().split():
            if it.isdigit():
                mat[ih][iw] = int(it)
            else:
                mat[ih][iw] = -1
            iw += 1
    f.close()
    return mat

def toCNF(mat):
    clauses = []
    h, w = mat.shape
    for i in range(h):
        for j in range(w):
            if mat[i][j] >= 0:
                clauses += getClauses(mat, i, j)
    return clauses

def getClauses(mat, ih, iw):
    clauses = []
    
    # Case 1: At least mat[ih][iw] + 1 adjacent cells are selected
    lits_1 = []
    for comb in itertools.combinations(getAllAdjacent(mat, ih, iw), mat[ih][iw] + 1):
        lits_1.append([-x for x in comb])
    clauses.extend(lits_1)
    
    # Case 2: Exactly len(getAllAdjacent(mat, ih, iw)) - mat[ih][iw] + 1 adjacent cells are selected
    lits_2 = []
    for comb in itertools.combinations(getAllAdjacent(mat, ih, iw), len(getAllAdjacent(mat, ih, iw)) - mat[ih][iw] + 1):
        lits_2.append(list(comb))
    clauses.extend(lits_2)
    
    return clauses

def getAllAdjacent(mat, ih, iw):
    res = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            ii = i + ih
            jj = j + iw
            if validCell(ii, jj, mat.shape) and lvars[ii][jj] not in res:
                res.append(lvars[ii][jj])
    return res

def validCell(i, j, shape):
    return 0 <= i < shape[0] and 0 <= j < shape[1]

def initVars(mat):
    ivar = 1
    lvars = np.zeros(mat.shape, dtype=np.int32)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            lvars[i, j] = ivar
            ivar += 1
    return lvars, ivar - 1

def solveCNFs(clauses):
    g = Glucose3()
    for clause in clauses:
        int_clause = [int(var) for var in clause]
        g.add_clause(int_clause)
    ret, result = g.solve(), None
    if ret:
        result = g.get_model()
    
    return ret, result

def fortmatFilledCell(text, cl_code):
    return '\033[1;37;%dm%s\033[1;0;0m'%(cl_code, text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', help='The puzzle file', default='maze.txt')
    parser.add_argument('--outfile', help='The output file', default='output.txt')
    args = parser.parse_args()
    
    mat = readMat(args.infile)
    
    lvars, num = initVars(mat)
    clauses = toCNF(mat)
    
    print("Clauses:", clauses)  # 1
    ret, res = solveCNFs(clauses)
    print("Solved:", ret, res)  # 2

    if res is None:
        print("No solution")  # 3
        sys.exit(0)

    ret, res = solveCNFs(clauses)

    vis_str = ''
    with open(args.outfile, 'wt') as g:
        for ih in range(mat.shape[0]):
            for iw in range(mat.shape[1]):
                txt = ''
                if mat[ih][iw] >= 0:
                    g.write('%d'%(mat[ih][iw]))
                    txt += '%-2d'%(mat[ih, iw])
                else:
                    g.write(' ')
                    txt += '  '

                if lvars[ih][iw] in res:
                    g.write('.')
                    vis_str += fortmatFilledCell(txt, 42)
                else:
                    g.write(' ')
                    vis_str += fortmatFilledCell(txt, 41)
            g.write('\n')
            vis_str += '\n'

    print ('\n=======INPUT=======')

    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i][j] < 0:
                print ('_', end='')
            else:
                print (mat[i][j], end='')
        print ('')
    print ('===================')
    print ('\n=======ANSWER=======')
    print (vis_str,'=====================')