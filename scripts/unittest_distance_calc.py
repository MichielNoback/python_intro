import unittest


def distance_meters4(speed_km_h, time_sec = 1):
    return (1000 / 3600) * speed_km_h * time_sec


class TestDistanceCalculations(unittest.TestCase):

    def test_zero(self):
        self.assertAlmostEqual(distance_meters4(4, 0), 0, places = 6)
        self.assertAlmostEqual(distance_meters4(4000000, 0), 0, places = 6)
        self.assertAlmostEqual(distance_meters4(0, 10000), 0, places = 6)
    
    def test_normal(self):
        self.assertAlmostEqual(distance_meters4(36, 5), 50, places = 6)
        self.assertAlmostEqual(distance_meters4(36), 10, places = 6)
        
if __name__ == '__main__':
    unittest.main()
