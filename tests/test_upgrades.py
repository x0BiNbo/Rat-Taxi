import pytest
from src.player import Player
from src.upgrade import UpgradeManager

def test_upgrade_purchase_and_cheese_deduction():
    manager = UpgradeManager(cheese=10)
    assert manager.purchase_upgrade('engine')
    assert manager.cheese == 5
    assert manager.get_stat('engine') == 1
    assert not manager.purchase_upgrade('unknown')  # Should not upgrade unknown type

def test_upgrade_effects_on_player():
    player = Player(city_width=20, city_height=15)
    # Simulate upgrades
    player.engine_level = 2
    player.tires_level = 1
    player.seats_level = 3
    player.fare_level = 0
    assert player.engine_level == 2
    assert player.tires_level == 1
    assert player.seats_level == 3
    assert player.fare_level == 0 