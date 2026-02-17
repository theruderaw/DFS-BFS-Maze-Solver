def dfs(table, start, end, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
    
    m, n = len(table), len(table[0])
    x, y = start
    
    if start == end:
        return path 
    
    visited.add(start)
    
    for dx, dy in [(1,0),(0,1),(0,-1),(-1,0)]:
        nx, ny = x + dx, y + dy
        
        # Check bounds
        if 0 <= nx < m and 0 <= ny < n:
            if table[nx][ny] != 1 and (nx, ny) not in visited:
                res_path = dfs(table, (nx, ny), end, path + [(nx, ny)], visited)
                if res_path: 
                    return res_path
    return None 

from collections import deque

def bfs(table, start, end):
    m, n = len(table), len(table[0])
    visited = [[False]*n for _ in range(m)]
    parent = [[None]*n for _ in range(m)]

    queue = deque([start])
    visited[start[0]][start[1]] = True

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            path = []
            curr = end
            while curr is not None:
                path.append(curr)
                curr = parent[curr[0]][curr[1]]
            path.reverse()
            return path

        for dx, dy in [(1,0),(0,1),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < m and 0 <= ny < n:
                if table[nx][ny] != 1 and not visited[nx][ny]:
                    visited[nx][ny] = True
                    parent[nx][ny] = (x, y)
                    queue.append((nx, ny))

    return None  