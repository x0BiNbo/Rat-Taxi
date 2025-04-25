import pytest
from src.upgrade import UpgradeManager

def test_cheese_currency():
    upgrades = UpgradeManager(cheese=10)
    assert upgrades.cheese == 10
    result = upgrades.purchase_upgrade('engine')
    assert result is True
    assert upgrades.cheese == 5, 'Cheese should be deducted by 5 after purchase.'
    result2 = upgrades.purchase_upgrade('engine')
    assert result2 is True
    assert upgrades.cheese == 0, 'Cheese should be 0 after two purchases.'
    result3 = upgrades.purchase_upgrade('engine')
    assert result3 is False, 'Should not be able to purchase with insufficient cheese.'
    assert upgrades.cheese == 0

def test_upgrade_purchase():
    upgrades = UpgradeManager(cheese=5)
    assert upgrades.engine_level == 0
    result = upgrades.purchase_upgrade('engine')
    assert result is True
    assert upgrades.engine_level == 1
    assert upgrades.cheese == 0
    # Try invalid upgrade
    result2 = upgrades.purchase_upgrade('invalid')
    assert result2 is False
    assert upgrades.engine_level == 1 