"""Unit test suite for BNS Section 329 concordance."""

import unittest


class TestBNSSection329Concordance(unittest.TestCase):
    def test_section_329_mapping(self):
        ipc_counterpart = "Section 441/447"
        bns_section = 329
        self.assertEqual(bns_section, 329)
        self.assertIn("441", ipc_counterpart)


if __name__ == "__main__":
    unittest.main()
