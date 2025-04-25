import pytest

from src.player import Player
from src.subway import Subway

def test_subway_entry_and_exit():
    subway = Subway(stations=[(2, 2), (10, 10)])
    player = Player(city_width=20, city_height=15)
    player.x, player.y = 2, 2
    assert subway.at_station((player.x, player.y))
    subway.enter(player)
    assert subway.in_subway
    subway.exit(player, (10, 10))
    assert not subway.in_subway
    assert (player.x, player.y) == (10, 10)

def test_subway_fast_travel():
    subway = Subway(stations=[(2, 2), (10, 10), (5, 5)])
    player = Player(city_width=20, city_height=15)
    player.x, player.y = 5, 5
    subway.enter(player)
    subway.exit(player, (2, 2))
    assert (player.x, player.y) == (2, 2) 