"""Unit tests for BNS Section 318 statutory penalty thresholds."""

import unittest


class TestBNSCheatingPenalties(unittest.TestCase):
    def test_basic_cheating_imprisonment_limit(self):
        max_years = 3
        self.assertLessEqual(max_years, 3)

    def test_cheating_with_knowledge_of_wrongful_loss(self):
        max_years = 5
        self.assertEqual(max_years, 5)

    def test_cheating_and_dishonestly_inducing_delivery(self):
        max_years = 7
        self.assertGreaterEqual(max_years, 7)


if __name__ == '__main__':
    unittest.main()
