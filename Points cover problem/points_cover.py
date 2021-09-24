import argparse
from itertools import combinations

# here we get the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--first_solution", action = "store_true")
parser.add_argument("-g", "--grid_lines_solution", action="store_true")
parser.add_argument("txt_file")
args = parser.parse_args()

def file_open(file): # opening, reading the file and making a list
    points_list = []
    with open (file) as points_file: # read the txt file
        for line in points_file:
            points_l = [int(x) for x in line.split()] # make a list of points of each line
            points = tuple(points_l) # convert it to tuple
            points_list.append(points) # append it to points_list
    return points_list # [(1, 1), (2, 2), ..., (11, 5), (11, 6)]

def find_combinations(points_list, n): # find all the combinations of the points without replacement
    result = combinations(points_list, n) # use of the combinations method from itertools library
    comb_list = []
    for each in result:
        comb_list.append(list(each))
    return comb_list # [[(1, 1), (2, 2)], [(1, 1), (3, 3)], ..., [(11, 4), (11, 6)], [(11, 5), (11, 6)]]

# to find the slope formula of two points -> a = (y2 - y1) / (x2 - x1)
# to find the intercept formula of two points -> b = y1 - a * x1
def slope_intercept_gen(x1, y1, x2, y2): # general function for finding the a, b in a line y=ax+b
    if (x1 == x2): # straight line
        a = "nd" # not defined, vertical line
        b = x1
    else: # any other line
        a = (float)(y2-y1)/(x2-x1)
        b = y1 - a * x1
    return a, b

def find_comb_slope_intercept(comb): # every line between 2 points
    for line in comb:
        k = slope_intercept_gen(line[0][0], line[0][1], line[1][0], line[1][1])
        line.append(list(k))
    return comb # [[(1, 1), (2, 2), [1.0, 0.0]], [(1, 1), (3, 3), [1.0, 0.0]],..., [(11, 4), (11, 6), ['nd', 11]], [(11, 5), (11, 6), ['nd', 11]]]

def find_lone_h_lines(points_list): # horizontal lines with only one point
    new_p1 = [point[1] for point in points_list] # list of y's in the points_list
    h_par = []
    for point in points_list:
        if (new_p1.count(point[1])) < 2: # we want the y's that appear only one time so we can make the extra horizontal lines
            new_point = tuple()
            new_point = (point[0] + 1, point[1]) # the point next to it
            new_p = []
            new_p.append(0.0)
            new_p.append(float(point[1]))
            new_p3 = [tuple(point), new_point]
            new_p.append(new_p3)
            h_par.append(new_p) # [[0.0, 7.0, [(7, 7), (8, 7)]], [0.0, 8.0, [(8, 8), (9, 8)]], [0.0, 9.0, [(9, 9), (10, 9)]]] for ex_3
    return h_par # len(h_par) = 3 for ex_3, list of the extra lines

def find_lines(f_comb, h_par): # total possible lines
    si = [] # slope_intersept_list
    for line in f_comb:
        if line[2] not in si:
            si.append(line[2]) # len(si) = 111
    lines = [x[:] for x in si] # create a lines list by copying the si without reference
    for line1 in range(len(si)):
        for line2 in f_comb:
            if (line2[2] == si[line1]):
                if line2[0] not in lines[line1]:
                    lines[line1].append(line2[0])
                if line2[1] not in lines[line1]:
                    lines[line1].append(line2[1]) # add the two connected points to the line
    for i in lines:
        l = list(i[2:])
        for j in i[2:]:
            i.remove(j)
        i.append(l) # put the points of each line on a list
    for line in h_par:
        lines.append(line) # also include the horizontal lines with one point
    return lines # [[1.0, 0.0, [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]], ..., ['nd', 11, [(11, 4), (11, 5), (11, 6)]]]

def find_par_lines(f_lines): # list of total vertical and horizontal lines
    p_lines = []
    for line in f_lines:
        if (line[0] == 0.0) | (line[0] == "nd"):
            p_lines.append(line)
    return p_lines

def sol_combs(lines): # total possible subsets for the first solution
    c = [] # combinations list
    for i in range(len(lines)):
        c.append(find_combinations(lines, i))
    c.remove(c[0]) # remove the first line because it's empty
    return c

# The combinations are the subsets of the solution and they are in order so that 
# the behavior is incremental
# So we only have to search till the first solution we find and is also the best, 
# as the next feasible solution will contain more lines 
# because of the incremental behavior of the combinations, and we don't want it

def sol_f(universe, subsets): # finds the solution (if -f argument is given)
    for sub in subsets:
        for sub1 in sub:
            total_points_set = set()
            total_points_list = []
            best_sol = []
            sol = []
            for line in sub1:
                total_points = line[2]
                for line2 in total_points:
                    if line2 in universe: # we only want the points of the universe (not the extra ones)
                        total_points_list.append(line2)
            total_points_set = set(total_points_list) # total distinct points of all the lines in the solution
            for line in sub1:
                sol.append(line[2]) # add the lines on the solution
            if len(total_points_set) == len(universe): # check if the number of points creates the universe
                for i in sol:
                    best_sol.append(i)
                return best_sol

def greedy(universe, subsets): # greedy solution (if -f argument is not given)
    covered = [] # points covered
    points_subsets = []
    sol = [] # solution with the lines
    covered_set = set()
    for line in range(len(subsets)): # we keep only the points of each line
        l1 = []
        l1.append(subsets[line][2])
        points_subsets.append(l1)
    for line in points_subsets: # we duplicate the previous list so we modify the first and keep the second static
        l = []
        for j in line[0]:
            l.append(j)
        line.append(l)
    while len(covered_set) != len(universe): # while we haven't found all the points of the universe
        points_subsets = sorted(points_subsets, key = lambda x: len(x[0])) # sort the subsets by their length
        last = points_subsets.pop()
        sol.append(last[1]) # add the subset with the most points at the time to the solution
        for i in last[0]:
            covered.append(i)
            for j in range(len(points_subsets)):
                if i in points_subsets[j][0]:
                    points_subsets[j][0].remove(i) # remove the points covered from the other subsets
        for point in covered:
            if point not in universe: # if it is the extra points we used for the parallel lines
                covered.remove(point) # remove it so it wont be counted as a point of the universe
        covered_set = set(covered)
    return sol # the total solution for the greedy

def sort_sol(sol): # takes a solution and sorts it the right way
    sol = sorted(sol, key = lambda x: x[0][1]) # sort based on y
    sol = sorted(sol, key = lambda x: x[0][0]) # sort based on x
    sol = sorted(sol, key = len, reverse = True) # sort based on length
    sol1 = []
    for each in sol:
        each = sorted(each, key = lambda x: x[0]) # sort each row based on x
        sol1.append(each)
    return sol1

def result(sol): # here we print the final result and call it in the main
    for i in range(len(sol)) : 
        for j in range(len(sol[i])) : 
            print(sol[i][j], end=" ")
        print()

def get_cmd(f_lines, g_lines, points_list): # here we handle the optional arguments for the right result
    if args.first_solution:
        if args.grid_lines_solution:
            s_combs = sol_combs(g_lines)
            best_sol = sol_f(points_list, s_combs)
            return best_sol # -f, -g
        else:
            s_combs = sol_combs(f_lines)
            best_sol = sol_f(points_list, s_combs)
            return best_sol # -f
    elif args.grid_lines_solution:
        greedy_sol = greedy(points_list, g_lines)
        return greedy_sol # -g
    else:
        greedy_sol = greedy(points_list, f_lines)
        return greedy_sol # no optional arguments

def main(): # here we call all the methods at the end to get the result
    file = args.txt_file
    points_list = file_open(file)
    comb = find_combinations(points_list, 2)
    f_comb = find_comb_slope_intercept(comb)
    h_par = find_lone_h_lines(points_list)
    f_lines = find_lines(f_comb, h_par)
    g_lines = find_par_lines(f_lines)
    call_prog = get_cmd(f_lines, g_lines, points_list)
    final_sol = sort_sol(call_prog)
    res = result(final_sol)
    return res
main()

#! FINISHED
