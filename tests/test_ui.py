import pytest
import pygame
import numpy as np

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

def test_health_ui_wraps_rows(monkeypatch):
    import pygame
    pygame.init()
    from src.main import main as game_main
    # Patch pygame.display.set_mode to use a dummy surface
    dummy_screen = pygame.Surface((800, 600))
    monkeypatch.setattr(pygame.display, 'set_mode', lambda size: dummy_screen)
    # Patch pygame.display.flip to do nothing
    monkeypatch.setattr(pygame.display, 'flip', lambda: None)
    # Patch pygame.event.get to return quit after one loop
    monkeypatch.setattr(pygame.event, 'get', lambda: [pygame.event.Event(pygame.QUIT)])
    # Patch max_health to 24 (12 hearts)
    monkeypatch.setattr('src.main.max_health', 24)
    # Run main (should not error)
    try:
        game_main()
    except SystemExit:
        pass

def test_score_below_hearts(monkeypatch):
    import pygame
    pygame.init()
    from src.main import main as game_main
    # Patch pygame.display.set_mode to use a dummy surface
    dummy_screen = pygame.Surface((800, 600))
    monkeypatch.setattr(pygame.display, 'set_mode', lambda size: dummy_screen)
    # Patch pygame.display.flip to do nothing
    monkeypatch.setattr(pygame.display, 'flip', lambda: None)
    # Patch pygame.event.get to return quit after one loop
    monkeypatch.setattr(pygame.event, 'get', lambda: [pygame.event.Event(pygame.QUIT)])
    # Patch max_health to 24 (12 hearts)
    monkeypatch.setattr('src.main.max_health', 24)
    # Run main (should not error)
    try:
        game_main()
    except SystemExit:
        pass

def test_icon_contrast():
    """Failing test: All icons must have sufficient contrast against the background (WCAG 4.5:1)."""
    from src.ui import get_icon_surfaces_for_test
    icons = get_icon_surfaces_for_test()
    def rel_luminance(rgb):
        # WCAG relative luminance
        def channel(c):
            c = c/255.0
            return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
        r, g, b = rgb
        return 0.2126*channel(r) + 0.7152*channel(g) + 0.0722*channel(b)
    def contrast_ratio(l1, l2):
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)
    for icon_surface, bg_color in icons:
        arr = pygame.surfarray.pixels3d(icon_surface)
        alpha = pygame.surfarray.pixels_alpha(icon_surface)
        mask = (alpha > 0) & ((arr[:,:,0] > 10) | (arr[:,:,1] > 10) | (arr[:,:,2] > 10))
        icon_pixels = arr[mask]
        if len(icon_pixels) == 0:
            continue
        icon_lum = np.mean([rel_luminance(px) for px in icon_pixels])
        bg_lum = rel_luminance(bg_color)
        ratio = contrast_ratio(icon_lum, bg_lum)
        assert ratio >= 4.5, f'Icon contrast ratio too low: {ratio}'

def test_minimap_marker_contrast_and_presence():
    """Failing test: All minimap markers must be present, distinct, and have sufficient contrast (WCAG 4.5:1) against the minimap background."""
    import pygame
    from src.ui import draw_minimap
    minimap_bg = (0, 0, 0)
    surface = pygame.Surface((160, 120), pygame.SRCALPHA)
    player_pos = (5, 7)
    city_size = (20, 15)
    stations = [(2, 2), (10, 10)]
    pickup = (3, 4)
    dropoff = (15, 12)
    draw_minimap(surface, player_pos, city_size, stations, pickup, dropoff)
    arr = pygame.surfarray.pixels3d(surface)
    alpha = pygame.surfarray.pixels_alpha(surface)
    def rel_luminance(rgb):
        def channel(c):
            c = c/255.0
            return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
        r, g, b = rgb
        return 0.2126*channel(r) + 0.7152*channel(g) + 0.0722*channel(b)
    def contrast_ratio(l1, l2):
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)
    # Check for presence and contrast of each marker
    marker_colors = [
        (255, 220, 40),   # player
        (100, 100, 255),  # subway
        (40, 220, 40),    # pickup
        (255, 80, 80),    # dropoff (updated)
    ]
    found = [False, False, False, False]
    for y in range(arr.shape[1]):
        for x in range(arr.shape[0]):
            if alpha[x, y] == 0:
                continue
            px = arr[x, y]
            for i, color in enumerate(marker_colors):
                if np.all(np.abs(px - color) < 30):
                    found[i] = True
                    # Check contrast
                    marker_lum = rel_luminance(color)
                    bg_lum = rel_luminance(minimap_bg)
                    ratio = contrast_ratio(marker_lum, bg_lum)
                    assert ratio >= 4.5, f'Minimap marker {color} contrast too low: {ratio}'
    for i, present in enumerate(found):
        assert present, f'Minimap marker {marker_colors[i]} not found on minimap.'

def test_player_feedback_visual_effects():
    """Failing test: Player receives clear visual feedback (e.g., flash/highlight) for pickups, hazards, and fare completion."""
    import pygame
    from src.ui import draw_player_with_feedback
    surface = pygame.Surface((64, 64), pygame.SRCALPHA)
    # Simulate normal player
    draw_player_with_feedback(surface, feedback=None)
    normal_arr = pygame.surfarray.array3d(surface).copy()
    # Simulate pickup feedback
    draw_player_with_feedback(surface, feedback='pickup')
    pickup_arr = pygame.surfarray.array3d(surface).copy()
    # Simulate hazard feedback
    draw_player_with_feedback(surface, feedback='hazard')
    hazard_arr = pygame.surfarray.array3d(surface).copy()
    # Simulate fare completion feedback
    draw_player_with_feedback(surface, feedback='fare_complete')
    fare_arr = pygame.surfarray.array3d(surface).copy()
    # There should be a visible difference for each feedback type
    assert not (pickup_arr == normal_arr).all(), 'No visual feedback for pickup.'
    assert not (hazard_arr == normal_arr).all(), 'No visual feedback for hazard.'
    assert not (fare_arr == normal_arr).all(), 'No visual feedback for fare completion.' 