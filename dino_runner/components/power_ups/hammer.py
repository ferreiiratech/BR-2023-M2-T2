from dino_runner.utils.constants import FIRE_BALL, HAMMER_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Hammer(PowerUp):
    def __init__(self):
        self.image = FIRE_BALL
        self.type = HAMMER_TYPE
        super().__init__(self.image, self.type)