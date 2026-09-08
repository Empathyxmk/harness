const BSync = require('../bit-sync');

describe('BSync.util', () => {
  describe('readInt32', () => {
    it('reads positive int32 values correctly', () => {
      // 0x7FFFFFFF == 2147483647
      const arr = new Uint8Array([0xff, 0xff, 0xff, 0x7f]);
      expect(BSync.util.readInt32(arr, 0)).toBe(2147483647);
    });
    it('reads max uint32 (0xFFFFFFFF) as 4294967295', () => {
      const arr = new Uint8Array([0xff, 0xff, 0xff, 0xff]);
      expect(BSync.util.readInt32(arr, 0)).toBe(4294967295);
    });
    it('reads zero from int32', () => {
      expect(BSync.util.readInt32(new Uint8Array([0,0,0,0]), 0)).toBe(0);
    });
  });

  describe('adler32', () => {
    it('computes correct adler32 checksum for [1,2,3,4]', () => {
      const arr = new Uint8Array([1,2,3,4]);
      const out = BSync.util.adler32(0, 4, arr);
      expect(out.a).toBe(11);
      expect(out.b).toBe(24);
      expect(out.checksum).toBe((out.b << 16) | out.a);
    });
    it('returns 1 if length is 0', () => {
      expect(BSync.util.adler32(0, 0, new Uint8Array([])).checksum).toBe(1);
    });
  });

  describe('makeBlockChecksums', () => {
    it('returns expected number of blocks', () => {
      const arr = new Uint8Array([1,1,1,1, 2,2,2,2, 3,3,3,3]);
      const blocks = BSync.util.makeBlockChecksums(arr, 4);
      expect(blocks.length).toBe(3);
      for (const block of blocks) {
        expect(typeof block.weak).toBe('number');
        expect(typeof block.strong).toBe('string');
      }
    });
    it('handles empty buffer', () => {
      expect(BSync.util.makeBlockChecksums(new Uint8Array([]), 4)).toEqual([]);
    });
  });

  describe('padBuffer', () => {
    it('pads to larger size', () => {
      const arr = new Uint8Array([1,2,3]);
      const padded = BSync.util.padBuffer(arr, 5);
      expect(padded.length).toBe(5);
      expect(padded[0]).toBe(1);
      expect(padded[2]).toBe(3);
      expect(padded[4]).toBe(0);
    });
    it('returns the same buffer if already correct size', () => {
      const arr = new Uint8Array([1,2,3]);
      expect(BSync.util.padBuffer(arr, 3)).toEqual(arr);
    });
    it('returns empty buffer for 0 size', () => {
      expect(BSync.util.padBuffer(new Uint8Array([]), 0)).toEqual(new Uint8Array([]));
    });
  });
});

describe('BSync main API', () => {
  it('can compute differences and patches for simple blocks', () => {
    const buf1 = new Uint8Array([0,1,2,3,4,5,6,7,8,9]);
    const buf2 = new Uint8Array([0,1,9,3,4,50,6,7,8,9]);
    const blockSize = 5;
    const aBlocks = BSync.util.makeBlockChecksums(buf1, blockSize);
    const bBlocks = BSync.util.makeBlockChecksums(buf2, blockSize);

    const diff = BSync.diff(buf1, blockSize, bBlocks);
    // check structure
    expect(Array.isArray(diff)).toBeTruthy();

    const patched = BSync.patch(buf2, diff);
    expect(patched).toBeInstanceOf(Uint8Array);
    expect(patched.length).toBe(buf1.length);
  });

  it('patch returns original buffer if diff is empty or null', () => {
    const orig = new Uint8Array([1,2,3]);
    expect(BSync.patch(orig, [])).toBe(orig);
    expect(BSync.patch(orig, null)).toBe(orig);
  });

  // More coverage: diff with null/edge cases
  it('diff returns empty ops when input buffer is empty', () => {
    const diff = BSync.diff(new Uint8Array([]), 4, []);
    expect(Array.isArray(diff)).toBe(true);
    expect(diff.length).toBe(0);
  });
  it('diff returns a single insert with data when bBlocks is null/empty', () => {
    const buffer = new Uint8Array([1, 2, 3]);
    [null, undefined, []].forEach(bBlocks => {
      const diff = BSync.diff(buffer, 4, bBlocks);
      expect(diff.length).toBe(1);
      expect(diff[0].type).toBe('insert');
      expect(diff[0].data).toEqual(buffer);
    });
  });

  // Coverage for patch with only 'insert' ops
  it('patch concatenates insert ops', () => {
    const b1 = new Uint8Array([5,6]);
    const b2 = new Uint8Array([7]);
    const diff = [
      { type: 'insert', data: b1 },
      { type: 'insert', data: b2 },
    ];
    const result = BSync.patch(new Uint8Array(), diff);
    expect(Array.from(result)).toEqual([5,6,7]);
  });

  // Coverage for patch with empty ops array
  it('patch returns original buffer for empty ops', () => {
    const orig = new Uint8Array([9]);
    expect(BSync.patch(orig, [])).toBe(orig);
  });
});