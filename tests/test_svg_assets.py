import pytest
import pygame
import io
from pathlib import Path

@pytest.fixture(autouse=True)
def pygame_init_and_quit():
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()

@pytest.fixture
def surface():
    return pygame.Surface((32, 32))

def test_load_and_render_player_svg(surface):
    from src.ui import load_and_render_svg
    svg_path = Path('assets/svg/player.svg')
    load_and_render_svg(svg_path, surface)
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0, 'Player SVG did not render any content.'

def test_load_and_render_customer_svg(surface):
    from src.ui import load_and_render_svg
    svg_path = Path('assets/svg/customer.svg')
    load_and_render_svg(svg_path, surface)
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0, 'Customer SVG did not render any content.'

def test_load_and_render_subway_svg(surface):
    from src.ui import load_and_render_svg
    svg_path = Path('assets/svg/subway.svg')
    load_and_render_svg(svg_path, surface)
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0, 'Subway SVG did not render any content.'

def test_load_and_render_prop_svg(surface):
    from src.ui import load_and_render_svg
    svg_path = Path('assets/svg/prop.svg')
    load_and_render_svg(svg_path, surface)
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0, 'Prop SVG did not render any content.'

def test_load_and_render_environment_svg(surface):
    from src.ui import load_and_render_svg
    svg_path = Path('assets/svg/environment.svg')
    load_and_render_svg(svg_path, surface)
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0, 'Environment SVG did not render any content.'

def test_svg_asset_fallback_missing(surface):
    from src.ui import load_and_render_svg
    from pathlib import Path
    # Use a non-existent SVG path
    svg_path = Path('assets/svg/does_not_exist.svg')
    try:
        load_and_render_svg(svg_path, surface)
    except Exception:
        pass  # Acceptable for now
    arr = pygame.surfarray.array3d(surface)
    # Should render a fallback (not blank)
    assert arr.sum() > 0, 'Fallback asset not rendered for missing SVG.'

def test_svg_asset_fallback_corrupt(surface):
    from src.ui import load_and_render_svg
    from pathlib import Path
    # Create a corrupt SVG file
    corrupt_path = Path('assets/svg/corrupt.svg')
    with open(corrupt_path, 'w') as f:
        f.write('<svg><notvalid></svg>')
    try:
        load_and_render_svg(corrupt_path, surface)
    except Exception:
        pass  # Acceptable for now
    arr = pygame.surfarray.array3d(surface)
    # Should render a fallback (not blank)
    assert arr.sum() > 0, 'Fallback asset not rendered for corrupt SVG.'
    corrupt_path.unlink()

def test_svg_asset_scaling(surface):
    from src.ui import load_and_render_svg
    from pathlib import Path
    svg_path = Path('assets/svg/player.svg')
    # Render at a different size
    big_surface = pygame.Surface((64, 64))
    load_and_render_svg(svg_path, big_surface)
    arr = pygame.surfarray.array3d(big_surface)
    assert arr.sum() > 0, 'SVG did not scale and render at larger size.'

def test_city_tile_asset_mapping(surface):
    """
    For each city grid tile type (sidewalk and building variants), ensure the correct SVG asset is mapped and renders without error.
    """
    from src.ui import load_and_render_svg
    tile_asset_map = {
        3: [
            'assets/svg/sidewalk.svg',
            'assets/svg/sidewalk_t.svg',
            'assets/svg/sidewalk_corner.svg',
            'assets/svg/sidewalk_straight.svg',
            'assets/svg/sidewalk_end.svg',
        ],
        4: ['assets/svg/building.svg'],
        41: ['assets/svg/building1.svg'],
        42: ['assets/svg/building2.svg'],
    }
    for tile_type, asset_list in tile_asset_map.items():
        for asset in asset_list:
            try:
                load_and_render_svg(asset, surface)
                arr = pygame.surfarray.array3d(surface)
                assert arr.sum() > 0, f'Asset {asset} for tile type {tile_type} did not render any content.'
            except Exception as e:
                assert False, f'Error rendering asset {asset} for tile type {tile_type}: {e}'

def test_load_and_render_fare_pickup_svg(surface):
    from src.ui import load_and_render_svg
    svg_path = Path('assets/svg/fare_pickup.svg')
    load_and_render_svg(svg_path, surface)
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0, 'Fare pickup SVG did not render any content.'

def test_load_and_render_fare_dropoff_svg(surface):
    from src.ui import load_and_render_svg
    svg_path = Path('assets/svg/fare_dropoff.svg')
    load_and_render_svg(svg_path, surface)
    arr = pygame.surfarray.array3d(surface)
    assert arr.sum() > 0, 'Fare dropoff SVG did not render any content.' 