import random
from datetime import datetime, timedelta


class LifeEngine:
    def __init__(self, player):
        self.player = player

    def advance_day(self):
        self.player["day"] += 1

        if self.player["day"] > 30:
            self.player["day"] = 1
            self.player["month"] += 1

        if self.player["month"] > 12:
            self.player["month"] = 1
            self.player["year"] += 1
            self.player["age"] += 1

        self.process_daily_effects()
        self.process_random_events()

        return self.player

    def process_daily_effects(self):
        energy_loss = random.randint(1, 10)
        self.player["energy"] = max(0, self.player["energy"] - energy_loss)

        if self.player["career"] == "fighter":
            self.player["discipline"] += random.randint(0, 2)

        if self.player["money"] < 0:
            self.player["stress"] += 2

    def process_random_events(self):
        event_roll = random.randint(1, 100)

        if event_roll <= 10:
            self.player["stress"] += 5

        elif event_roll <= 20:
            self.player["money"] += random.randint(100, 1000)

        elif event_roll <= 25:
            self.player["injured"] = True

        elif event_roll <= 30:
            self.player["fame"] += random.randint(1, 5)

    def train(self):
        self.player["strength"] += random.randint(1, 3)
        self.player["skill"] += random.randint(1, 3)
        self.player["energy"] = max(0, self.player["energy"] - 15)

        return {
            "message": "Training completed.",
            "player": self.player
        }

    def work_job(self):
        income = random.randint(50, 300)
        self.player["money"] += income
        self.player["energy"] = max(0, self.player["energy"] - 10)

        return {
            "message": f"You earned ${income}",
            "player": self.player
        }
