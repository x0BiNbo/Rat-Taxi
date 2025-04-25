import pytest
import importlib
 
def test_game_initialization():
    # Test that the main function exists in src.main
    main_module = importlib.import_module('src.main')
    assert hasattr(main_module, 'main'), 'main() function not found in src.main.' 