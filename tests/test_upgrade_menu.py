import pytest
import pygame
import numpy as np

@pytest.fixture(autouse=True)
def pygame_init_and_quit():
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()

@pytest.fixture
def surface():
    return pygame.Surface((320, 240))

def test_upgrade_menu_renders_options(surface):
    from src.ui import draw_upgrade_menu
    font = pygame.font.Font(None, 32)
    upgrades = {'engine': 1, 'tires': 0, 'seats': 2, 'fare': 1}
    selected = 2
    cheese = 10
    draw_upgrade_menu(surface, font, upgrades, selected, cheese)
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0, 'Upgrade menu did not render any content.'

def test_upgrade_menu_highlights_selected(surface):
    from src.ui import draw_upgrade_menu
    font = pygame.font.Font(None, 32)
    upgrades = {'engine': 1, 'tires': 0, 'seats': 2, 'fare': 1}
    selected = 1
    cheese = 10
    draw_upgrade_menu(surface, font, upgrades, selected, cheese)
    # No assertion for highlight color, but should not error 

def test_upgrade_menu_labels_and_costs(surface):
    from src.ui import draw_upgrade_menu
    font = pygame.font.Font(None, 32)
    upgrades = {'engine': 1, 'tires': 0, 'seats': 2, 'fare': 1}
    selected = 0
    cheese = 10
    draw_upgrade_menu(surface, font, upgrades, selected, cheese)
    # Check that all upgrade options are rendered with clear labels and costs
    # (This is a placeholder: in a real test, OCR or pixel color checks would be used)
    # For now, just ensure no error and surface is not blank
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0

def test_upgrade_menu_retro_palette(surface):
    from src.ui import draw_upgrade_menu
    font = pygame.font.Font(None, 32)
    upgrades = {'engine': 1, 'tires': 0, 'seats': 2, 'fare': 1}
    selected = 0
    cheese = 10
    draw_upgrade_menu(surface, font, upgrades, selected, cheese)
    arr = pygame.surfarray.array3d(surface)
    # Check that the background color matches the retro palette (40, 40, 60)
    assert (arr[0,0] == [40, 40, 60]).all(), 'Upgrade menu background is not retro palette.'

def test_upgrade_menu_accessibility_contrast(surface):
    from src.ui import draw_upgrade_menu
    font = pygame.font.Font(None, 32)
    upgrades = {'engine': 1, 'tires': 0, 'seats': 2, 'fare': 1}
    selected = 0
    cheese = 10
    draw_upgrade_menu(surface, font, upgrades, selected, cheese)
    arr = pygame.surfarray.array3d(surface)
    # Check that text is not the same color as background (simple contrast check)
    assert not (arr == [40, 40, 60]).all(), 'Text is not visible (contrast issue).'

def test_upgrade_menu_mouse_navigation_placeholder(surface):
    # Placeholder for future mouse navigation test
    assert True 

def test_upgrade_menu_tooltip_description(surface):
    from src.ui import draw_upgrade_menu
    font = pygame.font.Font(None, 32)
    upgrades = {'engine': 1, 'tires': 0, 'seats': 2, 'fare': 1}
    selected = 0  # engine
    cheese = 10
    draw_upgrade_menu(surface, font, upgrades, selected, cheese)
    arr = pygame.surfarray.array3d(surface)
    # The description is rendered at (30, 230) in color (180, 220, 255)
    # Check for presence of this color in the region where the description should be
    desc_color = np.array([180, 220, 255])
    region = arr[30:290, 220:240, :]
    # Allow for some tolerance in color matching
    matches = np.isclose(region, desc_color[None, None, :], atol=20).all(axis=2)
    assert matches.sum() > 10, 'Tooltip/description for selected upgrade not rendered.'

def test_upgrade_menu_icons(surface):
    from src.ui import draw_upgrade_menu
    font = pygame.font.Font(None, 32)
    upgrades = {'engine': 1, 'tires': 0, 'seats': 2, 'fare': 1}
    selected = 0
    cheese = 10
    draw_upgrade_menu(surface, font, upgrades, selected, cheese)
    arr = pygame.surfarray.array3d(surface)
    icon_colors = {
        'engine': [255, 80, 80],
        'tires': [80, 255, 80],
        'seats': [80, 80, 255],
        'fare': [255, 220, 40]
    }
    for i, opt in enumerate(['engine', 'tires', 'seats', 'fare']):
        color = np.array(icon_colors[opt])
        # Icon is at (10, 70 + i*40) with size 16x16
        region = arr[10:26, 70 + i*40:70 + i*40 + 16, :]
        matches = np.isclose(region, color[None, None, :], atol=10).all(axis=2)
        assert matches.sum() > 50, f'Icon for {opt} not rendered.'

def test_upgrade_menu_mouse_navigation(surface):
    from src.ui import handle_upgrade_menu_mouse
    upgrade_options = ['engine', 'tires', 'seats', 'fare']
    # Simulate a mouse click at the center of the second option (tires)
    mouse_pos = (20, 70 + 1 * 40 + 8)  # x=20, y=center of second option
    mouse_click = True
    selected = handle_upgrade_menu_mouse(mouse_pos, mouse_click, upgrade_options)
    assert selected == 1, 'Mouse navigation did not select the correct upgrade option.'

def test_upgrade_menu_visual_feedback(surface):
    from src.ui import draw_upgrade_menu
    font = pygame.font.Font(None, 32)
    upgrades = {'engine': 1, 'tires': 0, 'seats': 2, 'fare': 1}
    selected = 2  # seats
    cheese = 10
    draw_upgrade_menu(surface, font, upgrades, selected, cheese)
    arr = pygame.surfarray.array3d(surface)
    # The label for the selected option is rendered at (30, 70 + 2*40)
    # Check for the highlight color (255, 255, 0) in this region
    region = arr[30:200, 150:190, :]
    highlight_color = np.array([255, 255, 0])
    matches = np.isclose(region, highlight_color[None, None, :], atol=10).all(axis=2)
    assert matches.sum() > 10, 'Visual feedback (highlight) for selected upgrade not rendered.' 