import numpy as np
import time
# translate function: converts a state in string form to a two-dimensional matrix form
def transtate(state):
    np_state = np.zeros((5,4))
    assert len(state) == 20, 'error'
    state_dict = dict()
    state_dict['a'] = 210
    state_dict['f'] = 211
    state_dict['b'] = 12
    state_dict['c'] = 11
    state_dict['d'] = 22
    state_dict['e'] = 0
    for k in range(20):
        i = int(k / 4)
        j = int(k % 4)
        np_state[i][j] = state_dict[state[k]]
    return np_state
    
# Convert a two-dimensional matrix form of state to a string form
def statetrans(np_state):
    state = ""
    dict_state = dict()
    dict_state[210] = 'a'
    dict_state[211] = 'f'
    dict_state[12] = 'b'
    dict_state[11] = 'c'
    dict_state[22] = 'd'
    dict_state[0] = 'e'
    for i in range(5):
        for j in range(4):
            state = state + dict_state[np_state[i][j]]
    return state 

# Judgement positions are also not out of bounds, e.g. rows over 5 or columns less than 0
def bound(row, column):
    if row<5 and row>=0 and column < 4 and column >=0:
        return True
    else:
        return False

# A* algorithm is a heuristic to find a solution, and what it finds is not necessarily the optimal solution.
# The cost of each node in the A* algorithm is divided into two parts, one for f and one for h. f is the cost of getting from the initial state to the current state
# This is exact, and can be calculated using the number of iterations, while g is the cost from the current state to the end point, which we can only estimate, but not get an exact value for g.
# The core of the implementation of the A* algorithm is the selection of g and the analysis of state changes



# In each iteration, the current state generates many states, as each state requires the use of spaces. Let's take the theme of spaces and change the states
# Three cases, one where two spaces are not adjacent, then they can be swapped with 1*1's, or 2*1's can be made to move up and down one frame, or 1*2's can be made to move left and right one frame
# One is where two spaces are adjacent to each other as 2*1 spaces, then they can either swap with 2*1's or move 2*2's
# One is where two spaces are next to each other as 1*2 spaces, then they can either swap with 1*2's or move 2*2's
# The latter two cases also include the first, i.e. the state extended by case 1 also needs to be added to case 2 or 3.



# Situation 1
def state0(row, column, np_state):
    ex_states = []
    rcs = []
    rcs.append((row-1, column))
    rcs.append((row+1, column))
    rcs.append((row, column-1))
    rcs.append((row, column+1))
    for i in range(4):
        n_row, n_column = rcs[i]
        if bound(n_row, n_column) and np_state[n_row][n_column] == 11:
            np_state2 = np_state.copy()
            np_state2[row][column] = 11
            np_state2[n_row][n_column] = 0
            ex_states.append(np_state2)
            #ppp(np_state2, np_state)
    if bound(row-2,column) and np_state[row-1][column] == 211 and np_state[row-2][column] == 210:
        np_state2 = np_state.copy()
        np_state2[row-2][column] = 0
        np_state2[row-1][column] = 210
        np_state2[row][column] = 211
        ex_states.append(np_state2)
    if bound(row+2,column) and np_state[row+1][column] == 210 and np_state[row+2][column] == 211:
        np_state2 = np_state.copy()
        np_state2[row][column] = 210
        np_state2[row+1][column] = 211
        np_state2[row+2][column] = 0
        ex_states.append(np_state2)
    if bound(row,column-2) and np_state[row][column-1] == 12 and np_state[row][column-2] == 12:
        np_state2 = np_state.copy()
        np_state2[row][column-2] = 0
        np_state2[row][column] = 12
        ex_states.append(np_state2)
    if bound(row,column+2) and np_state[row][column+1] == 12 and np_state[row][column+2] == 12:
        np_state2 = np_state.copy()
        np_state2[row][column+2] = 0
        np_state2[row][column] = 12
        ex_states.append(np_state2)
    return ex_states

def ppp(np_state2, np_state):
    index0, index1 = np.where(np_state2==0)
    if len(index0) != 2:
        print('Error')
        print(np_state)
        print(np_state2)

# Case 3, subsequent state of the state (subsequent step)
def state12(row, column, np_state):
    #left
    ex_states = []
    rcs = []
    rcs.append((-1, 0))
    rcs.append((1, 0))
    for i in range(2):
        n_row, n_column = row + rcs[i][0], column
        if bound(n_row, n_column):
            if np_state[n_row][n_column] == 12 and np_state[n_row][n_column+1] == 12:
                np_state2 = np_state.copy()
                np_state2[row][column] = 12
                np_state2[row][column+1] = 12
                np_state2[n_row][n_column] = 0
                np_state2[n_row][n_column+1] = 0
                ex_states.append(np_state2)
                #print(np_state2)
                ppp(np_state2, np_state)
            elif np_state[n_row][n_column] == 22 and np_state[n_row][n_column+1] == 22:
                np_state2 = np_state.copy()
                np_state2[row][column] = 22
                np_state2[row][column+1] = 22
                np_state2[row + 2 * rcs[i][0]][column] = 0
                np_state2[row + 2 * rcs[i][0]][column+1] = 0
                ex_states.append(np_state2)
                #print(np_state2)
                ppp(np_state2, np_state)
    if bound(row, column+3) and np_state[row][column+2] == 12 and np_state[row][column+3] == 12:
        np_state2 = np_state.copy()
        np_state2[row][column] = 12
        np_state2[row][column+1] = 12
        np_state2[row][column+2] = 0
        np_state2[row][column+3] = 0
        ex_states.append(np_state2)
        #ppp(np_state2, np_state)
    elif bound(row, column-2) and np_state[row][column-1] == 12 and np_state[row][column-2] == 12:
        np_state2 = np_state.copy()
        np_state2[row][column] = 12
        np_state2[row][column+1] = 12
        np_state2[row][column-1] = 0
        np_state2[row][column-2] = 0
        ex_states.append(np_state2)
        #ppp(np_state2, np_state)
    
    return ex_states

# Case II, subsequent state of the state (subsequent step)
def state21(row, column, np_state):
    # up
    ex_states = []
    rcs = []
    rcs.append((0, -1))
    rcs.append((0, 1))
    for i in range(2):
        n_row, n_column = row, column + rcs[i][1]
        #print(n_row, n_column)
        if bound(n_row, n_column):
            if np_state[row][n_column] == 210 and np_state[row+1][n_column] == 211:
                np_state2 = np_state.copy()
                np_state2[row][column] = 210
                np_state2[row+1][column] = 211
                np_state2[row][n_column] = 0
                np_state2[row+1][n_column] = 0
                ex_states.append(np_state2)
                #print(np_state2)
                #ppp(np_state2, np_state)
            elif np_state[row][n_column] == 22 and np_state[row+1][n_column] == 22:
                np_state2 = np_state.copy()
                np_state2[row][column] = 22
                np_state2[row+1][column] = 22
                np_state2[row][column + 2 * rcs[i][1]] = 0
                np_state2[row+1][column + 2 * rcs[i][1]] = 0
                ex_states.append(np_state2)
                #print(np_state2)
                #ppp(np_state2, np_state)
    if bound(row+3, column) and np_state[row+2][column] == 210 and np_state[row+3][column] == 211:
        np_state2 = np_state.copy()
        np_state2[row][column] = 210
        np_state2[row+1][column] = 211
        np_state2[row+2][column] = 0
        np_state2[row+3][column] = 0
        ex_states.append(np_state2)
        #ppp(np_state2, np_state)
    elif bound(row-2, column) and np_state[row-1][column] == 211 and np_state[row-2][column] == 210:
        np_state2 = np_state.copy()
        np_state2[row-2][column] = 0
        np_state2[row-1][column] = 0
        np_state2[row][column] = 210
        np_state2[row+1][column] = 211
        ex_states.append(np_state2)
        #ppp(np_state2, np_state)
    return ex_states

# For an input state, analyse all his subsequent states (subsequent step)
def state_ex(np_state):
    ex_states = []
    index0, index1 = np.where(np_state==0)
    assert len(index0) == 2, 'Error'
    if index0[0] == index0[1] and abs(index1[0]-index1[1])==1:
        #print(index0[0], min(index1[0], index1[1]))
        exs = state12(index0[0], min(index1[0], index1[1]), np_state.copy())
        ex_states = ex_states + exs
        #print(len(state12(index0[0], min(index1[0], index1[1]), np_state.copy())))
    elif index1[0] == index1[1] and abs(index0[0]-index0[1])==1:
        #print('2*1')
        #print(min(index0[0], index0[1]), index1[0])
        exs = state21(min(index0[0], index0[1]), index1[0], np_state.copy())
        #print(np_state)
        #for ex in exs:
            #print(ex)
        ex_states = ex_states + exs
        #print(len(state21(min(index0[0], index0[1]), index1[0], np_state.copy())))
    else:
        pass
    #print('1*1')    
    ex_states = ex_states + state0(index0[0], index1[0], np_state.copy())
    ex_states = ex_states + state0(index0[1], index1[1], np_state.copy())
    return ex_states
    
# g function is designed so that we directly weight the current distance between Cao Cao and the exit as g. We think it's harder to make Cao Cao move up and down, so the distance up and down is weighted higher
def heu(np_state):
    index0, index1  = np.where(np_state==22)
    return (10*abs(np.max(index0) - 4) + abs(np.min(index1)-1))

# Check the current status for the number of pawns, generals, Cao Cao and spaces
def check(np_state, father_dict):
    #print(np_state)
    #str_state = statetrans(np_state)
    #print(father_dict[str_state])
    assert len(np.where(np_state==22)[0]) == 4
    assert len(np.where(np_state==0)[0])  == 2
    assert len(np.where(np_state==12)[0]) == 2
    assert len(np.where(np_state==211)[0]) == 4
    assert len(np.where(np_state==210)[0]) == 4
    assert len(np.where(np_state==11)[0]) == 4

# Main functions
def main(init_state):
    t0 = time.time()
    open_dict = {}  # Storage candidate status
    f_value_dict = {}  # Store the f-value of each state
    close_dict = {} # Store the traversed state
    np_init_state = transtate(init_state) # trans for the initial state
    open_dict[init_state] = 0 + heu(np_init_state) 
    f_value_dict[init_state] = 0
    flag = True
    counts = 0
    #time_cost = time.time()
    while(flag):  # Iterate through open_dict until a solution is found, picking the least costly state each time
    # For each traversed state, analyse whether it is a solution; find its subsequent state and add it to open_dict.
    #(add states to determine if they have been analysed, if they have been analysed, they are not added);
    # Throw the traversed state into close_dict
        if len(open_dict.keys()) == 0:
            print('failed')
            flag = False
            break 
        #Sort
        sort_states = sorted(open_dict.items(),key = lambda x:x[1],reverse = False)
        state = sort_states[0][0]
        #state = list(open_dict.keys())[0]
        
        np_state = transtate(state)
        check(np_state, father_dict)
        counts = counts + 1
        if heu(np_state) == 0:
            flag = False
            break
        else:
            ex_states = state_ex(np_state)
            for nstate in ex_states:
                str_state = statetrans(nstate)
                father_dict[str_state] = np_state
                if str_state in open_dict.keys():
                    f_value_dict[str_state] = min(f_value_dict[state] + 1, f_value_dict[str_state])
                    open_dict[str_state] = f_value_dict[str_state] + heu(nstate)
                if str_state in close_dict.keys():
                    continue
                if str_state not in open_dict.keys() and str_state not in close_dict.keys():
                    #print(nstate)
                    f_value_dict[str_state] = f_value_dict[state] + 1
                    open_dict[str_state] = f_value_dict[str_state] + heu(nstate)
            close_dict[state] = open_dict[state] 
            open_dict.pop(state)
    str_state = statetrans(np_state)
    t1 = time.time()
    print('Introductions:')
    print('12 means 1*2 obstacle;')
    print('210 means 2*1 obstacle(up);')
    print('211 means 2*1 obstacle(down);')
    print('22 means Caocao;')
    print('11 means 1*1 obstacle;')
    print('0 means blank.')
    print('Number of steps:', f_value_dict[str_state])
    print('Number of states:', counts)
    print('Time cost:', t1-t0, end='')
    print('s')
    print('Last state:')
    print(np_state)

father_dict = {}
init_state = 'addafddfabbafccfceec'
father_dict[init_state] = init_state
main(init_state)

