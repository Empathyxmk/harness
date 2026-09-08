#!/usr/bin/env python3
from src.true_random import true_random

def main():
    """
    Public test: similar to tester.c, but prints more values than the original 
    to ensure different input/output data and same functionality.
    """
    for _ in range(15):
        print(true_random())

if __name__ == "__main__":
    main()