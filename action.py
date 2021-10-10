class Action:
    pass

class EscapeAction(Action):
    pass

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx, self.dy = dx, dy