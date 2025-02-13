import unittest
from core.physic import calculate_tensions, calculate_body_position, conversor
import math

class TestPhysicsCalculations(unittest.TestCase):

    def test_calculate_tensions(self):
        # Test case 1: Equal angles
        T1, T2 = calculate_tensions(100, 45, 45)
        self.assertAlmostEqual(T1, T2, delta=0.01)  # Account for floating-point precision

        # Test case 2: Different angles
        T1, T2 = calculate_tensions(100, 30, 60)
        self.assertAlmostEqual(T1, 50, delta=0.01)
        self.assertAlmostEqual(T2, 86.6, delta=0.01)

        # Test case 3: Edge case (denominator near zero)
        with self.assertRaises(ZeroDivisionError): # This assumes it raises ZeroDivisionError
            calculate_tensions(100, 89.9, 89.9)


    def test_calculate_body_position(self):
        # Test case 1: Simple case
        x, y = calculate_body_position(100, 300, 100, 50, 50, 45, 45)
        self.assertAlmostEqual(x, 200, delta=1) # Account for integer conversion
        self.assertAlmostEqual(y, 135, delta=1)

        # Add more test cases with different inputs

    def test_conversor(self):
        self.assertEqual(conversor(1), 9.81)
        self.assertEqual(conversor(10), 98.1)
        self.assertEqual(conversor(0), 0)

if __name__ == '__main__':
    unittest.main()