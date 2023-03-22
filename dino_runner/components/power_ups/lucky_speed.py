from dino_runner.utils.constants import HEART, SPEED_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


# Criei o lucky_speed
class Lucky_speed(PowerUp):
    def __init__(self):
        self.image = HEART
        self.type = SPEED_TYPE
        super().__init__(self.image, self.type)