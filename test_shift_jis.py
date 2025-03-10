import unittest
from encode_shift_jis import encode_shift_jis, decode_shift_jis

class TestShiftJISEncoding(unittest.TestCase):

    def test_encode_basic_text(self):
        """Test encoding basic Japanese text."""
        self.assertEqual(encode_shift_jis("ゾンビ"), "835d 8393 8372")

    def test_encode_mame_format(self):
        """Test encoding with MAME format output."""
        self.assertEqual(
            encode_shift_jis("ゾンビ", mame_format=True),
            "find 0:maincpu,1000000,w.835d,w.8393,w.8372"
        )

    def test_decode_basic_text(self):
        """Test decoding basic Shift JIS hex back to text."""
        self.assertEqual(decode_shift_jis("835d83938372"), "ゾンビ")

    def test_decode_mixed_spacing(self):
        """Test decoding Shift JIS hex with inconsistent spaces between bytes."""
        self.assertEqual(decode_shift_jis("835d  8393    8372"), "ゾンビ")

    def test_invalid_odd_length_hex(self):
        """Test decoding an odd-length hex string (should raise error)."""
        self.assertIn("Invalid Shift JIS hex input", decode_shift_jis("835d 839"))

    def test_invalid_hex_characters(self):
        """Test decoding invalid hex characters."""
        self.assertIn("Error decoding Shift JIS", decode_shift_jis("ZZZZ ZZZZ"))

if __name__ == '__main__':
    unittest.main()
