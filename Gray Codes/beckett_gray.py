
from itertools import permutations
import argparse

# here we get the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--all_solutions", action = "store_true")
parser.add_argument("-b", "--beckett_gray_codes", action="store_true")
parser.add_argument("-u", "--unfinished_beckett_gray_codes", action = "store_true")
parser.add_argument("-c", "--cyclic_codes", action="store_true")
parser.add_argument("-p", "--path_codes", action = "store_true")
parser.add_argument("-r", "--reverse_isomorphism", action="store_true")
parser.add_argument("-f", "--full_binary_solution", action = "store_true")
parser.add_argument("-m", "--matrix", action="store_true")
parser.add_argument("number_of_bits", type=int)
args = parser.parse_args()

n = args.number_of_bits # number of bits to start

# initialization of some lists for the dfs algorithm
x_list = [[0] * n] # initial nodes list
visited = [False] * (2**n) # initialize the visited list (all unvisited except for the first node)
visited[0] = True # the first node is visited

all_nodes = [] # all the nodes from the initial gray list for the n bits
final_codes = [] # all the gray codes for n bits
all_delta = [] # all the delta sequencies for n bits

delta = [] # the delta sequence each iteration
# beckett = []
# beckett_delta = []
all_beckett = [] # all the beckett-gray codes
all_beckett_delta = [] # all the beckett-gray delta sequencies
h = []
r = []
f = [] # condition to find the beckett-gray codes

def flip(x, i):
    if x_list[x][-1-i] == 0:
        k = [t for t in x_list[x]]
        k[-1-i] = 1
        if k not in x_list:
            x_list.append(k)
    elif x_list[x][-1-i] == 1:
        k = [t for t in x_list[x]]
        k[-1-i] = 0
        if k not in x_list:
            x_list.append(k)
    for l in range(len(x_list)):
        if x_list[l] == k:
            return l

def find_paths(f_codes, delta_f):
    c = 0
    k = 0
    for i in range(len(f_codes[-1])):
        if f_codes[-1][-1-i] != f_codes[0][-1-i]:
            c += 1
            k = i
    if c > 1:
        pass
        # print("its a path, not a cycle")
    else:
        delta_f.append(k)

def gc_dfs(d, x, max_coord, n, gc):
    global h
    if d == 2**n:
        node_list = gc[:] # we need copies without reference of the lists, because they change dynamically
        all_nodes.append(node_list)
        f_codes = [x_list[i] for i in gc]
        final_codes.append(f_codes)
        delta_f = delta[:] # [d for d in delta]
        find_paths(f_codes, delta_f) # we update the delta sequencies for the cyclic codes with the last position
        f_delta = delta_f[:]
        all_delta.append(f_delta)
        if False not in f:
            beckett = f_codes[:]
            beckett_delta = f_delta[:]
            all_beckett.append(beckett)
            all_beckett_delta.append(beckett_delta)
        return
    for i in range(0, min(n - 1, max_coord) + 1): # from the minimum to max coordinate from the left
        x = flip(x, i) # change the bit accordingly
        if not visited[x]:
            visited[x] = True
            gc.append(x)
            delta.append(i) # insert the position to the delta sequence
            if len(r) != 0:
                h = [p for p in r[-1]]
            if x_list[x][-1-i] == 1:
                h.append(i)
                u = h[:]
                r.append(u)
                f.append(True)
            elif x_list[x][-1-i] == 0:
                if len(h) != 0:
                    y = h.pop(0)
                    u = h[:]
                    r.append(u)
                    if i == y:
                        f.append(True)
                    else:
                        f.append(False)
            gc_dfs(d+1, x, max(i+1, max_coord), n, gc) # go to the next step recursively
            visited[x] = False # when coming back from the recursion, we say we haven't visited the node so we can explore it again
            gc.pop() # extract the node
            delta.pop() # extract the position
            if len(r) != 0:
                r.pop()
            if len(f) != 0:
                f.pop()
        x = flip(x, i) # if we have visited the node, change the bit back and search for the next node

# method for finding cycles with (2**n) bits, paths with (2**n - 1)
def paths(codes, delta):
    paths_co = []
    paths_de = []
    for d in range(len(codes)):
        if len(delta[d]) != 2**n:
            paths_co.append(codes[d])
            paths_de.append(delta[d])
    return paths_co, paths_de

# method for finding paths with (2**n - 1)
def cycles(codes, delta):
    cycles_co = []
    cycles_de = []
    for d in range(len(codes)):
        if len(delta[d]) == 2**n:
            cycles_co.append(codes[d])
            cycles_de.append(delta[d])
    return cycles_co, cycles_de

# print the delta sequencies for all codes
def print_result_all(delta, cycles_de, paths_de):
    for i in range(len(delta)):
        if delta[i] in cycles_de:
            letter = "C "
        elif delta[i] in paths_de:
            letter = "P "
        print(letter, end="")
        for j in range(len(delta[i])):
            print(delta[i][j], end="")
        print()

# print the delta sequencies for specific codes
def print_result(delta, letter):
    for i in range(len(delta)):
        print(letter, end="")
        for j in range(len(delta[i])):
            print(delta[i][j], end="")
        print()

def print_binary_all(delta, codes, cycles_de, paths_de):
    for i in range(len(delta)):
        if delta[i] in cycles_de:
            letter = "C "
        elif delta[i] in paths_de:
            letter = "P "
        print(letter, end="")
        for j in range(len(codes[i])):
            for l in (codes[i][j]):
                print(l, end="")
            print(end=" ")
        print()

def print_binary(delta, codes, letter):
    for i in range(len(delta)):
        print(letter, end="")
        for j in range(len(codes[i])):
            for l in (codes[i][j]):
                print(l, end="")
            print(end=" ")
        print()

# method for finding and printing reverse isomorphisms
def permut(delta, c):
    for d in delta:
        for j in list(permutations(d)):
            j = list(j)
            if j.reverse() in delta:
                print(d + " <=> " + j.reverse())
                c += 1
            if c == (2**n)/2:
                break

# finding and printing the codes in matrix type
def find_matrix(delta, codes, letter):
    k = []
    for code in range(len(codes)):
        l2 = list(map(list, zip(*codes[code])))
        k.append(l2[::-1])
    for i in range(len(k)):
        print(letter, end="")
        for j in range(len(delta[i])):
            print(delta[i][j], end="")
        print()
        for j in range(len(k[i])):
            for l in k[i][j]:
                print(l, end=" ")
            print()

# checking the arguments and printing the results
def result():
    if args.all_solutions:
        codes = final_codes
        delta = all_delta
        cycles_co, cycles_de = cycles(final_codes, all_delta)
        paths_co, paths_de = paths(final_codes, all_delta)
        print_result_all(delta, cycles_de, paths_de)
    elif args.beckett_gray_codes:
        letter = "B "
        codes = all_beckett
        delta = all_beckett_delta
        if not args.matrix:
            print_result(delta, letter)
    elif args.unfinished_beckett_gray_codes:
        letter = "U "
        paths_co, paths_de = paths(all_beckett, all_beckett_delta)
        codes = paths_co
        delta = paths_de
        if not args.matrix:
            print_result(delta, letter)
    elif args.cyclic_codes:
        letter = "C "
        cycles_co, cycles_de = cycles(final_codes, all_delta)
        codes = cycles_co
        delta = cycles_de
        if not args.matrix:
            print_result(delta, letter)
    elif args.path_codes:
        letter = "P "
        paths_co, paths_de = paths(final_codes, all_delta)
        codes = paths_co
        delta = paths_de
        if not args.matrix:
            print_result(delta, letter)
    else:
        codes = final_codes
        delta = all_delta
        cycles_co, cycles_de = cycles(final_codes, all_delta)
        paths_co, paths_de = paths(final_codes, all_delta)
        print_result_all(delta, cycles_de, paths_de)
    if args.reverse_isomorphism:
        permut(delta, 0)
    if args.full_binary_solution:
        if args.all_solutions:
            print_binary_all(delta, codes, cycles_de, paths_de)
        else:
            print_binary(delta, codes, letter)
    if args.matrix:
        find_matrix(delta, codes, letter)

def solution():
    gc_dfs(1, 0, 0, n, [0])
    sol = result()
    return sol
solution()
