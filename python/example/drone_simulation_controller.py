class DroneSimulationController:
    def __init__(self):
        self.command: Command = Idle()

    def take_off(self):
        self.command = TakeOff()


class Command:
    pass


class Idle(Command):
    pass


class TakeOff(Command):
    pass