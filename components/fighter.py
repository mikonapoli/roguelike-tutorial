import color
from components.base_component import BaseComponent

from input_handlers import GameOverEventHandler

from render_order import RenderOrder

class Fighter(BaseComponent):
    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power
    
    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.entity.ai:
            self.die()
    
    def die(self) -> None:
        msg = f"{self.entity.name} is dead"
        msg_color = color.ENEMY_DIE
        if self.engine.player is self.entity:
            msg = "You died!"
            msg_color = color.PLAYER_DIE
            self.engine.event_handler = GameOverEventHandler(self.engine)

        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.render_order = RenderOrder.CORPSE
        self.entity.name = f"Remains of {self.entity.name}"
        self.engine.message_log.add_message(msg, msg_color)
        