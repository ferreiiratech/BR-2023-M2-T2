from dino_runner.utils.constants import PORTAL, PORTAL_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Portal_speed(PowerUp):
    def __init__(self):
        self.image = PORTAL
        self.type = PORTAL_TYPE
        super().__init__(self.image, self.type)