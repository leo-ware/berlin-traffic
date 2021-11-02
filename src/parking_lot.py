from src.abstract_asphalt import AbstractAsphalt


class ParkingLot(AbstractAsphalt):
    def __init__(self):
        super().__init__()
        self.n_cars = 0

    def step(self):
        pass

    def push(self, positions, _):
        self.n_cars += len(positions)
