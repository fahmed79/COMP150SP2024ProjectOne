import random


class Statistic:
    def __init__(self, legacy_points: int):
        self.value = self._generate_starting_value(legacy_points)
        self.description = None
        self.min_value = 0
        self.max_value = 100

    def __str__(self):
        return f"{self.value}"

    def increase(self, amount):
        self.value += amount
        if self.value > self.max_value:
            self.value = self.max_value

    def decrease(self, amount):
        self.value -= amount
        if self.value < self.min_value:
            self.value = self.min_value

    def _generate_starting_value(self, legacy_points: int):
        """Generate a starting value for the statistic based on random number and user properties."""
        """This is just a placeholder for now. Perhaps some statistics will be based on user properties, and others 
        will be random."""
        return legacy_points / 100 + random.randint(1, 3)


class Strength(Statistic):

    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Strength is a measure of physical power."

class Dexterity(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Dexterity measures the speed and agility of a character."

class Constitution(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Constitution represents the body's natural armor and resilience."

class Vitality(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Vitality is an indirect measure of age and represents a character's hit points."

class Endurance(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Endurance determines how quickly a character recovers from injuries and fatigue."

class Intelligence(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Intelligence measures a character's ability to solve problems and think quickly."

class Wisdom(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Wisdom affects a character's ability to make effective choices under pressure."

class Knowledge(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Knowledge represents a character's overall knowledge, with potential bonuses or deficits in specific areas."

class Willpower(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Willpower measures a character's ability to overcome natural urges and resist mind control."

class Spirit(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Spirit is a catchall for the ability to perform otherworldly acts, with different skills using different resource pools."

class Capacity(Statistic):
    def __init__(self, legacy_points: int):
        super().__init__(legacy_points)
        self.description = "Capacity represents specific abilities or pools of resources like mana, stamina, or HP."


# and so on for the other statistics
