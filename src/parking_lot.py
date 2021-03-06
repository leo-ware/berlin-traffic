from src.abstract_asphalt import AbstractAsphalt


class ParkingLot(AbstractAsphalt):
    def __init__(self):
        super().__init__()
        self.n_parked_cars = 0

    def step(self):
        pass

    def push(self, positions, _):
        self.n_parked_cars += len(positions)

    def space_available(self) -> bool:
        return True
