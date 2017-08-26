"""math_test is a testing specs for math"""

import unittest

from maths import maths

class MathTestCase(unittest.TestCase):
    """MathTestCase defines test cases for math module"""
    def test_add_method(self):
        """test_add_method simply test the add method"""
        self.assertEqual(3, maths.add(1, 2))
        self.assertEqual(6, maths.add(3, 3))

    def test_multiply_method(self):
        """test multiply result"""
        self.assertEqual(6, maths.multiply(2, 3))
        self.assertEqual(8, maths.multiply(2, 4))
        self.assertEqual(8, maths.multiply(4, 2))
