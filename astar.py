import copy
import random
import time
import math
random.seed(time.time())


class WorldState:
    init_state = []
    goal_state = []
    num_box = 10
    num_column = 7
    use_random_states = True
    alpha = 0.03

    def __init__(self, state, f, g, h, parent_move=None) -> None:
        self.state = state
        self.f = f
        self.g = g  # Total cost of all previous moves
        self.h = h
        self.parent_move = parent_move
    
    def str_state(self):
        return str(self.state)
    
    def move(self, move):
        from_col = move[0]
        to_col = move[1]

        # Make a new state out of the current state and move
        new_state = WorldState(copy.deepcopy(self.state), f=0, g=0, h=0, parent_move=move)
        box = new_state.state[from_col].pop()
        new_state.state[to_col].append(box)
        new_state.g = self.g + abs(to_col - from_col)
        new_state.h = WorldState.calculate_h(new_state.state, WorldState.goal_state)
        new_state.f = WorldState.alpha*new_state.g + new_state.h

        return new_state

    def generate_possible_moves(self) -> list:
        move_list = []
        for from_col in range(0, WorldState.num_column):
            # Can't move from an empty column
            if len(self.state[from_col]) == 0:
                continue

            for to_col in range(0, WorldState.num_column):
                if from_col == to_col:
                    continue
                
                # Avoid going backward
                if self.parent_move is not None:
                    if self.parent_move[1] == from_col and self.parent_move[0] == to_col:
                        break
                
                move_list.append((from_col, to_col))

        return move_list
    
    def generate_states(self, possible_moves) -> list:
        world_state_lists = []

        for move in possible_moves:
            new_state = self.move(move)
            world_state_lists.append(new_state)

        return world_state_lists

    def previous_state_str(self) -> str:
        if self.parent_move is None:
            return None
        prev_state = copy.deepcopy(self.state)
        from_col = self.parent_move[1]
        to_col = self.parent_move[0]

        box = prev_state[from_col].pop()
        prev_state[to_col].append(box)

        return str(prev_state)

    @staticmethod
    def state_score(state):
        return state.f
    
    @staticmethod
    def equal_states(state1, state2):
        return state1 == state2
    
    @staticmethod
    def calculate_h(state, goal_state):
        correct_count = 0
        for i in range(0, WorldState.num_column):
            index = 0
            while index < len(state[i]) and index < len(goal_state[i]) and state[i][index] == goal_state[i][index]:
                index += 1
                correct_count += 1

        return WorldState.num_box - correct_count



def solve(init_state, goal_state):
    init_world_state = WorldState(state=init_state, f=0, g=0, h=0, parent_move=None)
    open_list = {init_world_state.str_state(): init_world_state}
    closed_list = {}

    # While open_list not empty
    while bool(open_list):

        min_key, min_world_state = min(open_list.items(), key=lambda x: x[1].f) # Get state with minimum f cost
        del open_list[min_key]
        closed_list[min_key] = min_world_state

        # If this state is equal to goal state, found it
        if WorldState.equal_states(min_world_state.state, goal_state):
            return {
                'state': min_world_state,
                'closed list': closed_list,
            }

        # print(f"Current f:{min_world_state.f:.2f}")

        # Get all possible next states
        possible_next_states = min_world_state.generate_states(min_world_state.generate_possible_moves())

        for next_state in possible_next_states:
            next_state_str = next_state.str_state()
            if next_state_str in closed_list:
                continue

            if next_state_str not in open_list:
                open_list[next_state_str] = next_state

            if open_list[next_state_str].f > next_state.f:
                open_list[next_state_str] = next_state

    return None

def generate_solution_moves(solution_state, closed_list):
    solution_sequence = []
    current_state = solution_state
    while current_state.parent_move is not None:
        prev_state_str = current_state.previous_state_str()

        if prev_state_str not in closed_list:
            raise RuntimeError("Closed list error!")
        
        solution_sequence.insert(0, current_state.parent_move)
        current_state = closed_list[prev_state_str]

    return solution_sequence


def initRandom(init, goal, boxes):
    init.clear()
    goal.clear()
    for i in range(WorldState.num_column):
        init.append([])
        goal.append([])

    for i in boxes:
        tmp = random.randint(0, WorldState.num_column - 1)
        init[tmp].append(i)
        tmp = random.randint(0, WorldState.num_column - 1)
        goal[tmp].append(i)
    
    f = open("test_astar.txt", "w")
    f.write("Init:\n")
    f.write(str(init))
    f.write("\nGoal:\n")
    f.write(str(goal))
    f.close()

def initNotRandom(init, goal, boxes):
    init = [['1', '2'], ['5', '3'], [], ['6', '4']]
    goal = [['1', '5'], ['2', '6'], ['3'], ['4']]

    count_init = 0
    for i in init:
        count_init += len(i)
    
    count_goal = 0
    for i in goal:
        count_goal += len(i)
    
    if count_init != WorldState.num_box:
        raise AssertionError("Manual initial state is wrong")
    
    if count_goal != WorldState.num_box:
        raise AssertionError("Manual goal state is wrong")

def main():
    boxes = list(map(lambda x: str(x), list(range(WorldState.num_box))))

    if WorldState.use_random_states:
        initRandom(WorldState.init_state, WorldState.goal_state, boxes)
    else:
        initNotRandom(WorldState.init_state, WorldState.goal_state, boxes)

    start_time = time.time()
    solution = solve(WorldState.init_state, WorldState.goal_state)
    end_time = time.time()
    seconds_elapsed = end_time - start_time

    if solution != None:
        solution_moves = generate_solution_moves(solution['state'], solution['closed list'])
        print(f"Found solution in {seconds_elapsed:.5f} seconds")
        print(f"Moving cost (total horizontal distance traversed): {solution['state'].g:d}")
        print(f"Number of moves: {len(solution_moves):d}")
        print(solution_moves)
    else:
        print("Couldn't find a solution")


if __name__ == "__main__":
    main()
