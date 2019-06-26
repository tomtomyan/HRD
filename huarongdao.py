import numpy as np
import copy
import queue as Q
import sys

class State():
    def __init__(self, l, p, cost=0, f=0):
        self.l = l
        self.p = p
        self.cost = cost
        self.f = f
    def __lt__(self, other):
        return self.f < other.f


def print_state(state):
    for line in state:
        print(*line, sep="")
    
def read_puzzle(id):
    with open(id) as file:
        puzzle = [[int(num) for num in line.rstrip()] for line in file]
        for y in range(len(puzzle)):
            for x in range(len(puzzle[y])):
                if puzzle[y][x] >= 2 and puzzle[y][x] <= 6:
                    if y+1 <= 4 and puzzle[y][x] == puzzle[y+1][x]:
                        puzzle[y][x] = 10
                        puzzle[y+1][x] = 10
                    elif x+1 <= 3 and puzzle[y][x] == puzzle[y][x+1]:
                        puzzle[y][x] = 11
                        puzzle[y][x+1] = 11
                elif puzzle[y][x] == 7:
                    puzzle[y][x] = 4
        for y in range(len(puzzle)):
            for x in range(len(puzzle[y])):
                if puzzle[y][x] == 10:
                    puzzle[y][x] = 3
                elif puzzle[y][x] == 11:
                    puzzle[y][x] = 2
        return puzzle

def is_goal(state):
    return state[3][1]==1 and state[3][2]==1 and state[4][1]==1 and state[4][2]==1

def swap1(state, x1, y1, x2, y2):
    #print("swap1 called on " + str(x1) + str(y1) + str(x2) + str(y2))
    s = np.copy(state)
    s[y1][x1] = s[y2][x2]
    s[y2][x2] = 0
    return s

def swap_horizontal(state, x, y1, y2):
    #print("swap_horizontal called on " + str(x) + str(y1) + str(x) + str(y2))
    s = np.copy(state)
    s[y1][x] = s[y2][x]
    s[y1][x+1] = s[y2][x+1]
    s[y2][x] = 0
    s[y2][x+1] = 0
    return s

def swap_vertical(state, x1, x2, y):
    #print("swap_vertical called on " + str(x1) + str(y) + str(x2) + str(y))
    s = np.copy(state)
    s[y][x1] = s[y][x2]
    s[y+1][x1] = s[y+1][x2]
    s[y][x2] = 0
    s[y+1][x2] = 0
    return s

def get_successors(state):
    successors = []
    zeros = []
    for y, line in enumerate(state):
        for x, num in enumerate(line):
            if num == 0:
                zeros.append((x, y))

    #print(zeros)
    
    # get coordinates of zeros
    x = zeros[0][0]
    y = zeros[0][1]
    x2 = zeros[1][0]
    y2 = zeros[1][1]

    # check adjacent
    if (x2 - x) + (y2 - y) == 1:

        # horizontal adjacent
        if x2 - x == 1:
            if y-1 >= 0 and state[y-1][x] == 1 and state[y-1][x+1] == 1:
                successors.append(swap_horizontal(state, x, y, y-2))
            elif y-1 >= 0 and state[y-1][x] == 2 and state[y-1][x+1] == 2:
                if not (x-1 >= 0 and x+2 <= 3 and state[y-1][x-1] == 2 and state[y-1][x+2] == 2):
                    successors.append(swap_horizontal(state, x, y, y-1))

            if y+1 <= 4 and state[y+1][x] == 1 and state[y+1][x+1] == 1:
                successors.append(swap_horizontal(state, x, y, y+2))
            elif y+1 <= 4 and state[y+1][x] == 2 and state[y+1][x+1] == 2:
                if not (x-1 >= 0 and x+2 <= 3 and state[y+1][x-1] == 2 and state[y+1][x+2] == 2):
                    successors.append(swap_horizontal(state, x, y, y+1))

        # vertical adjacent
        elif y2 - y == 1:
            if x-1 >= 0 and state[y][x-1] == 1 and state[y+1][x-1] == 1:
                successors.append(swap_vertical(state, x, x-2, y))
            elif x-1 >= 0 and state[y][x-1] == 3 and state[y+1][x-1] == 3:
                # extra error checking
                if not (y-1 >= 0 and y+2 <= 4 and state[y-1][x-1] == 3 and state[y+2][x-1] == 3):
                    successors.append(swap_vertical(state, x, x-1, y))

            if x+1 <= 3 and state[y][x+1] == 1 and state[y+1][x+1] == 1:
                successors.append(swap_vertical(state, x, x+2, y))
            elif x+1 <= 3 and state[y][x+1] == 3 and state[y+1][x+1] == 3:
                if not (y-1 >= 0 and y+2 <= 4 and state[y-1][x+1] == 3 and state[y+2][x+1] == 3):
                    successors.append(swap_vertical(state, x, x+1, y))

    # check individual zero
    for x, y in zeros:
        above = state[y-1][x] if y-1 >= 0 else -1
        below = state[y+1][x] if y+1 <=4 else -1
        left = state[y][x-1] if x-1 >= 0 else -1
        right = state[y][x+1] if x+1 <= 3 else -1

        if above == 4:
            successors.append(swap1(state, x, y, x, y-1))
        elif above == 3:
            successors.append(swap1(state, x, y, x, y-2))

        if below == 4:
            successors.append(swap1(state, x, y, x, y+1))
        elif below == 3:
            successors.append(swap1(state, x, y, x, y+2))

        if left == 4:
            successors.append(swap1(state, x, y, x-1, y))
        elif left == 2:
            successors.append(swap1(state, x, y, x-2, y))
            
        if right == 4:
            successors.append(swap1(state, x, y, x+1, y))
        elif right == 2:
            successors.append(swap1(state, x, y, x+2, y))

    return successors

def get_cost(state):
    return state.cost

def get_heuristic(state):
    for y, line in enumerate(state.l):
        for x, num in enumerate(line):
            if num == 1:
                return abs(3-y) + abs(1-x)

def a_star(initial_state):
    global num_expanded
    global num_generated
    s = State(initial_state, None)
    s.f = s.cost + get_heuristic(s)
    frontier = Q.PriorityQueue()
    frontier.put(s)
    
    while frontier:
        cur_state = frontier.get()

        if str(cur_state.l) not in visited:
            visited[str(cur_state.l)] = 1
        else:
            continue

        if is_goal(cur_state.l):
            return cur_state

        num_expanded += 1
        for s in get_successors(cur_state.l):
            if str(s) not in frontier_states:
                new_state = State(s, cur_state, cur_state.cost+1)
                new_state.f = new_state.cost + get_heuristic(new_state)
                frontier.put(new_state)
                frontier_states[str(s)] = 1
                num_generated += 1

def bfs(initial_state):
    global num_expanded
    global num_generated
    s = State(initial_state, None)
    frontier = [s]
    
    while frontier:
        cur_state = frontier.pop(0)

        if str(cur_state.l) not in visited:
            visited[str(cur_state.l)] = 1
        else:
            continue

        if is_goal(cur_state.l):
            return cur_state

        num_expanded += 1
        for s in get_successors(cur_state.l):
            if str(s) not in frontier_states:
                frontier.append(State(s, cur_state))
                frontier_states[str(s)] = 1
                num_generated += 1

def dfs(initial_state):
    global num_expanded
    global num_generated
    s = State(initial_state, None)
    frontier = [s]
    
    while frontier:
        cur_state = frontier.pop()

        if str(cur_state.l) not in visited:
            visited[str(cur_state.l)] = 1
        else:
            continue

        if is_goal(cur_state.l):
            return cur_state

        num_expanded += 1
        for s in get_successors(cur_state.l):
            if str(s) not in frontier_states:
                frontier.append(State(s, cur_state))
                frontier_states[str(s)] = 1
                num_generated += 1

visited = {}
frontier_states = {}
num_expanded = 0
num_generated = 1
initial_state = read_puzzle(sys.argv[2])
solver = sys.argv[1]
if solver == "astar":
    state = a_star(initial_state)
elif solver == "bfs":
    state = bfs(initial_state)
elif solver == "dfs":
    state = dfs(initial_state)
else:
    print("Invalid algorithm to solve puzzle")
    sys.exit()

state_list = []
p = state
while p:
    state_list.insert(0, p.l)
    p = p.p

print("Initial state:")
print_state(initial_state)
print()
print("Cost of the (optimal) solution: " + str(len(state_list)-1))
print()
print("Number of states expanded: " + str(num_expanded))
print("Number of states generated: " + str(num_generated))
print()
print("(Optimal) solution:")

for i, s in enumerate(state_list):
    print()
    print(i)
    print_state(s)
