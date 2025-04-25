import pytest
import importlib

def test_city_generation():
    city_module = importlib.import_module('src.city')
    City = getattr(city_module, 'City')
    city = City()
    grid = city.get_grid()
    assert len(grid) == 15, 'City grid should have 15 rows.'
    assert all(len(row) == 20 for row in grid), 'Each row should have 20 columns.' 