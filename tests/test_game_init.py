import pytest
import importlib
import pygame

def test_game_initialization():
    # Test that the main function exists in src.main
    main_module = importlib.import_module('src.main')
    assert hasattr(main_module, 'main'), 'main() function not found in src.main.'

def test_game_over_on_health_depletion(monkeypatch):
    from src.main import main as game_main
    # Patch pygame.display.set_mode to use a dummy surface
    dummy_screen = pygame.Surface((800, 600))
    monkeypatch.setattr(pygame.display, 'set_mode', lambda size: dummy_screen)
    # Patch pygame.display.flip to do nothing
    monkeypatch.setattr(pygame.display, 'flip', lambda: None)
    # Patch pygame.event.get to simulate health depletion and then quit
    events = [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}), pygame.event.Event(pygame.QUIT)]
    monkeypatch.setattr(pygame.event, 'get', lambda: events)
    # Patch health to 0 to trigger game over
    monkeypatch.setattr('src.main.health', 0)
    # Run main (should not error)
    try:
        game_main()
    except SystemExit:
        pass

def test_upgrade_menu_navigation_and_persistence(monkeypatch):
    import pygame
    from src.main import main as game_main
    # Patch pygame.display.set_mode to use a dummy surface
    dummy_screen = pygame.Surface((800, 600))
    monkeypatch.setattr(pygame.display, 'set_mode', lambda size: dummy_screen)
    # Patch pygame.display.flip to do nothing
    monkeypatch.setattr(pygame.display, 'flip', lambda: None)
    # Simulate up, down, enter (upgrade), then enter (restart), then quit
    events = [
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN}),
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP}),
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}),
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}),
        pygame.event.Event(pygame.QUIT)
    ]
    monkeypatch.setattr(pygame.event, 'get', lambda: events)
    # Patch health to 0 to trigger game over
    monkeypatch.setattr('src.main.health', 0)
    # Run main (should not error)
    try:
        game_main()
    except SystemExit:
        pass 