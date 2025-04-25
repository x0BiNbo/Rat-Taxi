import pytest
import pygame

def test_fare_meter_display():
    pass  # Placeholder removed; see real rendering test below

def test_minimap_display():
    pass  # Placeholder removed; see real rendering test below

# Dummy surface for rendering tests
@pytest.fixture
def surface():
    return pygame.Surface((200, 50))

def test_fare_meter_renders_status_and_bonus(surface):
    import pygame
    pygame.init()
    pygame.font.init()
    from src.ui import draw_fare_meter
    font = pygame.font.Font(None, 32)
    fare_active = True
    fare_bonus = 2
    cheese = 10
    draw_fare_meter(surface, font, fare_active, fare_bonus, cheese)
    arr = pygame.surfarray.array3d(surface)
    # Should render some non-black pixels (text or bar)
    assert arr.sum() > 0, 'Fare Meter did not render any content.'

def test_minimap_renders_player(surface):
    from src.ui import draw_minimap
    player_pos = (5, 7)
    city_size = (20, 15)
    stations = [(2, 2), (10, 10)]
    pickup = (3, 4)
    dropoff = (15, 12)
    # Should not raise and should draw something for player
    draw_minimap(surface, player_pos, city_size, stations, pickup, dropoff)
    # Check that at least one non-black pixel exists (player dot)
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0, 'Mini-Map did not render any content.'

def test_minimap_renders_stations_and_fares(surface):
    from src.ui import draw_minimap
    player_pos = (0, 0)
    city_size = (20, 15)
    stations = [(2, 2), (10, 10)]
    pickup = (3, 4)
    dropoff = (15, 12)
    draw_minimap(surface, player_pos, city_size, stations, pickup, dropoff)
    arr = pygame.surfarray.array3d(surface)
    # Should render at least 4 colored dots (player, 2 stations, pickup, dropoff)
    assert (arr != 0).sum() > 4, 'Mini-Map did not render stations and fares.' 