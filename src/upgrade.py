class UpgradeManager:
    VALID_UPGRADES = {'engine', 'tires', 'seats', 'fare'}
    def __init__(self, cheese):
        self.cheese = cheese
        self.engine_level = 0
        self.tires_level = 0
        self.seats_level = 0
        self.fare_level = 0

    def purchase_upgrade(self, upgrade_type):
        if upgrade_type not in self.VALID_UPGRADES:
            return False
        if self.cheese < 5:
            return False
        self.cheese -= 5
        if upgrade_type == 'engine':
            self.engine_level += 1
        elif upgrade_type == 'tires':
            self.tires_level += 1
        elif upgrade_type == 'seats':
            self.seats_level += 1
        elif upgrade_type == 'fare':
            self.fare_level += 1
        return True

    def get_stat(self, upgrade_type):
        if upgrade_type == 'engine':
            return self.engine_level
        elif upgrade_type == 'tires':
            return self.tires_level
        elif upgrade_type == 'seats':
            return self.seats_level
        elif upgrade_type == 'fare':
            return self.fare_level
        return 0 