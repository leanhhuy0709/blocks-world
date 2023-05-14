from astar import WorldState, generate_solution_moves
from astar import solve as astar_solve
from benchmark_cfg import cfg
import random
import time
import copy
from run import *

def initRandom(init, goal, boxes, boxes_astar):

    # init for astar
    deepcopy_boxes_astar = copy.deepcopy(boxes_astar)
    deepcopy_boxes = copy.deepcopy(boxes)
    WorldState.init_state.clear()
    WorldState.goal_state.clear()
    for i in range(WorldState.num_column):
        WorldState.init_state.append([])
        WorldState.goal_state.append([])

    for i in deepcopy_boxes_astar:
        tmp = random.randint(0, WorldState.num_column - 1)
        WorldState.init_state[tmp].append(i)
        tmp = random.randint(0, WorldState.num_column - 1)
        WorldState.goal_state[tmp].append(i)

    # init for greedy
    init = []
    goal = []
    for i in WorldState.init_state:
        init.append([])
        for j in i:
            init[len(init) - 1].append(deepcopy_boxes[int(j)])

    for i in WorldState.goal_state:
        goal.append([])
        for j in i:
            goal[len(goal) - 1].append(deepcopy_boxes[int(j)])

    return init, goal

def init_benchmark():
    WorldState.num_box = cfg.num_box
    WorldState.num_column = cfg.num_column
    WorldState.alpha = cfg.astar_alpha
    NUM_BOX = cfg.num_box
    NUM_CELL = cfg.num_column

def benchmark():
    init_benchmark()
    boxs = []
    for i in range(NUM_BOX):
        boxs.append(Box(str(i)))
    boxes_astar = map(lambda x: str(x), list(range(WorldState.num_box)))
    init = []
    goal = []
    
    greedy_time_list = []
    astar_time_list = []

    greedy_cost_list = []
    astar_cost_list = []

    greedy_num_move_list = []
    astar_num_move_list = []

    greedy_unfinished_list = []
    astar_unfinished_list = []
    for test in range(0, cfg.num_tests):
        # initialize the benchmark testcases
        greedy_init, greedy_goal = initRandom(init, goal, boxs, boxes_astar)

        for i in boxs:
            i.isInTable = False

        # Greedy solve
        start_time = time.time()
        moves, numTableSlot = solve(greedy_init, greedy_goal)
        end_time = time.time()
        greedy_time = end_time - start_time
        
        costs = map(lambda x: abs(x[0] - x[1]), moves)

        greedy_time_list.append(greedy_time)
        greedy_num_move_list.append(len(moves))
        greedy_cost_list.append(sum(costs))

        # Astar solve
        start_time = time.time()
        solution = astar_solve(WorldState.init_state, WorldState.goal_state)
        end_time = time.time()
        astar_time = end_time - start_time

        if solution != None:
            astar_solution_moves = generate_solution_moves(solution['state'], solution['closed list'])
            astar_time_list.append(astar_time)
            astar_cost_list.append(solution['state'].g)
            astar_num_move_list.append(len(astar_solution_moves))
        else:
            astar_time_list.append(None)
            astar_cost_list.append(None)
            astar_num_move_list.append(None)
            astar_unfinished_list.append(test)

        # print(f"Test {test:d} done")

    print(f"Number of tests: {cfg.num_tests:d}")
    print("======= Summary =======")
    # For greedy
    print("Greedy method:")
    # print(" * Time list: ", greedy_time_list)
    print(" * Number of moves list: ", greedy_num_move_list)
    print(" * Cost list: ", greedy_cost_list)
    print(f"\tAverage time (seconds): {sum(greedy_time_list) / cfg.num_tests:.4f}")
    print(f"\tAverage number of moves: {sum(greedy_num_move_list) / cfg.num_tests:.4f}")
    print(f"\tAverage cost: {sum(greedy_cost_list) / cfg.num_tests:.4f}")

    print("---------------------------")

    # For a star
    print("A star method:")
    print("Unfinished list: ", astar_unfinished_list)
    # print(" * Time list: ", astar_time_list)
    print(" * Number of moves list: ", astar_num_move_list)
    print(" * Cost list: ", astar_cost_list)
    print(f"\tAverage time (seconds): {sum(astar_time_list) / cfg.num_tests:.4f}")
    print(f"\tAverage number of moves: {sum(astar_num_move_list) / cfg.num_tests:.4f}")
    print(f"\tAverage cost: {sum(astar_cost_list) / cfg.num_tests:.4f}")

    #----------------------------------------
    

if __name__ == '__main__':
    benchmark()