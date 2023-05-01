import random as rd, time, math
rd.seed(time.time())
NUM_BOX = 20
NUM_CELL = 10
IS_USE_RANDOM = True

class Box:
    def __init__(self, name, st = -1, ed = -1):
        self.name = name 
        self.st = st
        self.ed = ed
        self.isInTable = False
    def __str__(self):
        return self.name
    def __eq__(self, other):
        if isinstance(other, Box):
            return self.name == other.name
        return NotImplemented

def move(curr, source, target, isSave = True):
    if source >= len(curr): 
        print("Source is not valid")
        raise "Error"
    if target >= len(curr): 
        print("Target is not valid")
        raise "Error"
    if len(curr[source]) == 0:
        print("Can't pop []")
        raise "Error"
    
    #print("Move from " + str(source) + " to " + str(target))
    curr[target].append(curr[source].pop())
    return (source, target)

def isOnTop(curr, st):
    return st[1] + 1 == len(curr[st[0]])

def initRandom(init, goal, boxs):
    init.clear()
    goal.clear()
    for i in range(NUM_CELL):
        init.append([])
        goal.append([])

    for i in boxs:
        tmp = rd.randint(0, NUM_CELL - 1)
        init[tmp].append(i)
        tmp = rd.randint(0, NUM_CELL - 1)
        goal[tmp].append(i)
    
    f = open("test.txt", "w")
    f.write("Init:\n")
    f.write(str(list(map(lambda x: list(map(str, x)), init))))
    f.write("\nGoal:\n")
    f.write(str(list(map(lambda x: list(map(str, x)), goal))))
    f.close()
    
def initNotRandom(init, goal, boxs):
    """Need edit init_s and goal_s in this function"""
    init_s = [['4'], ['2', '3', '0', '1'], []]
    goal_s = [['0', '3'], ['2'], ['1', '4']]
    count = 0
    for i in init_s:
        for j in i:
            count += 1
    
    
    if count != NUM_BOX:
        raise "Error: Init not random wrong"
    
    for i in init_s:
        init.append([])
        for j in i:
            init[len(init) - 1].append(boxs[int(j)])

    for i in goal_s:
        goal.append([])
        for j in i:
            goal[len(goal) - 1].append(boxs[int(j)])

def printResult(moves, numTableSlot, start_time, end_time):
    print("Number of Box:", NUM_BOX)
    print("Number of Cell (Init):", NUM_CELL)
    print("Number of moves: ", len(moves))
    print("Number of table slot: ", numTableSlot)
    elapsed_time = end_time - start_time
    print("Elapsed time: ", math.floor(elapsed_time * 1000000) / 1000, " ms")
    print("------------------------------------------------------------------")

def main():
    boxs = []
    for i in range(NUM_BOX):
        boxs.append(Box(str(i)))
    init = []
    goal = []
    
    if IS_USE_RANDOM:
        initRandom(init, goal, boxs)
    else:
        initNotRandom(init, goal, boxs)
    #----------------------------------------
    
    start_time = time.time()
    for i in boxs: i.isInTable = False
    moves, numTableSlot = solve(init, goal)
    end_time = time.time()
    printResult(moves, numTableSlot, start_time, end_time)
    return init, goal, moves, numTableSlot
    #print(moves)
    
def compareBox(box1, curr, check):
    val1 = len(curr[box1.st[0]]) - box1.st[1]
    if val1 > 1: return NUM_BOX * 2 #Không ở đỉnh -> Không lấy được
    val2 = box1.ed[1] - check[box1.ed[0]]
    if val2 == 0 and len(curr[box1.ed[0]]) == check[box1.ed[0]]: return -NUM_BOX * 2 #Có thể đặt vào đúng vị trí -> Lấy liền
    res = val2 + box1.isInTable * NUM_BOX / 2 #Lựa chọn những thằng ở đỉnh, hạn chế những thằng ở Table
    return res

def solve(init, goal):
    curr = []
    for i in range(len(init)):
        curr.append([])
        for j in range(len(init[i])):
            curr[i].append(init[i][j])
    
    for i in range(len(init)):
        for j in range(len(init[i])):
            init[i][j].st = [i, j].copy()
    
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            goal[i][j].ed = [i, j].copy()
    
    stack = []
    check = []
    table = []
    for i in range(len(init)):
        tmp = 0
        while tmp < len(init[i]) and tmp < len(goal[i]) and init[i][tmp].name == goal[i][tmp].name:
            tmp += 1
        for j in range(tmp, len(init[i])):
            stack.append(init[i][j])
        check.append(tmp)
        if tmp == len(goal[i]) and tmp == len(init[i]):
            table.append(i)
    
    moves = []
    while len(stack) > 0:
        stack.sort(key = lambda x: compareBox(x, curr, check), reverse = True)
        box = stack.pop()
        st = box.st
        ed = box.ed
        if check[ed[0]] == ed[1]:
            if len(curr[ed[0]]) == ed[1]:
                moves.append(move(curr, st[0], ed[0]))                    
                check[ed[0]] += 1
                if check[st[0]] == len(curr[st[0]]) and check[st[0]] == len(goal[st[0]]): 
                    table.append(st[0])
                if check[ed[0]] == len(goal[ed[0]]):
                    table.append(ed[0])
                box.st[0], box.st[1] = box.ed[0], box.ed[1]
               
            elif st[0] == ed[0]:
                if len(table) == 0: 
                    init.append([])
                    curr.append([])
                    goal.append([])
                    check.append(0)
                    table.append(len(init) - 1)
                tb = table.pop()
                moves.append(move(curr, st[0], tb))
                box.st[0], box.st[1] = tb, len(curr[tb]) - 1
                box.isInTable = True
                stack.append(box)
            else:
                if len(table) == 0: 
                    init.append([])
                    curr.append([])
                    goal.append([])
                    check.append(0)
                    table.append(len(init) - 1)
                tb = table.pop()
                moves.append(move(curr, ed[0], tb))
                stack.append(box)
                boxEd = curr[tb][len(curr[tb]) - 1]
                boxEd.st[0], boxEd.st[1] = tb, len(curr[tb]) - 1
                boxEd.isInTable = True
        elif check[ed[0]] < ed[1]:
            if len(table) == 0:
                init.append([])
                curr.append([])
                goal.append([])
                check.append(0)
                table.append(len(init) - 1)
            tb = table.pop()
            moves.append(move(curr, st[0], tb))
            box.st[0], box.st[1] = tb, len(curr[tb]) - 1
            box.isInTable = True
            stack.append(box)
    numTableSlot = len(init) - NUM_CELL
    for i in range(numTableSlot):
        init.pop()
        goal.pop()    
    return moves, numTableSlot

def compareBox2(box1, curr, check):
    val1 = len(curr[box1.st[0]]) - box1.st[1]
    #if val1 > 1: return NUM_BOX * 2 #Không ở đỉnh -> Không lấy được
    val2 = box1.ed[1] - check[box1.ed[0]]
    #if val2 == 0 and len(curr[box1.ed[0]]) == check[box1.ed[0]]: return -NUM_BOX * 2 #Có thể đặt vào đúng vị trí -> Lấy liền
    res = val1 * NUM_BOX + val2 + box1.isInTable * NUM_BOX / 2 #Lựa chọn những thằng ở đỉnh, hạn chế những thằng ở Table
    return res

def solve2(init, goal):
    curr = []
    for i in range(len(init)):
        curr.append([])
        for j in range(len(init[i])):
            curr[i].append(init[i][j])
    
    for i in range(len(init)):
        for j in range(len(init[i])):
            init[i][j].st = [i, j].copy()
    
    for i in range(len(goal)):
        for j in range(len(goal[i])):
            goal[i][j].ed = [i, j].copy()
    stack = []
    check = []
    table = []
    for i in range(len(init)):
        tmp = 0
        while tmp < len(init[i]) and tmp < len(goal[i]) and init[i][tmp].name == goal[i][tmp].name:
            tmp += 1
        for j in range(tmp, len(init[i])):
            stack.append(init[i][j])
        check.append(tmp)
        if tmp == len(goal[i]) and tmp == len(init[i]):
            table.append(i)
    
    moves = []
    while len(stack) > 0:
        stack.sort(key = lambda x: compareBox2(x, curr, check), reverse = True)
        box = stack.pop()
        st = box.st
        ed = box.ed
        if check[ed[0]] == ed[1]:
            if len(curr[ed[0]]) == ed[1]:
                moves.append(move(curr, st[0], ed[0]))
                check[ed[0]] += 1
                if check[st[0]] == len(curr[st[0]]) and check[st[0]] == len(goal[st[0]]): 
                    table.append(st[0])
                if check[ed[0]] == len(goal[ed[0]]):
                    table.append(ed[0])
                box.st[0], box.st[1] = box.ed[0], box.ed[1]
            elif st[0] == ed[0]:
                if len(table) == 0: 
                    init.append([])
                    curr.append([])
                    goal.append([])
                    check.append(0)
                    table.append(len(init) - 1)
                tb = table.pop()
                moves.append(move(curr, st[0], tb))
                box.st[0], box.st[1] = tb, len(curr[tb]) - 1
                box.isInTable = True
                stack.append(box)
            else:
                if len(table) == 0: 
                    init.append([])
                    curr.append([])
                    goal.append([])
                    check.append(0)
                    table.append(len(init) - 1)
                tb = table.pop()
                moves.append(move(curr, ed[0], tb))
                stack.append(box)
                boxEd = curr[tb][len(curr[tb]) - 1]
                boxEd.st[0], boxEd.st[1] = tb, len(curr[tb]) - 1
                boxEd.isInTable = True
        elif check[ed[0]] < ed[1]:
            if len(table) == 0:
                init.append([])
                curr.append([])
                goal.append([])
                check.append(0)
                table.append(len(init) - 1)
            tb = table.pop()
            moves.append(move(curr, st[0], tb))
            box.st[0], box.st[1] = tb, len(curr[tb]) - 1
            box.isInTable = True
            stack.append(box)
    numTableSlot = len(init) - NUM_CELL
    for i in range(numTableSlot):
        init.pop()
        goal.pop()    
    return moves, numTableSlot

main()