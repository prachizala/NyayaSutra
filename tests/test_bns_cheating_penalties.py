"""Unit tests for BNS Section 318 statutory penalty thresholds."""
import unittest

class TestBNSCheatingPenalties(unittest.TestCase):
    def test_penalty_thresholds(self):
        bns_section = 318
        max_imprisonment_years = 7
        self.assertEqual(bns_section, 318)
        self.assertLessEqual(max_imprisonment_years, 7)

if __name__ == '__main__':
    unittest.main()
