#!/usr/bin/env python3
import sys
from src.true_random import get_bit, get_byte

def main():
    """
    Generate a constant stream of 20 bytes in a different bit-packing pattern.
    """
    # Generate 20 bytes of data and write to stdout
    for _ in range(20):
        sys.stdout.buffer.write(bytes([get_byte()]))

if __name__ == "__main__":
    main()