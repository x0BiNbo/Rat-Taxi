import pytest
import importlib

def test_fare_spawning():
    fare_module = importlib.import_module('src.fare')
    Fare = getattr(fare_module, 'Fare')
    fare = Fare(city_width=20, city_height=15)
    assert 0 <= fare.pickup[0] < 20 and 0 <= fare.pickup[1] < 15
    assert 0 <= fare.dropoff[0] < 20 and 0 <= fare.dropoff[1] < 15
    assert fare.pickup != fare.dropoff

def test_fare_completion():
    fare_module = importlib.import_module('src.fare')
    Fare = getattr(fare_module, 'Fare')
    fare = Fare(city_width=20, city_height=15)
    # Simulate picking up and dropping off
    assert fare.at_pickup(fare.pickup)
    fare.pick_up()
    assert fare.picked_up
    assert fare.at_dropoff(fare.dropoff) 