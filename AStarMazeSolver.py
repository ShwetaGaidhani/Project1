"""
Optimized A* Maze Solver
Finds the shortest path from Start (S) to Goal (G)
"""

import heapq


# Heuristic (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ---------------------------------
# Maze Class
# ---------------------------------
class Maze:

    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0])

    # Get valid neighbors
    def neighbors(self, pos):

        r, c = pos
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        result = []

        for dr, dc in directions:

            nr = r + dr
            nc = c + dc

            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] == 0:
                    result.append((nr, nc))

        return result


    # Display maze with path
    def display(self, path=None):

        for r in range(self.rows):

            row = ""

            for c in range(self.cols):

                if (r,c) == self.start:
                    row += "S "

                elif (r,c) == self.goal:
                    row += "G "

                elif path and (r,c) in path:
                    row += "* "

                elif self.grid[r][c] == 1:
                    row += "# "

                else:
                    row += ". "

            print(row)


# ---------------------------------
# A* Solver
# ---------------------------------
class AStarSolver:

    def __init__(self, maze):
        self.maze = maze

    def solve(self):

        start = self.maze.start
        goal = self.maze.goal

        open_list = []
        heapq.heappush(open_list, (0, start))

        came_from = {}
        g_cost = {start: 0}

        closed_set = set()
        nodes_explored = 0

        while open_list:

            _, current = heapq.heappop(open_list)

            if current in closed_set:
                continue

            closed_set.add(current)
            nodes_explored += 1

            # Goal reached
            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return path, nodes_explored

            for neighbor in self.maze.neighbors(current):

                if neighbor in closed_set:
                    continue

                new_cost = g_cost[current] + 1

                if neighbor not in g_cost or new_cost < g_cost[neighbor]:

                    g_cost[neighbor] = new_cost
                    f_cost = new_cost + heuristic(neighbor, goal)

                    heapq.heappush(open_list, (f_cost, neighbor))
                    came_from[neighbor] = current

        return None, nodes_explored


    # Build final path
    def reconstruct_path(self, came_from, current):

        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path


# ---------------------------------
# User Input Maze
# ---------------------------------
def get_maze():

    rows = int(input("Enter number of rows: "))
    print("\nEnter maze rows:")
    print("S = Start, G = Goal, # = Wall, . = Free\n")

    grid = []
    start = None
    goal = None

    for r in range(rows):

        line = input(f"Row {r+1}: ")

        row = []

        for c, ch in enumerate(line):

            if ch == "#":
                row.append(1)

            elif ch == "S":
                start = (r,c)
                row.append(0)

            elif ch == "G":
                goal = (r,c)
                row.append(0)

            else:
                row.append(0)

        grid.append(row)

    return grid, start, goal


# ---------------------------------
# Main Program
# ---------------------------------
if __name__ == "__main__":

    grid, start, goal = get_maze()

    maze = Maze(grid, start, goal)

    solver = AStarSolver(maze)

    path, explored = solver.solve()

    if path:

        print("\nPath Found!\n")

        maze.display(path)

        print("\nPath:", path)
        print("Steps:", len(path)-1)
        print("Nodes Explored:", explored)

    else:

        print("\nNo Path Found")
        print("Nodes Explored:", explored)