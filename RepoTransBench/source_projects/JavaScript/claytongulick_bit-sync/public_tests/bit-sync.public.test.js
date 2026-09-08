const BSync = require('../bit-sync');

describe('BSync.util (public tests)', () => {
  describe('readInt32', () => {
    it('reads another positive int32 value correctly', () => {
      // 0x12345678 == 305419896
      const arr = new Uint8Array([0x78, 0x56, 0x34, 0x12]);
      expect(BSync.util.readInt32(arr, 0)).toBe(305419896);
    });
    it('reads 0x0000FFFF as 65535', () => {
      const arr = new Uint8Array([0xff, 0xff, 0x00, 0x00]);
      expect(BSync.util.readInt32(arr, 0)).toBe(65535);
    });
    it('reads 0x00010000 as 65536', () => {
      const arr = new Uint8Array([0x00, 0x00, 0x01, 0x00]);
      expect(BSync.util.readInt32(arr, 0)).toBe(65536);
    });
  });

  describe('adler32', () => {
    it('computes correct adler32 checksum for [10,20,30]', () => {
      const arr = new Uint8Array([10,20,30]);
      const out = BSync.util.adler32(0, 3, arr);
      expect(out.a).toBe(1 + 10 + 20 + 30);
      expect(out.b).toBe((1 + 10) + (1 + 10 + 20) + (1 + 10 + 20 + 30));
      expect(out.checksum).toBe((out.b << 16) | out.a);
    });
    it('returns 1 if length is 0 (different buffer)', () => {
      expect(BSync.util.adler32(0, 0, new Uint8Array([1,2,3,4])).checksum).toBe(1);
    });
  });

  describe('makeBlockChecksums', () => {
    it('returns correct number of blocks for length not divisible by blockSize', () => {
      const arr = new Uint8Array([8,8,8, 7,7,7, 6]);
      const blocks = BSync.util.makeBlockChecksums(arr, 3);
      expect(blocks.length).toBe(3);
      for (const block of blocks) {
        expect(typeof block.weak).toBe('number');
        expect(typeof block.strong).toBe('string');
      }
    });
    it('handles empty buffer for blockSize > 1', () => {
      expect(BSync.util.makeBlockChecksums(new Uint8Array([]), 2)).toEqual([]);
    });
  });

  describe('padBuffer', () => {
    it('pads a buffer to larger size with zeros (new data)', () => {
      const arr = new Uint8Array([10,20]);
      const padded = BSync.util.padBuffer(arr, 4);
      expect(padded.length).toBe(4);
      expect(padded[0]).toBe(10);
      expect(padded[1]).toBe(20);
      expect(padded[3]).toBe(0);
    });
    it('returns the same buffer if already correct size (other data)', () => {
      const arr = new Uint8Array([9,8,7]);
      expect(BSync.util.padBuffer(arr, 3)).toEqual(arr);
    });
    it('returns empty buffer for size=0 (edge test)', () => {
      expect(BSync.util.padBuffer(new Uint8Array([]), 0)).toEqual(new Uint8Array([]));
    });
  });
});

describe('BSync main API (public tests)', () => {
  it('can compute differences and patches for other blocks', () => {
    const buf1 = new Uint8Array([10,11,12,13,14,15,16,17]);
    const buf2 = new Uint8Array([10,99,12,13,55,15,88,17]);
    const blockSize = 4;
    const aBlocks = BSync.util.makeBlockChecksums(buf1, blockSize);
    const bBlocks = BSync.util.makeBlockChecksums(buf2, blockSize);

    const diff = BSync.diff(buf1, blockSize, bBlocks);
    expect(Array.isArray(diff)).toBeTruthy();

    const patched = BSync.patch(buf2, diff);
    expect(patched).toBeInstanceOf(Uint8Array);
    expect(patched.length).toBe(buf1.length);
  });

  it('patch returns original buffer if diff is empty or null with other data', () => {
    const orig = new Uint8Array([4,3,2,1]);
    expect(BSync.patch(orig, [])).toBe(orig);
    expect(BSync.patch(orig, null)).toBe(orig);
  });

  it('diff returns empty ops when buffer is empty, with non-4 block size', () => {
    const diff = BSync.diff(new Uint8Array([]), 8, []);
    expect(Array.isArray(diff)).toBe(true);
    expect(diff.length).toBe(0);
  });
  it('diff returns single insert for non-trivial buffer and bBlocks empty/null', () => {
    const buffer = new Uint8Array([42, 69]);
    [null, undefined, []].forEach(bBlocks => {
      const diff = BSync.diff(buffer, 2, bBlocks);
      expect(diff.length).toBe(1);
      expect(diff[0].type).toBe('insert');
      expect(diff[0].data).toEqual(buffer);
    });
  });

  it('patch concatenates only insert ops with new test data', () => {
    const b1 = new Uint8Array([3,4]);
    const b2 = new Uint8Array([5,6,7]);
    const diff = [
      { type: 'insert', data: b1 },
      { type: 'insert', data: b2 },
    ];
    const result = BSync.patch(new Uint8Array(), diff);
    expect(Array.from(result)).toEqual([3,4,5,6,7]);
  });

  it('patch returns original buffer for empty ops (alternate buffer)', () => {
    const orig = new Uint8Array([123, 124]);
    expect(BSync.patch(orig, [])).toBe(orig);
  });
});