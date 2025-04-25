import random

class City:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        # 0 = vertical road, 1 = horizontal road, 2 = cross/intersection, 3 = sidewalk
        # 4 = building.svg, 41 = building1.svg, 42 = building2.svg
        # 5 = road_corner_tl, 6 = road_corner_tr, 7 = road_corner_bl, 8 = road_corner_br
        # 9 = grass, 10 = dirt
        v_roads = [width // 3, 2 * width // 3]
        h_roads = [height // 3, 2 * height // 3]
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                is_v = x in v_roads
                is_h = y in h_roads
                if is_v and is_h:
                    self.grid[y][x] = 2  # cross/intersection
                elif is_v:
                    if y == 0:
                        self.grid[y][x] = 5
                    elif y == height - 1:
                        self.grid[y][x] = 7
                    else:
                        self.grid[y][x] = 0  # vertical road
                elif is_h:
                    if x == 0:
                        self.grid[y][x] = 5
                    elif x == width - 1:
                        self.grid[y][x] = 6
                    else:
                        self.grid[y][x] = 1  # horizontal road
                else:
                    r = random.random()
                    if r < 0.08:
                        self.grid[y][x] = 41  # building1.svg
                    elif r < 0.16:
                        self.grid[y][x] = 42  # building2.svg
                    elif r < 0.25:
                        self.grid[y][x] = 4   # building.svg
                    else:
                        self.grid[y][x] = None  # undecided, will fill later
        # Pass 2: Place sidewalks contextually (only if adjacent to road/building)
        for y in range(height):
            for x in range(width):
                if self.grid[y][x] is None:
                    if self._adjacent_to_road_or_building(x, y):
                        self.grid[y][x] = 3  # sidewalk
        # Pass 3: Fill remaining with grass/dirt (only if not adjacent to road/building/sidewalk)
        for y in range(height):
            for x in range(width):
                if self.grid[y][x] is None:
                    if not self._adjacent_to_any(x, y, {0,1,2,3,4,5,6,7,8,41,42}):
                        self.grid[y][x] = 9 if random.random() < 0.7 else 10
                    else:
                        self.grid[y][x] = 3  # fallback to sidewalk if surrounded

    def _adjacent_to_road_or_building(self, x, y):
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.grid[ny][nx] in (0,1,2,4,5,6,7,8,41,42):
                    return True
        return False

    def _adjacent_to_any(self, x, y, tile_types):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny][nx] in tile_types:
                        return True
        return False

    def get_grid(self):
        return self.grid

    def is_driveable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] in (0, 1, 2, 5, 6, 7, 8)
        return False 