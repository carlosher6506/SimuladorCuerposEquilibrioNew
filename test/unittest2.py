import unittest
from unittest.mock import patch
from simulator import PhysicsSimulator # Assuming this is your main simulator class

class TestPhysicsSimulator(unittest.TestCase):

    @patch('pygame.display.set_mode') # Mocking pygame functions
    @patch('pygame.display.set_caption')
    @patch('pygame.time.Clock')
    def test_simulation_loop_runs(self, mock_clock, mock_set_caption, mock_set_mode):
        simulator = PhysicsSimulator()
        
if __name__ == '__main__':
    unittest.main()