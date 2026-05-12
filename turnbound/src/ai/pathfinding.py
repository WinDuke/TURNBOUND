"""A* Pathfinding implementation."""

import heapq
from typing import Optional


def find_path(
    start: tuple[int, int],
    goal: tuple[int, int],
    arena_map: dict,
    blocked_entities: set[tuple[int, int]] = None,
) -> list[tuple[int, int]]:
    """
    Find shortest path using A* algorithm.
    
    Returns list of positions from start to goal (inclusive).
    Returns empty list if no path exists.
    """
    if blocked_entities is None:
        blocked_entities = set()
    
    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
        """Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def is_walkable(pos: tuple[int, int]) -> bool:
        """Check if position is walkable."""
        x, y = pos
        tile = arena_map.get((x, y), {})
        terrain_type = tile.get("type", "floor")
        
        if terrain_type in ("wall", "obstacle", "water", "lava"):
            return False
        if pos in blocked_entities:
            return False
        return True
    
    # Check if start or goal is blocked
    if not is_walkable(start) or not is_walkable(goal):
        return []
    
    # Priority queue: (f_score, g_score, position, path)
    open_set = [(heuristic(start, goal), 0, start, [start])]
    visited = set()
    
    while open_set:
        f_score, g_score, current, path = heapq.heappop(open_set)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        # Goal reached
        if current == goal:
            return path
        
        # Explore neighbors (4-directional movement)
        x, y = current
        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            if not is_walkable(neighbor):
                continue
            
            new_g_score = g_score + 1
            new_f_score = new_g_score + heuristic(neighbor, goal)
            new_path = path + [neighbor]
            
            heapq.heappush(open_set, (new_f_score, new_g_score, neighbor, new_path))
    
    # No path found
    return []


def get_direction_to_target(
    current_pos: tuple[int, int],
    target_pos: tuple[int, int],
    arena_map: dict,
    blocked_entities: set[tuple[int, int]] = None,
) -> tuple[int, int]:
    """
    Get the next move direction toward a target.
    
    Returns (dx, dy) tuple for the best move.
    Returns (0, 0) if no valid move exists.
    """
    path = find_path(current_pos, target_pos, arena_map, blocked_entities)
    
    if len(path) < 2:
        return (0, 0)
    
    next_pos = path[1]  # Second element is the first step
    dx = next_pos[0] - current_pos[0]
    dy = next_pos[1] - current_pos[1]
    
    return (dx, dy)
