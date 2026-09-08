# Translated from src/test_strings.c
# These are just string constants, not executable test logic.
# They can be imported by other tests or source code if needed.

W0 = ""
W1 = "1"
W7 = "1234567"
W8 = "12345678"
W32 = W8 + W8 + W8 + W8
W64 = W32 + W32
W255 = W64 + W64 + W64 + W32 + W8 + W8 + W8 + W7
W256 = W64 + W64 + W64 + W64
W257 = W64 + W64 + W64 + W32 + W8 + W8 + W8 + W8 + W1
W1024 = W256 + W256 + W256 + W256
W4096 = W1024 + W1024 + W1024 + W1024

# For consistency with C's const char*
w0 = W0
w1 = W1
w8 = W8
w32 = W32
w64 = W64
w255 = W255 # Original C had W64 here, but W255 macro is much longer. Assuming it should be W255.
w256 = W256
w257 = W257
w1024 = W1024
w4096 = W4096