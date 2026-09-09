import unittest
import importlib

# Dynamic import since the module name starts with a digit
module = importlib.import_module("0908_1")
generate_lotto_game = module.generate_lotto_game

class TestLottoGenerator(unittest.TestCase):
    def test_lotto_length(self):
        """Verify that exactly 6 numbers are generated."""
        game = generate_lotto_game()
        self.assertEqual(len(game), 6)

    def test_lotto_range(self):
        """Verify that all generated numbers are between 1 and 45."""
        game = generate_lotto_game()
        for number in game:
            self.assertTrue(1 <= number <= 45, f"Number {number} is out of range 1-45")

    def test_lotto_uniqueness(self):
        """Verify that all 6 numbers are unique."""
        game = generate_lotto_game()
        self.assertEqual(len(set(game)), 6, f"Duplicate numbers found in {game}")

    def test_lotto_sorted(self):
        """Verify that numbers are sorted in ascending order."""
        game = generate_lotto_game()
        self.assertEqual(game, sorted(game), f"Game numbers are not sorted: {game}")

if __name__ == '__main__':
    unittest.main()
