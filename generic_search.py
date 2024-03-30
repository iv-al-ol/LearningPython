from __future__ import annotations
from heapq import heappop, heappush
from typing import TypeVar, Iterable, Sequence, \
                    Generic, List, Callable, Set, \
                    Deque, Dict, Any, Optional
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []
        
    @property
    def empty(self) -> bool:
        return not self._container #не равно True для пустого контейнера
    
    def push(self, item: T) -> None:
        self._container.append(item)
    
    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], 
                 cost: float = 0.0, heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic
        
    def __lt__(self, other: Node) -> bool:
        return (self.cost + 
                self .heuristic) < (other.cost + 
                                    other.heuristic)
                
def dfs(initial: T, goal_test: Callable[[T], bool], 
        successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # frontier - то, что нам нужно проверить
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    # expLored - то, где мы уже были
    explored: Set[T] = {initial}
    
    # продолжаем, пока есть что просматривать
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # если мы нашли искомое, заканчиваем
        if goal_test(current_state):
            return current_node
        # проверяем, куда можно двинуться дальше и что мы еще не исследовали
        for child in successors(current_state):
            # пропустить состояния, которые уже исследовали
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None # все проверили, пути к целевой точке не нашли

def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # двигаемся назад, от конца к началу
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path

class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()
        
    @property
    def empty(self) -> bool:
        return not self._container # не рабно True для пустого контейнера
    
    def push(self, item: T) -> None:
        self._container.append(item)
    
    def pop(self) -> T:
        return self._container.popleft() # FIFO
    
    def __repr__(self) -> str:
        return repr(self._container)

def bfs(initial: T, goal_test: Callable[[T], bool], 
        successors: Callable[[T], List[T]]) -> Optional[Node[T]]:
    # froпtier - это то, что мы только собираемся проверить
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # expLored - это то, что уже проверено
    explored: Set[T] = {initial}
    
    # продолжаем, пока есть что проверять
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # если мы нашли искомое, то процесс закончен
        if goal_test(current_state):
            return current_node
        # ищем неисследованные ячейки, в которые можно перейти
        for child in successors(current_state):
            if child in explored: #пропустить состояния, которые уже исследовали
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None # все проверили, пути к целевой точке не нашли

class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []
        
    @property
    def empty(self) -> bool:
        return not self._container #не Тrие для пустого контейнера
    
    def push(self, item: T) -> None:
        heappush(self._container, item) #поместить в очередь по приоритету

    def pop(self) -> T:
        return heappop(self._container) # извлечь по приоритету
    
    def _repr_(self) -> str:
        return repr(self._container)

def astar(initial: T, goal_test: Callable[[T], bool], 
          successors: Callable[[T], List[T]], 
          heuristic: Callable[[T], float]) -> Optional[Node[T]]:
    # froпtier - то, куда мы хотим двигаться
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # expLored - то, что мы уже просмотрели
    explored: Dict[T, float] = {initial: 0.0}
    # продолжаем, пока есть что просматривать
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # если цель найдена, мы закончили
        if goal_test(current_state):
            return current_node
        # проверяем, в какую из неисследованных ячеек направиться
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1
            # 1 - для сетки, для более сложных приложений здесь
            # должна быть функция затрат
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost,
                heuristic(child)))
    return None # все проверили, пути к целевой точке не нашли
