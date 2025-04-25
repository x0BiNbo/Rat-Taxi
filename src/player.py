class Player:
    def __init__(self, city_width=20, city_height=15, spawn_pos=None):
        if spawn_pos is not None:
            self.x, self.y = spawn_pos
        else:
            self.x = city_width // 2
            self.y = city_height // 2
        self.fx = float(self.x)
        self.fy = float(self.y)
        self.city_width = city_width
        self.city_height = city_height
        self.engine_level = 0
        self.tires_level = 0
        self.seats_level = 0
        self.fare_level = 0

    def move(self, dx, dy):
        # Smooth movement: update float position
        self.fx += dx
        self.fy += dy
        # Map wrapping
        self.fx = self.fx % self.city_width
        self.fy = self.fy % self.city_height
        # Sync int position for grid logic
        self.x = int(round(self.fx)) % self.city_width
        self.y = int(round(self.fy)) % self.city_height

    def get_position(self):
        return self.x, self.y

    def get_float_position(self):
        return self.fx, self.fy 