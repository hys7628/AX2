import unittest
from gugudan import generate_dan, format_dan, format_all_tables

class TestGugudan(unittest.TestCase):
    def test_generate_dan_success(self):
        """Verify that generate_dan returns the correct multiplication list."""
        result = generate_dan(3, limit=3)
        expected = [
            (3, 1, 3),
            (3, 2, 6),
            (3, 3, 9)
        ]
        self.assertEqual(result, expected)

    def test_generate_dan_invalid_inputs(self):
        """Verify that generate_dan raises ValueError for invalid inputs."""
        with self.assertRaises(ValueError):
            generate_dan(0)
        with self.assertRaises(ValueError):
            generate_dan(5, limit=-1)

    def test_format_dan(self):
        """Verify the formatting of a single dan."""
        formatted = format_dan(5, limit=3)
        lines = formatted.split("\n")
        self.assertEqual(lines[0], "=== 5단 ===")
        self.assertEqual(lines[1], "5 x 1 = 5")
        self.assertEqual(lines[2], "5 x 2 = 10")
        self.assertEqual(lines[3], "5 x 3 = 15")

    def test_format_all_tables_columns(self):
        """Verify format_all_tables lays out multiple dans in columns correctly."""
        # Print 2단 to 3단 with 2 columns, up to multiplier 2
        formatted = format_all_tables(start=2, end=3, limit=2, cols=2)
        lines = formatted.split("\n")
        
        # We expect a header line, and 2 multiplication lines
        # Check that headers are present
        self.assertIn("=== 2단 ===", lines[0])
        self.assertIn("=== 3단 ===", lines[0])
        
        # Check content lines
        self.assertIn("2 x 1 = 2", lines[1])
        self.assertIn("3 x 1 = 3", lines[1])
        self.assertIn("2 x 2 = 4", lines[2])
        self.assertIn("3 x 2 = 6", lines[2])

    def test_format_all_tables_invalid_range(self):
        """Verify that format_all_tables raises ValueError when start > end."""
        with self.assertRaises(ValueError):
            format_all_tables(start=5, end=4)

if __name__ == "__main__":
    unittest.main()
