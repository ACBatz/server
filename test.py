from satellite import Satellite

tleLine1 = '1 25544U 98067A   13149.87225694  .00009369  00000-0  16828-3 0  9031'
tleLine2 = '2 25544 051.6485 199.1576 0010128 012.7275 352.5669 15.50581403831869'
sat = Satellite(id='sat2', size=10, line1=tleLine1, line2=tleLine2)

position = sat.get_position({'year': 2019, 'month': 3, 'day': 2, 'hour': 23, 'minute': 59, 'second': 55})
print(position)
