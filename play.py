import numpy as np
import matplotlib.pyplot as plt

from src.parking_lot import ParkingLot
from src.on_ramp import OnRamp
from src.lane import Lane

lot = ParkingLot()
lane = Lane(length=20, next=lot, p_slow=0)
ramp = OnRamp(next=lane)

for _ in range(10):
    ramp.step()
    lane.step()


# plt.imshow(np.vstack(lane.hist))
# plt.show()

lane.space_time_plot()
