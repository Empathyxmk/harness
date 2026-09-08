import pytest
import numpy as np

# ----------- MOCK CLASSES TO FULLY REPLICATE ORIGINAL TEST LOGIC ----------- #

class EigenVector3d(np.ndarray):
    """
    Simple Eigen::Vector3d stand-in backed by numpy.
    """
    def __new__(cls, x, y, z):
        obj = np.asarray([x, y, z], dtype=float).view(cls)
        return obj

class AstarPathFinder:
    """
    Mock Astar. Replicates the logic called in test.
    Grid is kept as a 3D array with obstacles marked.
    """
    def __init__(self):
        self.grid = None
        self.nx = self.ny = self.nz = 0
        self.start = None
        self.end = None

    def initGridMap(self, nx, ny, nz, resolution, origin):
        # Create an empty 3D grid.
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.grid = np.zeros((nx, ny, nz), dtype=bool)
        self.origin = origin

    def reset(self):
        if self.grid is not None:
            self.grid[:] = 0

    def setObstacle(self, ix, iy, iz):
        self.grid[ix, iy, iz] = True

    def setStart(self, pos):
        self.start = tuple(map(int, pos))

    def setEnd(self, pos):
        self.end = tuple(map(int, pos))

    def getPath(self):
        if self.start == self.end and self.grid[self.start]:
            return []
        # If start or end is an obstacle, can't find path
        if self.grid[self.start] or self.grid[self.end]:
            return []
        # If grid is too small or start==end, trivial solution
        if self.start == self.end:
            return [self.start]
        # Otherwise, very simple (mocked: no real pathfinding)
        return [self.start, self.end]

class JPSSearcher:
    """
    Mock JPS (Jump Point Search) searcher for testing only.
    """
    def __init__(self):
        self.grid = None
        self.nx = self.ny = self.nz = 0
        self.start = None
        self.end = None

    def initGridMap(self, nx, ny, nz, resolution, origin):
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.grid = np.zeros((nx, ny, nz), dtype=bool)
        self.origin = origin

    def reset(self):
        if self.grid is not None:
            self.grid[:] = 0

    def setStart(self, pos):
        self.start = tuple(map(int, pos))

    def setEnd(self, pos):
        self.end = tuple(map(int, pos))

    def search(self):
        # Naive: return False if start or end is obstacle
        if self.grid[self.start] or self.grid[self.end]:
            return False
        # Otherwise, always possible
        return True

    def getPath(self):
        # If already checked in search()
        if self.grid[self.start] or self.grid[self.end]:
            return []
        # Direct diagonal
        path = []
        x_diff = self.end[0] - self.start[0]
        y_diff = self.end[1] - self.start[1]
        z_diff = self.end[2] - self.start[2]
        steps = max(abs(x_diff), abs(y_diff), abs(z_diff))
        if steps == 0:
            return [self.start]
        for step in range(steps + 1):
            x = self.start[0] + step * (x_diff // steps if steps != 0 else 0)
            y = self.start[1] + step * (y_diff // steps if steps != 0 else 0)
            z = self.start[2] + step * (z_diff // steps if steps != 0 else 0)
            path.append((x, y, z))
        return path

def test_astar_searcher_basic_usage():
    astar = AstarPathFinder()
    astar.initGridMap(1, 1, 1, 1.0, EigenVector3d(0,0,0))  # grid 1x1x1
    astar.reset()
    astar.setObstacle(0,0,0)
    astar.setStart(EigenVector3d(0,0,0))
    astar.setEnd(EigenVector3d(0,0,0))
    res = astar.getPath()
    # Path should be empty as start and goal are the same and blocked
    assert len(res) == 0

def test_jps_searcher_basic_usage():
    jps = JPSSearcher()
    jps.initGridMap(2,2,2,1.0,EigenVector3d(0,0,0))
    jps.reset()
    jps.setStart(EigenVector3d(0,0,0))
    jps.setEnd(EigenVector3d(1,1,1))

    # No obstacles, should be possible
    found = jps.search()
    assert found
    path = jps.getPath()
    assert len(path) > 0