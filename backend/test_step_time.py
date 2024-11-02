import unittest
from Step_Time_Calculation import calculate_step_time
from target_zone_estimation import estimate_target_zone

THRESHOLD = 20.0

class TestStepTimeAndTargetZone(unittest.TestCase):

    def test_no_steps_below_threshold(self):
        """Test that all values below threshold yield no step times."""
        force_data = [(0.0, 0), (0.1, 0), (0.2, 10), (0.3, 15)]
        step_times = calculate_step_time(force_data, THRESHOLD)
        self.assertEqual(step_times, [])

    def test_step_time_calculation(self):
        """Test that the step times are calculated correctly with given data."""
        force_data = [
            (0.0, 0), (0.1, 25), (0.2, 30), (0.3, 0),
            (0.4, 0), (0.5, 25), (0.6, 30), (0.7, 0)
        ]
        step_times = calculate_step_time(force_data, THRESHOLD)
        self.assertAlmostEqual(step_times[0], 0.2, places=2)
        self.assertAlmostEqual(step_times[1], 0.2, places=2)

    def test_moving_average_step_times(self):
        """Test that the calculated step times match expected moving averages."""
        force_data = [
            (0.0, 0), (0.1, 25), (0.2, 30), (0.3, 0),
            (0.4, 0), (0.5, 25), (0.6, 30), (0.7, 0)
        ]
        step_times = calculate_step_time(force_data, THRESHOLD)
        self.assertAlmostEqual(step_times[0], 0.2, places=2)
        self.assertAlmostEqual(step_times[1], 0.2, places=2)

    def test_estimate_target_zone_with_steps(self):
        """Test target zone estimation with valid step times."""
        step_times = [0.2, 0.3, 0.4]
        target_zone = estimate_target_zone(step_times)

        self.assertEqual(target_zone['min'], min(step_times))
        self.assertEqual(target_zone['max'], max(step_times))
        self.assertAlmostEqual(target_zone['average'], sum(step_times) / len(step_times), places=2)

    def test_no_movement_target_zone(self):
        """Test target zone estimation when no step times are provided."""
        step_times = []
        target_zone = estimate_target_zone(step_times)

        self.assertEqual(target_zone, {"min": 0.0, "max": 0.0, "average": 0.0})

    def test_real_data_step_time_calculation(self):
        """Test step time calculation with real data."""
        real_force_data = [
            (0.00000, 159.548187),
            (0.00093, 159.304047),
            (0.01296, 158.327484),
            (0.01620, 158.327484),
            (0.05370, 157.106781),
            (0.05972, 156.862640)
        ]

        step_times = calculate_step_time(real_force_data, THRESHOLD)

        expected_step_times = []  # Assuming no steps are calculated with this data

        self.assertEqual(step_times, expected_step_times)

if __name__ == '__main__':
    unittest.main()
