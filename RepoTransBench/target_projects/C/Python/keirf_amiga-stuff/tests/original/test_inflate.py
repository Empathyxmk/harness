import os
import struct
import sys
import crcmod.predefined

# This is a direct Python translation/adaptation of the original C-style test harness

GZIP = "zopfli --i32 -c"
GUNZIP = "gunzip -c"

HUNK_HEADER = 0x3f3
HUNK_CODE   = 0x3e9
HUNK_END    = 0x3f2
PREFIX = '_test_'

def test_inflate_file(name):
    """Runs the inflate test on the given file (requires supporting binaries)."""
    if name.endswith('.gz'):
        # _test_1: Local copy of original gzipped file
        os.system('cp "{}" {}1'.format(name, PREFIX))
        # _test_0: Uncompressed file
        os.system('{} {}1 >{}0'.format(GUNZIP, PREFIX, PREFIX))
    else:
        # _test_0: Local copy of original uncompressed file
        os.system('cp "{}" {}0'.format(name, PREFIX))
        # _test_1: Gzipped file
        os.system('{} {}0 >{}1'.format(GZIP, PREFIX, PREFIX))

    # CRC of uncompressed data
    crc16 = crcmod.predefined.Crc('crc-ccitt-false')
    with open(PREFIX + '0', 'rb') as f:
        crc16.update(f.read())

    # _test_2: DEFLATE stream + custom header/footer
    os.system('degzip -H {}1 {}2'.format(PREFIX, PREFIX))

    # _test_3: Register & memory state for 68000 emulator
    f = open(PREFIX + '3', 'wb')
    # Poison exception vectors and low memory to 0x1000
    mem = bytearray([0xde,0xad,0xbe,0xef]) * 0x400
    # Marshal the depacker and test harness (Amiga load file)
    with open('test_inflate', 'rb') as infile:
        (id, x, nr, first, last) = struct.unpack('>5I', infile.read(5*4))
        assert id == HUNK_HEADER and x == 0
        assert nr == 1 and first == 0 and last == 0
        (x, id, nr) = struct.unpack('>3I', infile.read(3*4))
        assert id == HUNK_CODE and nr == x
        mem += infile.read(nr * 4)
        (id,) = struct.unpack('>I', infile.read(4))
        assert id == HUNK_END
    # Marshal the compressed binary with header (padded to longword)
    with open(PREFIX + '2', 'rb') as infile:
        mem += infile.read()
    mem += bytearray([0]) * (-len(mem)&3)
    # Poison remaining longwords to top of memory
    remain = (0x200000 - len(mem)) // 4
    mem += bytearray([0xde,0xad,0xbe,0xef]) * (remain-1)
    # Final return address is magic longword (we check PC after emulation)
    mem += bytearray([0xf0,0xe0,0xd0,0xc0])
    f.write(mem)
    # Initial register state: only SR,PC,SP really matter
    f.write(struct.pack('>18IH6x', 0,0,0,0,0,0,0,0, # D0-D7
                        0,0,0,0,0,0,0,0x1ffffc, # A0-A7
                        0x1000, # PC
                        0, # SSP
                        0)) # SR
    f.close()

    # Requires m68k_emulate from Github:keirf/Disk-Utilities.git/m68k on PATH
    os.system('m68k_emulate {}3 {}4'.format(PREFIX, PREFIX))
    with open(PREFIX + '4', 'rb') as f:
        mem = bytes(f.read(0x200000))
        (d0,d1,d2,d3,d4,d5,d6,d7) = struct.unpack('>8I', f.read(8*4))
        (a0,a1,a2,a3,a4,a5,a6,a7) = struct.unpack('>8I', f.read(8*4))
        (pc,ssp,sr) = struct.unpack('>2IH6x', f.read(4*4))
        # Checks
        assert pc == 0xf0e0d0c0
        assert a7 == 0x200000
        assert d0&0xffff == crc16.crcValue  # Emulated CRC == our CRC?
        assert d0&0xffff == d2&0xffff      # Emulated CRC == header CRC?
        assert sr&4  # CC_Z
        crc16.crcValue = 0xffff
        crc16.update(mem[a0:a0+d1])
        assert d0&0xffff == crc16.crcValue

    # All done: clean up
    os.system('rm {}*'.format(PREFIX))

def test_inflate_py():
    # Choose a robust file for CI - needs to be present
    # Prefer README.md, else COPYING, else some gzipped asset if present
    test_files = []
    try:
        if os.path.exists("../../README.md"):
            test_files.append("../../README.md")
        elif os.path.exists("../../COPYING"):
            test_files.append("../../COPYING")
        elif os.path.exists("test_assets/XenonIcon.gz"):
            test_files.append("test_assets/XenonIcon.gz")
    except Exception:
        pass
    if not test_files:
        pytest.skip("No suitable test file found for inflate test!")
    for f in test_files:
        test_inflate_file(f)