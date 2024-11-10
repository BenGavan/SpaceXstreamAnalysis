import unittest
from frame_analysis import processframe_fromfile

class Row:
    def __init__(self, filepath, time_seconds, bootster_speed, bootster_altitude, ship_speed, ship_altitude):
        self.filepath = filepath
        self.time_seconds = time_seconds

        self.booster_speed = bootster_speed
        self.bootster_altitude = bootster_altitude

        self.ship_speed = ship_speed
        self.ship_altitude = ship_altitude


class TestFrameAnalysis(unittest.TestCase):

    def test_telemetry(self):
        table = [
            Row('../img/Screenshot 2024-11-09 at 17.02.23.png', 22, 369, 1, None, None),
            Row('../img/Screenshot 2024-11-09 at 17.26.04.png', 60*4 + 17, 2002, 93, 7700, 121)
        ]

        for row in table:
            d = processframe_fromfile(row.filepath)
            self.assertEqual(d.booster_altitude, row.bootster_altitude)
            self.assertEqual(d.booster_speed, row.booster_speed)
            self.assertEqual(d.time_seconds, row.time_seconds)


        


if __name__ == '__main__':
    unittest.main()
