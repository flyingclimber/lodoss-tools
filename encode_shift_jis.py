import argparse

CARRIAGE_RETURN_HEX = ["0026", "0005"]
CPU_STRING = 'maincpu'
MEMORY_START = 0
MEMORY_END = 1000000

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('text', help="The Shift JIS text to encode")
    parser.add_argument('--mame', action='store_true', help="Output in MAME find format")
    args = parser.parse_args()

    text = args.text

    shift_jis_bytes = text.encode("shift_jis")
    hex_output = shift_jis_bytes.hex()

    # Split into 2-byte (4 hex-digit) pairs
    byte_pairs = [hex_output[i:i+4] for i in range(0, len(hex_output), 4)]

    formatted_pairs = []
    for char in text:
        if char == "\n":
            formatted_pairs.extend(CARRIAGE_RETURN_HEX)  # Insert special mapping
        else:
            shift_jis_bytes = char.encode("shift_jis")
            hex_pair = shift_jis_bytes.hex()
            if len(hex_pair) == 4:  # Valid Shift JIS pair
                formatted_pairs.append(hex_pair)

    if args.mame:
        # Convert to MAME format: find 0,10000,w.8023,w.9023, ...
        mame_output = f"find {MEMORY_START}:{CPU_STRING},{MEMORY_END}," + ",".join(f"w.{pair}" for pair in formatted_pairs)
        print(mame_output)
    else:
        # Default 2-byte hex pair output
        print(" ".join(formatted_pairs))
