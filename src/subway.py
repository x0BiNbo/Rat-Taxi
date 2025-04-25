import time

class Subway:
    def __init__(self, stations, cooldown=5.0):
        self.stations = stations
        self.in_subway = False
        self.cooldown = cooldown
        self.last_used = 0.0
        self.animating = False
        self.animation_ticks = 0
        self.animation_duration = 20  # frames

    def at_station(self, pos):
        return pos in self.stations

    def can_use(self):
        return (time.time() - self.last_used) >= self.cooldown and not self.animating

    def enter(self, player):
        if self.at_station((player.x, player.y)) and self.can_use():
            self.in_subway = True
            self.animating = True
            self.animation_ticks = self.animation_duration

    def update_animation(self):
        if self.animating:
            self.animation_ticks -= 1
            if self.animation_ticks <= 0:
                self.animating = False

    def exit(self, player, station):
        if self.in_subway and station in self.stations:
            player.x, player.y = station
            self.in_subway = False
            self.last_used = time.time() 