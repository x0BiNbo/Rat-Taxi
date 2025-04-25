import pytest
import importlib

def test_player_movement():
    player_module = importlib.import_module('src.player')
    Player = getattr(player_module, 'Player')
    player = Player(city_width=20, city_height=15)
    x0, y0 = player.get_position()
    player.move(1, 0)
    x1, y1 = player.get_position()
    assert x1 == (x0 + 1) % 20 and y1 == y0, 'Player should move right (with wrapping).'
    player.move(-1, 0)
    x2, y2 = player.get_position()
    assert x2 == x1 - 1 or (x1 == 0 and x2 == 19), 'Player should move left (with wrapping).'
    player.move(0, 1)
    x3, y3 = player.get_position()
    assert x3 == x2 and y3 == (y2 + 1) % 15, 'Player should move down (with wrapping).'
    player.move(0, -1)
    x4, y4 = player.get_position()
    assert x4 == x3 and (y4 == y3 - 1 or (y3 == 0 and y4 == 14)), 'Player should move up (with wrapping).'
    # Test wrapping
    for _ in range(100):
        player.move(-1, 0)
    x_min, _ = player.get_position()
    assert x_min == (x0 - 100) % 20, 'Player should wrap horizontally.'
    for _ in range(100):
        player.move(1, 0)
    x_max, _ = player.get_position()
    assert x_max == (x_min + 100) % 20, 'Player should wrap horizontally.' 