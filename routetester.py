from spacetrackservice import SatelliteTrackService
from station import Station
from datetime import datetime, timedelta
from lineofsightlibrary import do_routing
from timekeeper import TimeKeeper
import csv


sats = SatelliteTrackService.get_satellite_data()
uccs = Station('uccs', 38.893601, -104.800619, 0, size=20)
johann = Station('johann', -26.2041, 28.0473, 0, size=20)

time = datetime.now()
timekeeper = TimeKeeper(time)
with open('results-only-distance.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Hops', 'Time to Compute', 'Traveled', 'Ping'])
for i in range(10000):
    print('Testing with time={}'.format(timekeeper.get_time()))
    start = datetime.now()
    root = do_routing(uccs, johann, sats, timekeeper.get_time())
    node = root.root
    stop = datetime.now()
    hops = 0
    dist = 0
    while node.data is not johann:
        if node.child.data is johann:
            dist = node.child.distance
            pass
        else:
            hops = hops + 1
        node = node.child
    ping = dist / 299792456 * 1000
    ttc = (stop - start).total_seconds()
    print('hops = {}, time-to-compute={}, traveled={}, ping={}'.format(hops, ttc, dist, ping))
    with open('results-only-distance.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([hops, ttc, dist, ping])
    timekeeper.set_time(time + timedelta(minutes=i*5))
