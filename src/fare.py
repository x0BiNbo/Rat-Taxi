import random

class Fare:
    def __init__(self, city_width=20, city_height=15, city_grid=None, special=False, bonus=0, used_tiles=None):
        self.city_width = city_width
        self.city_height = city_height
        # Use city_grid to find all road tiles
        if city_grid is not None:
            road_tiles = [(x, y) for y in range(city_height) for x in range(city_width) if city_grid[y][x] == 0]
        else:
            road_tiles = [(x, y) for y in range(city_height) for x in range(city_width)]
        if used_tiles is None:
            used_tiles = set()
        available = [t for t in road_tiles if t not in used_tiles]
        self.pickup = random.choice(available)
        used_tiles.add(self.pickup)
        available = [t for t in road_tiles if t not in used_tiles]
        self.dropoff = random.choice(available)
        used_tiles.add(self.dropoff)
        self.picked_up = False
        self.special = special
        self.bonus = bonus

    def at_pickup(self, pos):
        return pos == self.pickup and not self.picked_up

    def at_dropoff(self, pos):
        return pos == self.dropoff and self.picked_up

    def pick_up(self):
        self.picked_up = True

class FareManager:
    def __init__(self, city_width=20, city_height=15, city_grid=None, max_fares=3):
        self.city_width = city_width
        self.city_height = city_height
        self.city_grid = city_grid
        self.max_fares = max_fares
        self.fares = []
        self.generate_fares()

    def generate_fares(self):
        self.fares = []
        used_tiles = set()
        for i in range(self.max_fares):
            # 1 in 4 chance for a special fare
            special = random.random() < 0.25
            bonus = random.randint(2, 5) if special else 0
            fare = Fare(self.city_width, self.city_height, self.city_grid, special, bonus, used_tiles)
            self.fares.append(fare)

    def get_active_fares(self):
        return [fare for fare in self.fares if not fare.picked_up or not fare.at_dropoff(fare.dropoff)]

    def pick_up_fare(self, pos):
        for fare in self.fares:
            if fare.at_pickup(pos):
                fare.pick_up()
                return fare
        return None

    def dropoff_fare(self, pos):
        for fare in self.fares:
            if fare.at_dropoff(pos):
                return fare
        return None 