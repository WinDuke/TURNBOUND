"""
A* Pathfinding Algorithm for TURNBOUND.
Finds the shortest path on a grid avoiding obstacles.
"""
import heapq
from typing import List, Tuple, Optional

Grid = List[List[str]]
Point = Tuple[int, int]

def heuristic(a: Point, b: Point) -> int:
    """Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(grid: Grid, point: Point) -> List[Point]:
    """Get valid neighboring cells (up, down, left, right)."""
    x, y = point
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    neighbors = []
    # Directions: Right, Left, Down, Up
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows:
            # Check if not a wall (#)
            if grid[ny][nx] != '#':
                neighbors.append((nx, ny))
                
    return neighbors

def find_path(grid: Grid, start: Point, end: Point) -> Optional[List[Point]]:
    """
    Find the shortest path from start to end using A*.
    
    Args:
        grid: 2D list of strings ('.' for floor, '#' for wall)
        start: (x, y) tuple
        end: (x, y) tuple
        
    Returns:
        List of (x, y) tuples representing the path, or None if no path exists.
    """
    if not grid or not grid[0]:
        return None
        
    if grid[start[1]][start[0]] == '#' or grid[end[1]][end[0]] == '#':
        return None
        
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1] # Reverse to get start -> end
            
        for neighbor in get_neighbors(grid, current):
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score, neighbor))
                
    return None # No path found
