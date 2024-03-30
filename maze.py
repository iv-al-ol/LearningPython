from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
from generic_search import dfs, node_to_path, Node, bfs, astar

class Cell(str, Enum):
    EMPTY = ".."
    BLOCKED = "##"
    START = ">>"
    GOAL = "<<"
    РАТН = "**"
    
class MazeLocation(NamedTuple):
    row: int
    column: int

class Maze:
    def __init__(self, rows: int = 15, columns: int = 15, 
                 sparseness: float = 0.2, 
                 start: MazeLocation = MazeLocation(0, 0), 
                 goal: MazeLocation = MazeLocation(14, 14)) -> None:
        # инициализация базовых переменных экземпляра
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # заполнение сетки пустыми ячейками
        self._grid: List[List[Cell]] = [[Cell.EMPTY for с in range(columns)] 
                                            for r in range(rows)]
        # заполнение сетки заблокированными ячейками
        self._randomly_fill(rows, columns, sparseness)
        # заполнение начальной и конечной позиций в лабиринте
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL
        
    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED
    
    # вывести красиво отформатированную Версию лабиринта для печати
    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if ml.row + 1 < self._rows and \
            self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
                locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and \
            self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
                locations.append(MazeLocation(ml.row - 1, ml.column))
        if ml.column + 1 < self._columns and \
            self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
                locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and \
            self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
                locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.РАТН
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL
        
def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return sqrt((xdist * xdist) + (ydist * ydist))
    return distance

def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return (xdist + ydist)
    return distance
            

if __name__ == "__main__":
    # Тестирование DFS
    m: Maze = Maze()
    print(m)
    
    solution1: Optional[Node[MazeLocation]] = dfs(m.start, 
                                                  m.goal_test, 
                                                  m.successors)
    if solution1 is None:
        print("Нет решения для поиска в глубину!")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        m.mark(path1)
        print(m)
        m.clear(path1)

    solution2: Optional[Node[MazeLocation]] = bfs(m.start,
                                                  m.goal_test,
                                                  m.successors)
    if solution2 is None:
        print("Нет решения для поиска в ширину!")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        m.mark(path2)
        print(m)
        m.clear(path2)

    distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
    solutionЗ: Optional[Node[MazeLocation]] = astar(m.start, 
                                                    m.goal_test, 
                                                    m.successors, distance)
    if solutionЗ is None:
        print("Нет решения для A*!")
    else:
        pathЗ: List[MazeLocation] = node_to_path(solutionЗ)
        m.mark(pathЗ)
        print(m)
    