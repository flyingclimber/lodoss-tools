import argparse
import binascii

CPU_STRING = 'maincpu'
MEMORY_START = 0
MEMORY_END = 1000000


def encode_shift_jis(text: str, mame_format: str = False) -> str:
    """Encodes text into Shift JIS hex and optionally formats it for MAME."""
    shift_jis_bytes = text.encode("shift_jis")
    hex_output = shift_jis_bytes.hex()

    # Split into 2-byte pairs (4 hex digits)
    byte_pairs = [hex_output[i:i+4] for i in range(0, len(hex_output), 4)]

    if mame_format:
        return f"find {MEMORY_START}:{CPU_STRING},{MEMORY_END}," + ",".join(f"w.{pair}" for pair in byte_pairs)
    else:
        return " ".join(byte_pairs)


def decode_shift_jis(hex_string: str) -> str:
    """Decodes a Shift JIS hex sequence back into readable text."""
    try:
        # Normalize hex string: remove spaces, convert to lowercase
        hex_string = hex_string.replace(" ", "").lower()

        # Ensure hex_string has an even length
        if len(hex_string) % 2 != 0:
            raise ValueError("Invalid Shift JIS hex input (must be even-length).")

        # Convert hex to bytes
        shift_jis_bytes = binascii.unhexlify(hex_string)

        # Decode Shift JIS to Japanese text
        decoded_text = shift_jis_bytes.decode("shift_jis", errors="ignore")

        return decoded_text
    except Exception as e:
        return f"Error decoding Shift JIS: {e}"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert text to Shift JIS hex (and vice versa).")
    parser.add_argument("text", help="Text to encode or hex to decode")
    parser.add_argument("--mame", action="store_true", help="Output in MAME find format")
    parser.add_argument("--decode", action="store_true", help="Decode a Shift JIS hex sequence back to text")

    args = parser.parse_args()

    if args.decode:
        print(decode_shift_jis(args.text))
    else:
        print(encode_shift_jis(args.text, args.mame))
