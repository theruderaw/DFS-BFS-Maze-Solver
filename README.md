# Maze Solver

An interactive pathfinding visualizer implemented in Python using the Pygame library. The application provides a 15×15 grid environment for constructing arbitrary maze layouts, executing classical graph traversal algorithms with step-by-step animation, and optionally solving mazes through direct user input.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Start and End Points](#start-and-end-points)
  - [Wall Placement](#wall-placement)
  - [Running Algorithms](#running-algorithms)
  - [User Solve Mode](#user-solve-mode)
  - [Resetting the Grid](#resetting-the-grid)
- [Algorithm Reference](#algorithm-reference)
  - [Breadth-First Search](#breadth-first-search)
  - [Depth-First Search](#depth-first-search)
  - [Comparative Analysis](#comparative-analysis)
- [Visual Encoding](#visual-encoding)
- [Controls](#controls)
- [Code Structure](#code-structure)
- [Known Limitations](#known-limitations)
- [Planned Enhancements](#planned-enhancements)
- [License](#license)

---

## Features

- Interactive 15×15 grid supporting freehand wall construction via click-and-drag
- Real-time animated visualization of Breadth-First Search and Depth-First Search
- Automatic shortest-path reconstruction and rendering upon algorithm completion
- User Solve mode for manual path submission with correctness validation
- Active mode indicator showing the currently selected operation at all times

---

## Requirements

- Python 3.7 or later
- [Pygame](https://www.pygame.org/) 2.x

---

## Installation

Clone or download the repository, then install the required dependency:

```bash
pip install pygame
```

No additional packages are required.

---

## Usage

Launch the application from the project directory:

```bash
python maze_solver.py
```

A 600×740 pixel window will open containing the grid and a two-row control panel along the bottom. All interaction is mouse-driven. The currently active mode is indicated by a yellow border on the corresponding button.

### Start and End Points

Select **Start** to enter start-placement mode. Click any cell to designate it as the origin; the cell is rendered in green. Only one start point may exist at a time — selecting a new cell automatically clears the previous designation.

Select **End** to enter end-placement mode. Click any cell to designate it as the destination; the cell is rendered in red. The same single-selection rule applies.

### Wall Placement

Select **Wall** to enter wall-drawing mode. Clicking an empty cell converts it to a wall; clicking an existing wall removes it. Holding the mouse button and dragging will paint or erase walls continuously, which is useful for constructing corridors and enclosed regions. Walls cannot be placed on the designated start or end cells.

### Running Algorithms

Both a start point and an end point must be placed before an algorithm can be executed. Attempting to run either algorithm without them will display a warning overlay.

Select **BFS** to execute Breadth-First Search, or **DFS** to execute Depth-First Search.

During execution, explored cells are rendered in blue as the algorithm progresses. Upon locating the destination, the reconstructed path is traced in yellow. If no path exists between the start and end points — for example, because the end cell is fully enclosed by walls — no path will be rendered and the grid will retain the visited-cell coloring.

Previously computed results (visited cells and path) are cleared automatically when a new algorithm is started.

### User Solve Mode

Select **User Solve** to enter manual path-drawing mode. Any prior user path is cleared upon entering this mode. Click and drag through the grid to trace a route from the start to the end; traversed cells are rendered in orange. The drawn path does not need to include the start or end cells themselves, as they are prepended and appended automatically during validation.

Once a path has been drawn, select **Submit** to validate it. The application will report one of three outcomes:

- **"Path is empty!"** — no cells were traced before submitting.
- **"Hit a wall!"** — the path passes through at least one wall cell.
- **"Maze solved correctly!"** — the path is valid; the grid resets to its initial state.

### Resetting the Grid

Select **Reset** to clear all walls, remove the start and end designations, erase any user path, and return the grid to a blank state.

---

## Algorithm Reference

### Breadth-First Search

Breadth-First Search (BFS) is an uninformed graph traversal algorithm that explores vertices in order of their distance from the source. It proceeds in discrete layers: all vertices at distance _d_ are fully explored before any vertex at distance _d + 1_ is visited.

**Procedure**

1. Enqueue the start cell and mark it as visited.
2. Dequeue the cell at the front of the queue.
3. If the dequeued cell is the destination, terminate and reconstruct the path.
4. Otherwise, examine all four cardinal neighbors (up, down, left, right). For each neighbor that is unvisited and not a wall, mark it as visited, record its predecessor, and enqueue it.
5. Repeat from step 2 until the destination is reached or the queue is exhausted.
6. Reconstruct the path by following predecessor references from the destination back to the source.

**Optimality**

Because BFS explores cells strictly by increasing distance from the source, the first time it reaches the destination is necessarily via the shortest possible path (measured in the number of steps). This guarantee holds for all unweighted graphs.

**Observed behavior**

The visited region expands outward from the source in a roughly uniform, diamond-shaped wavefront. The exploration is systematic and exhaustive at each distance level before proceeding further.

**Complexity**

| Dimension | Complexity |
|-----------|------------|
| Time      | O(V + E), where V is the number of cells and E the number of passable edges |
| Space     | O(V) — the queue may contain up to all reachable cells simultaneously |

---

### Depth-First Search

Depth-First Search (DFS) is an uninformed graph traversal algorithm that advances as far as possible along a single branch before backtracking to explore alternative branches. It does not consider vertex distance and makes no guarantee about the length of the path it discovers.

**Procedure**

1. Visit the start cell and mark it as visited.
2. Examine the first unvisited, non-wall neighbor in the defined neighbor order (down, right, left, up).
3. Recursively visit that neighbor, repeating the process.
4. If no unvisited neighbors exist (a dead end), return to the calling frame — this is the backtracking step.
5. Continue until the destination is reached or all reachable cells have been visited.
6. Reconstruct the path by following predecessor references from the destination back to the source.

In this implementation, DFS is realized recursively. Each invocation of `dfs_visit(x, y)` processes a single cell and recurses into its successors. On the 15×15 grid (225 cells maximum), the recursion depth remains well within Python's default limit.

**Optimality**

DFS does not guarantee a shortest path. The path it returns depends entirely on the neighbor traversal order and the topology of the maze. In the worst case, the algorithm may traverse nearly the entire grid before finding a path that a different traversal order would have found much sooner.

**Observed behavior**

The visited region advances aggressively in one direction, often reaching distant areas of the grid before exploring cells adjacent to the source. When a dead end is reached, the algorithm backtracks and resumes from the most recent unvisited branch, producing an irregular, winding exploration pattern.

**Complexity**

| Dimension | Complexity |
|-----------|------------|
| Time      | O(V + E) — identical to BFS in the worst case |
| Space     | O(V) — the call stack depth is bounded by the number of cells in the longest path |

---

### Comparative Analysis

| Property | BFS | DFS |
|---|---|---|
| Shortest-path guarantee | Yes | No |
| Typical memory consumption | Higher — entire frontier is stored | Lower — only the active path is on the call stack |
| Implementation style (this project) | Iterative, using `collections.deque` | Recursive |
| Exploration pattern | Uniform radial expansion | Deep, directional probing with backtracking |
| Suitable when optimality is required | Yes | No |
| Suitable when any valid path suffices | Yes | Yes |

BFS is the appropriate choice when the shortest path is required. DFS may be preferred in memory-constrained environments or when early termination on any valid path is acceptable and path length is not a concern.

---

## Visual Encoding

| Color  | Cell State |
|--------|------------|
| White  | Unvisited, passable cell |
| Black  | Wall (impassable) |
| Green  | Designated start point |
| Red    | Designated end point |
| Blue   | Visited during algorithm execution |
| Yellow | Reconstructed solution path |
| Orange | User-drawn path (User Solve mode) |

---

## Controls

| Action | Input |
|--------|-------|
| Set start point | Click **Start**, then click a cell |
| Set end point | Click **End**, then click a cell |
| Place or remove a wall | Click **Wall**, then click or drag on cells |
| Execute BFS | Click **BFS** |
| Execute DFS | Click **DFS** |
| Draw a manual path | Click **User Solve**, then click and drag |
| Submit a manual path | Click **Submit** |
| Clear the grid | Click **Reset** |
| Exit the application | Close the window |

---

## Code Structure

The application is contained within a single source file, `maze_solver.py`. The table below summarizes the principal components.

| Component | Description |
|-----------|-------------|
| Constants and color definitions | Grid dimensions (`ROWS`, `COLS`, `CELL_SIZE`), RGB color values, and frame rate |
| `color_map` | Maps integer cell-state codes to display colors |
| `buttons` | List of button descriptors specifying geometry, color, label, and associated mode |
| `draw_grid()` | Renders all grid cells and the button panel on each frame |
| `get_cell_from_mouse(pos)` | Converts a pixel coordinate to a `(row, col)` grid index |
| `show_message(text, duration)` | Displays a modal overlay message for a specified duration |
| `run_algorithm(algo)` | Executes BFS or DFS with per-step animation and reconstructs the solution path |
| `check_user_path()` | Validates the user-drawn path for wall intersections and reports the result |
| Main event loop | Processes Pygame events, dispatches mouse input to the appropriate handler, and maintains render state |

---

## Known Limitations

- Movement is restricted to the four cardinal directions. Diagonal traversal is not supported by either the algorithms or the user path validator.
- The DFS implementation is recursive. On grids significantly larger than 15×15, Python's default recursion limit (`sys.getrecursionlimit()`, typically 1000) could be exceeded. An iterative implementation using an explicit stack would be required for such cases.
- User path validation confirms only that no wall is intersected. It does not enforce cell-to-cell adjacency, meaning a disconnected path may be submitted and pass validation.
- Maze layouts must be constructed manually. No procedural maze generation is provided.
- Only BFS and DFS are implemented. No heuristic or weighted-graph algorithms (e.g., A*, Dijkstra's) are available.

---

## Planned Enhancements

- A* search with configurable heuristic (Manhattan or Euclidean distance)
- Dijkstra's algorithm for weighted-edge pathfinding scenarios
- Procedural maze generation via recursive backtracking or randomized Prim's algorithm
- Optional diagonal movement with configurable movement cost
- Animation speed control exposed as a slider in the UI
- Visited-cell and path-length counters displayed during and after execution
- Strict adjacency enforcement in user path validation
- Maze layout serialization for save and load functionality

---

## License

This project is made available for personal and educational use.
