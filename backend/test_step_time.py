import unittest
from Step_Time_Calculation import calculate_step_time 
import math

class TestCalculateStepTime(unittest.TestCase):

    def test_step_time_below_threshold(self):
        # All values below threshold should yield no step times
        force_data = [(0.0, 0), (0.1, 0), (0.2, 10), (0.3, 15)]
        step_times = calculate_step_time(force_data)
        self.assertEqual(step_times, [])  # Expected: []

    
    def test_step_time_calculation(self):
        # Adjusted force data
        force_data = [
            (0.0, 0), (0.1, 25), (0.2, 30), (0.3, 0),  # First step
            (0.4, 0), (0.5, 25), (0.6, 30), (0.7, 0)   # Second step
        ]
        step_times = calculate_step_time(force_data)
        # Check if the step times are approximately equal to expected values
        self.assertTrue(math.isclose(step_times[0], 0.2, rel_tol=1e-9))
        self.assertTrue(math.isclose(step_times[1], 0.2, rel_tol=1e-9))
    
    def test_moving_average(self):
        force_data = [
            (0.0, 0), (0.1, 25), (0.2, 30), (0.3, 0),
            (0.4, 0), (0.5, 25), (0.6, 30), (0.7, 0)
        ]
        step_times = calculate_step_time(force_data)
        # Check if the step times are approximately equal to expected values
        self.assertTrue(math.isclose(step_times[0], 0.2, rel_tol=1e-9))
        self.assertTrue(math.isclose(step_times[1], 0.2, rel_tol=1e-9))



