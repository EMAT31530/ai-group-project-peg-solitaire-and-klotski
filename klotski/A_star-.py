import copy
import pprint
import tkinter as tk
import threading
import time

def operation_1(liste, state):
    places_of_1 = []
    big_one = []
    for i in range(len(liste)):
        for b in range(len(liste[i])):
            if liste[i][b] == 1:
                places_of_1.append((i, b))
    if state == "right":
        a = copy.deepcopy(liste)
        for i in places_of_1:
            try:
                if liste[i[0]][i[1] + 1] == 0:
                    liste[i[0]][i[1] + 1] = 1
                    liste[i[0]][i[1]] = 0
                    big_one.append(copy.deepcopy(liste))
                    liste = a
            except:
                pass
    if state == "left":
        a = copy.deepcopy(liste)
        for i in places_of_1:
            try:
                if i[1] - 1 >= 0:
                    if liste[i[0]][i[1] - 1] == 0:
                        liste[i[0]][i[1] - 1] = 1
                        liste[i[0]][i[1]] = 0
                        big_one.append(copy.deepcopy(liste))
                        liste = a
            except:
                pass
        a = copy.deepcopy(liste)
        for i in places_of_1:
            try:

                if liste[i[0] + 1][i[1]] == 0:
                    liste[i[0] + 1][i[1]] = 1
                    liste[i[0]][i[1]] = 0
                    big_one.append(copy.deepcopy(liste))
                    liste = a
            except:
                pass
    if state == "up":
        a = copy.deepcopy(liste)
        for i in places_of_1:
            try:
                if i[0] - 1 >= 0:
                    if liste[i[0] - 1][i[1]] == 0:
                        liste[i[0] - 1][i[1]] = 1
                        liste[i[0]][i[1]] = 0
                        big_one.append(copy.deepcopy(liste))
                        liste = a
            except:
                pass
    return big_one

def operation_2(liste, state):
    p_for_2 = []
    for i in range(len(liste)):
        for b in range(len(liste[i])):
            if liste[i][b] == 2:
                p_for_2.append((i, b))
    if state == "left":
        try:
            if p_for_2[0][1] - 1 >= 0 and p_for_2[1][1] - 1 >= 0 and p_for_2[1][0] - 1 >= 0:
                if liste[p_for_2[0][0]][p_for_2[0][1] - 1] == 0 and liste[p_for_2[1][0]][p_for_2[1][1] - 1] == 0 \
                        and liste[p_for_2[0][0] + 1][p_for_2[0][1]] == 2 and liste[p_for_2[1][0] - 1][
                    p_for_2[1][1]] == 2:
                    liste[p_for_2[0][0]][p_for_2[0][1] - 1], liste[p_for_2[1][0]][p_for_2[1][1] - 1] = 2, 2
                    liste[p_for_2[0][0]][p_for_2[0][1]], liste[p_for_2[1][0]][p_for_2[1][1]] = 0, 0
                    return (liste)
        except:
            pass
    if state == "right":
        try:
            if p_for_2[1][0] - 1 >= 0:
                if liste[p_for_2[0][0]][p_for_2[0][1] + 1] == 0 and liste[p_for_2[1][0]][p_for_2[1][1] + 1] == 0 and \
                        liste[p_for_2[0][0] + 1][p_for_2[0][1]] == 2 and liste[p_for_2[1][0] - 1][p_for_2[1][1]] == 2:
                    liste[p_for_2[0][0]][p_for_2[0][1] + 1], liste[p_for_2[1][0]][p_for_2[1][1] + 1] = 2, 2
                    liste[p_for_2[0][0]][p_for_2[0][1]], liste[p_for_2[1][0]][p_for_2[1][1]] = 0, 0
                    return (liste)
        except:
            pass
        
    if state == "up":
        try:
            if p_for_2[1][0] - 1 >= 0 and p_for_2[0][0] - 1 >= 0:
                if liste[p_for_2[0][0] - 1][p_for_2[0][1]] == 0 and \
                        liste[p_for_2[0][0] + 1][p_for_2[0][1]] == 2 and liste[p_for_2[1][0] + 1][p_for_2[1][1]] == 2:
                    liste[p_for_2[0][0] - 1][p_for_2[0][1]] = 2
                    liste[p_for_2[1][0]][p_for_2[1][1]] = 0
                    return (liste)
        except:
            pass
    if state == "down":
        try:
            if p_for_2[1][0] - 1 >= 0:
                if liste[p_for_2[1][0] + 1][p_for_2[1][1]] == 0 and \
                        liste[p_for_2[0][0] + 1][p_for_2[0][1]] == 2 and liste[p_for_2[1][0] - 1][p_for_2[1][1]] == 2:
                    liste[p_for_2[1][0] + 1][p_for_2[1][1]] = 2
                    liste[p_for_2[0][0]][p_for_2[0][1]] = 0
                    return (liste)
        except:
            pass
        
def operation_3(liste, state):
    p_for_3 = []
    for i in range(len(liste)):
        for b in range(len(liste[i])):
            if liste[i][b] == 3:
                p_for_3.append((i, b))
    if state == "left":
        try:
            if p_for_3[0][1] - 1 >= 0 and p_for_3[1][1] - 1 >= 0:
                if liste[p_for_3[0][0]][p_for_3[0][1] - 1] == 0 and \
                        liste[p_for_3[0][0]][p_for_3[0][1] + 1] == 3 and liste[p_for_3[1][0]][p_for_3[1][1] - 1] == 3:
                    liste[p_for_3[0][0]][p_for_3[0][1] - 1] = 3
                    liste[p_for_3[0][0]][p_for_3[0][1] + 1] = 0
                    return (liste)
        except:
            pass
    if state == "right":
        try:
            if p_for_3[1][1] - 1 >= 0:
                if liste[p_for_3[1][0]][p_for_3[1][1] + 1] == 0 and liste[p_for_3[0][0]][p_for_3[0][1] + 1] == 3 and \
                        liste[p_for_3[1][0]][p_for_3[1][1] - 1] == 3:
                    liste[p_for_3[1][0]][p_for_3[1][1] - 1] = 0
                    liste[p_for_3[1][0]][p_for_3[1][1] + 1] = 3
                    return (liste)
        except:
            pass
    if state == "down":
        try:
            if p_for_3[1][1] - 1 >= 0:
                if liste[p_for_3[0][0] + 1][p_for_3[0][1]] == 0 and liste[p_for_3[1][0] + 1][p_for_3[1][1]] == 0 and \
                        liste[p_for_3[0][0]][p_for_3[0][1] + 1] == 3 and liste[p_for_3[1][0]][p_for_3[1][1] - 1] == 3:
                    liste[p_for_3[1][0] + 1][p_for_3[1][1]] = 3
                    liste[p_for_3[1][0] + 1][p_for_3[1][1] - 1] = 3
                    liste[p_for_3[1][0]][p_for_3[1][1]] = 0
                    liste[p_for_3[1][0]][p_for_3[1][1] - 1] = 0
                    return (liste)
        except:
            pass
    if state == "up":
        try:
            if p_for_3[1][1] - 1 >= 0 and p_for_3[1][0] - 1 >= 0:
                if liste[p_for_3[0][0] - 1][p_for_3[0][1]] == 0 and liste[p_for_3[1][0] - 1][p_for_3[1][1]] == 0 and \
                        liste[p_for_3[0][0]][p_for_3[0][1] + 1] == 3 and liste[p_for_3[1][0]][p_for_3[1][1] - 1] == 3:
                    liste[p_for_3[1][0] - 1][p_for_3[1][1]] = 3
                    liste[p_for_3[1][0] - 1][p_for_3[1][1] - 1] = 3
                    liste[p_for_3[1][0]][p_for_3[1][1]] = 0
                    liste[p_for_3[1][0]][p_for_3[1][1] - 1] = 0
                    return (liste)
        except:
            pass

def operation_4(liste, state):
    place_of_4 = []
    place_of_second_4 = []
    for i in range(len(liste)):
        if 4 in liste[i]:
            place_of_4.append(i)
            place_of_4.append(liste[i].index(4))
            place_of_second_4.append(i + 1)
            place_of_second_4.append(liste[i].index(4) + 1)
            break

    if state == "left":
        try:
            if place_of_4[1] - 1 >= 0:
                if liste[place_of_4[0]][place_of_4[1] - 1] == 0 and liste[place_of_4[0] + 1][place_of_4[1] - 1] == 0 and \
                        liste[place_of_4[0]][place_of_4[1] + 1] == 4 and liste[place_of_4[0] + 1][
                    place_of_4[1]] == 4 and liste[place_of_4[0] + 1][place_of_4[1] + 1] == 4:
                    liste[place_of_4[0]][place_of_4[1] - 1], liste[place_of_4[0] + 1][place_of_4[1] - 1] = 4, 4
                    liste[place_of_4[0]][place_of_4[1] + 1], liste[place_of_4[0] + 1][place_of_4[1] + 1] = 0, 0
                    return (liste)
        except:
            pass
        
    if state == "up":
        try:  
            if place_of_4[0] - 1 >= 0:
                if liste[place_of_4[0] - 1][place_of_4[1]] == 0 and liste[place_of_4[0] - 1][place_of_4[1] + 1] == 0 and \
                        liste[place_of_4[0]][place_of_4[1] + 1] == 4 and liste[place_of_4[0] + 1][
                    place_of_4[1]] == 4 and \
                        liste[place_of_4[0] + 1][place_of_4[1] + 1] == 4:
                    liste[place_of_4[0] - 1][place_of_4[1]], liste[place_of_4[0] - 1][place_of_4[1] + 1] = 4, 4
                    liste[place_of_4[0] + 1][place_of_4[1]], liste[place_of_4[0] + 1][place_of_4[1] + 1] = 0, 0
                    return (liste)
        except:
            pass
        
    if state == "down":
        try:
            if place_of_second_4[0] - 1 >= 0 and place_of_second_4[1] - 1 >= 0:
                if liste[place_of_second_4[0] + 1][place_of_second_4[1] - 1] == 0 and liste[place_of_second_4[0] + 1][
                    place_of_second_4[1]] == 0 and \
                        liste[place_of_second_4[0]][place_of_second_4[1] - 1] == 4 and liste[place_of_second_4[0] - 1][
                    place_of_second_4[1]] == 4 and \
                        liste[place_of_second_4[0] - 1][place_of_second_4[1] - 1] == 4:
                    liste[place_of_second_4[0] + 1][place_of_second_4[1] - 1], liste[place_of_second_4[0] + 1][
                        place_of_second_4[1]] = 4, 4
                    liste[place_of_second_4[0] - 1][place_of_second_4[1] - 1], liste[place_of_second_4[0] - 1][
                        place_of_second_4[1]] = 0, 0
                    return (liste)
        except:
            pass
    if state == "right":
        try:  
            if place_of_second_4[1] - 1 >= 0 and place_of_second_4[0] - 1 >= 0:
                if liste[place_of_second_4[0] - 1][place_of_second_4[1] + 1] == 0 and liste[place_of_second_4[0]][
                    place_of_second_4[1] + 1] == 0 and \
                        liste[place_of_second_4[0]][place_of_second_4[1] - 1] == 4 and liste[place_of_second_4[0] - 1][
                    place_of_second_4[1]] == 4 and \
                        liste[place_of_second_4[0] - 1][place_of_second_4[1] - 1] == 4:
                    liste[place_of_second_4[0] - 1][place_of_second_4[1] + 1], liste[place_of_second_4[0]][
                        place_of_second_4[1] + 1] = 4, 4
                    liste[place_of_second_4[0]][place_of_second_4[1] - 1], liste[place_of_second_4[0] - 1][
                        place_of_second_4[1] - 1] = 0, 0
                    return (liste)
        except:
            pass
 
class movements():
    def __init__(self, cost, parent, expanded, initial_state, queue, goal_state, my_list, state, cost_to_main_parent):
        self.cost = cost
        self.parent = parent
        self.expanded = expanded
        self.initial_state = initial_state
        self.queue = queue
        self.goal_state = goal_state
        self.my_list = my_list
        self.state = state
        self.cost_to_main_parent = cost_to_main_parent
    def right(self, list):
        self.expanded.append(operation_4(copy.deepcopy(list), "right"))
        self.expanded.append(operation_3(copy.deepcopy(list), "right"))
        self.expanded.append(operation_2(copy.deepcopy(list), "right"))
        self.expanded.append(operation_1(copy.deepcopy(list), "right"))
    def down(self, list):
        self.expanded.append(operation_4(copy.deepcopy(list), "down"))
        self.expanded.append(operation_3(copy.deepcopy(list), "down"))
        self.expanded.append(operation_2(copy.deepcopy(list), "down"))
        self.expanded.append(operation_1(copy.deepcopy(list), "down"))
    def up(self, list):
        self.expanded.append(operation_4(copy.deepcopy(list), "up"))
        self.expanded.append(operation_3(copy.deepcopy(list), "up"))
        self.expanded.append(operation_2(copy.deepcopy(list), "up"))
        self.expanded.append(operation_1(copy.deepcopy(list), "up"))
    def left(self, list):
        self.expanded.append(operation_4(copy.deepcopy(list), "left"))
        self.expanded.append(operation_3(copy.deepcopy(list), "left"))
        self.expanded.append(operation_2(copy.deepcopy(list), "left"))
        self.expanded.append(operation_1(copy.deepcopy(list), "left"))


    def A_star_search(self):
        first = movements(0, "", self.expanded, self.initial_state, self.queue, self.goal_state, self.my_list, self.state, 1)
        self.parent = first
        self.queue.append((first,first.cost))
        self.left(copy.deepcopy(self.initial_state))
        self.right(copy.deepcopy(self.initial_state))
        self.down(copy.deepcopy(self.initial_state))
        self.up(copy.deepcopy(self.initial_state))
        visited = [first.state]
        tmp = []
        while True:
            for k in self.expanded:
                position_of_left_down_4 = []
                if k != None:
                    if len(k) != 0:
                        if type(k[0][0]) == list:
                            for r in k:
                                for i in range(len(r)):
                                    if 4 in r[i]:
                                        position_of_left_down_4.append(i + 1)
                                        position_of_left_down_4.append(r[i].index(4))
                                cost = ((3 - position_of_left_down_4[0]) ** 2 + position_of_left_down_4[1] ** 2) ** 0.5
                                obj = movements(cost + self.parent.cost_to_main_parent, self.parent, self.expanded,
                                                 self.initial_state, self.queue, self.goal_state, self.my_list,
                                                 r, self.parent.cost_to_main_parent + 1.0)
                                tmp.append(obj)
                        else:
                            for i in range(len(k)):
                                if 4 in k[i]:
                                    position_of_left_down_4.append(i + 1)
                                    position_of_left_down_4.append(k[i].index(4))
                            cost = ((3 - position_of_left_down_4[0]) ** 2 + position_of_left_down_4[1] ** 2) ** 0.5
                            obj = movements(cost + self.parent.cost_to_main_parent, self.parent, self.expanded,
                                             self.initial_state, self.queue, self.goal_state, self.my_list,
                                             k, self.parent.cost_to_main_parent + 1.0)
                            tmp.append(obj)
            self.expanded = []
            def takeSecond(elem):
                return elem[1]
            for i in tmp:
                if i.state not in [i[0].state for i in self.queue]:
                    self.queue.append((i,i.cost))
                    self.queue.sort(key=takeSecond)
            tmp=[]
            for i in self.queue:
                if i[0].state[2][0]==4 and i[0].state[2][1]==4 and i[0].state[3][0]==4 and i[0].state[3][1]==4:
                    self.my_list=[i[0]]
                    for i in self.my_list:
                        if type(i.parent)!=str:
                            self.my_list.append(i.parent)
                    return False
                if i[0].state not in visited:
                    self.parent = i[0]
                    self.left(copy.deepcopy(i[0].state))
                    self.right(copy.deepcopy(i[0].state))
                    self.down(copy.deepcopy(i[0].state))
                    self.up(copy.deepcopy(i[0].state))
                    visited.append(i[0].state)
                    break


# list1 = [ [1, 2, 1, 1],
#        [1, 2, 4, 4],
#        [3, 3, 4, 4],
#        [1, 1, 0, 0] ]
list1 = [ [1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16] ]

#####A* SEARCH######
obj = movements(0, "", [], list1, [], [3, 0], [], list1, 0)
obj.A_star_search()



class BlockInterface(object):
    def __init__(self, master, G):
        master.title("Puzzle")
        canv_frame = tk.Frame(master)
        canv_frame.pack()
        self.canvas = tk.Canvas(canv_frame, width=10, height=60, bg="gray")
        self.canvas.pack(padx=10, pady=10)
        self.trace = G
        self.create_grid(G[0])
        self.activate(G[0])

    def create_rect(self, coord, val):
        if val == 0:
            fill = "white"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)
        elif val == 1:
            fill = "blue"
            self.canvas.create_rectangle(coord, fill=fill, outline="black")
        elif val == 2:
            fill = "green"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)
        elif val == 3:
            fill = "green"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)
        elif val == 4:
            fill = "red"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)

    def create_row(self, vector, y_coord):
        y0, y1 = y_coord
        w = 70
        x0, x1 = 0, w
        self.canvas.configure(width=w * len(vector))
        for i in range(len(vector)):
            self.create_rect([x0, y0, x1, y1], vector[i])
            x0 = x1
            x1 += w
        return

    def create_grid(self, matrix):
        yc_og = (0, 60)
        yc = (0, 60)
        self.canvas.configure(height=60 * len(matrix))
        for vector in matrix:
            self.create_row(vector, yc)
            yc = (yc[1], yc[1] + yc_og[1])

    def update_grid(self, G):
        self.canvas.update()
        self.create_grid(G)

    def activate(self, G):
        thread = threading.Thread(target=lambda: self.solve_puzzle(G))
        thread.daemon = True  
        thread.start()

    def solve_puzzle(self, G):
        i = 0
        while True:
            try:
                time.sleep(0.2)
                G = self.trace[i]
                self.update_grid(G)
                i += 1
            except IndexError:
                break
                
def start_simulation(G):
    root = tk.Tk()
    root.resizable(0, 0)
    BlockInterface(root, G)
    root.mainloop()

if __name__ == "__main__":

    x=[i.state for i in obj.my_list]
    x.reverse()
    start_simulation(x)


