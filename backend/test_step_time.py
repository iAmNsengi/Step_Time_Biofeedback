import unittest
from Step_Time_Calculation import calculate_step_time
from target_zone_estimation import estimate_target_zone
from target_zone_estimation import load_data_from_file
import os
import asyncio

THRESHOLD = 20.0 
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "tied_belt_OSS_f_1.tsv")

class TestStepTimeAndTargetZone(unittest.TestCase):

    def test_no_steps_below_threshold(self):
        """Test that all values below threshold yield no step times."""
        force_data = [(0.0, 0), (0.1, 0), (0.2, 10), (0.3, 15)]
        step_times = calculate_step_time(force_data)
        self.assertEqual(step_times, []) 

    def test_step_time_calculation(self):
        """Test that the step times are calculated correctly with given data."""
        force_data = [
            (0.0, 0), (0.1, 25), (0.2, 30), (0.3, 0),  
            (0.4, 0), (0.5, 25), (0.6, 30), (0.7, 0)  
        ]
        step_times = calculate_step_time(force_data)
        self.assertAlmostEqual(step_times[0], 0.2, places=2)
        self.assertAlmostEqual(step_times[1], 0.2, places=2)  

    def test_moving_average_step_times(self):
        """Test that the calculated step times match expected moving averages."""
        force_data = [
            (0.0, 0), (0.1, 25), (0.2, 30), (0.3, 0),
            (0.4, 0), (0.5, 25), (0.6, 30), (0.7, 0)
        ]
        step_times = calculate_step_time(force_data)
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
        """Test step time calculation with real data from the sample file."""
        real_force_data = asyncio.run(self.async_load_data_from_file())
        step_times = calculate_step_time(real_force_data)

        self.assertTrue(len(step_times) > 0, "Step times were not calculated as expected")

    async def async_load_data_from_file(self):
        """Asynchronous helper to load data from the file."""
        return [data async for data in load_data_from_file(DATA_FILE_PATH)]
