'use strict';

const farmhash = require('../index');

describe('farmhash public API', () => {
  const inputString = 'The quick brown fox jumped over the lazy sleeping dog';
  const inputBuffer = Buffer.from(inputString);
  const seed = 123;
  const seed2 = 456;

  describe('hash32', () => {
    it('returns a number for string input', () => {
      expect(typeof farmhash.hash32(inputString)).toBe('number');
    });

    it('returns a number for buffer input', () => {
      expect(typeof farmhash.hash32(inputBuffer)).toBe('number');
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.hash32(123)).toThrow();
      expect(() => farmhash.hash32({})).toThrow();
      expect(() => farmhash.hash32(null)).toThrow();
    });
  });

  describe('hash32WithSeed', () => {
    it('returns a number for string input', () => {
      expect(typeof farmhash.hash32WithSeed(inputString, seed)).toBe('number');
    });

    it('returns a number for buffer input', () => {
      expect(typeof farmhash.hash32WithSeed(inputBuffer, seed)).toBe('number');
    });

    it('throws for invalid seed', () => {
      expect(() => farmhash.hash32WithSeed(inputString, 'a')).toThrow();
      expect(() => farmhash.hash32WithSeed(inputString, 1.23)).toThrow();
      expect(() => farmhash.hash32WithSeed(inputString)).toThrow();
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.hash32WithSeed(123, seed)).toThrow();
    });
  });

  describe('hash64', () => {
    it('returns a bigint for string input', () => {
      expect(typeof farmhash.hash64(inputString)).toBe('bigint');
    });

    it('returns a bigint for buffer input', () => {
      expect(typeof farmhash.hash64(inputBuffer)).toBe('bigint');
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.hash64(123)).toThrow();
      expect(() => farmhash.hash64({})).toThrow();
      expect(() => farmhash.hash64(null)).toThrow();
    });
  });

  describe('hash64WithSeed', () => {
    it('returns a bigint for string input', () => {
      expect(typeof farmhash.hash64WithSeed(inputString, seed)).toBe('bigint');
    });

    it('returns a bigint for buffer input', () => {
      expect(typeof farmhash.hash64WithSeed(inputBuffer, seed)).toBe('bigint');
    });

    it('throws for invalid seed', () => {
      expect(() => farmhash.hash64WithSeed(inputString, 'a')).toThrow();
      expect(() => farmhash.hash64WithSeed(inputString, 4.67)).toThrow();
      expect(() => farmhash.hash64WithSeed(inputString)).toThrow();
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.hash64WithSeed(123, seed)).toThrow();
    });
  });

  describe('hash64WithSeeds', () => {
    it('returns a bigint for string input', () => {
      expect(typeof farmhash.hash64WithSeeds(inputString, seed, seed2)).toBe('bigint');
    });

    it('returns a bigint for buffer input', () => {
      expect(typeof farmhash.hash64WithSeeds(inputBuffer, seed, seed2)).toBe('bigint');
    });

    it('throws for invalid seeds', () => {
      expect(() => farmhash.hash64WithSeeds(inputString, 'b', seed2)).toThrow();
      expect(() => farmhash.hash64WithSeeds(inputString, seed, null)).toThrow();
      expect(() => farmhash.hash64WithSeeds(inputString, 23.4, seed2)).toThrow();
      expect(() => farmhash.hash64WithSeeds(inputString, seed)).toThrow();
      expect(() => farmhash.hash64WithSeeds(inputString)).toThrow();
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.hash64WithSeeds(123, seed, seed2)).toThrow();
    });
  });

  describe('fingerprint32', () => {
    it('returns a number for string input', () => {
      expect(typeof farmhash.fingerprint32(inputString)).toBe('number');
    });

    it('returns a number for buffer input', () => {
      expect(typeof farmhash.fingerprint32(inputBuffer)).toBe('number');
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.fingerprint32(555)).toThrow();
      expect(() => farmhash.fingerprint32({})).toThrow();
      expect(() => farmhash.fingerprint32(null)).toThrow();
    });
  });

  describe('fingerprint64', () => {
    it('returns a bigint for string input', () => {
      expect(typeof farmhash.fingerprint64(inputString)).toBe('bigint');
    });

    it('returns a bigint for buffer input', () => {
      expect(typeof farmhash.fingerprint64(inputBuffer)).toBe('bigint');
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.fingerprint64(555)).toThrow();
      expect(() => farmhash.fingerprint64({})).toThrow();
      expect(() => farmhash.fingerprint64(null)).toThrow();
    });
  });

  describe('fingerprint64signed', () => {
    it('returns a signed bigint for string', () => {
      const unsigned = farmhash.fingerprint64('1footrue');
      const signed = farmhash.fingerprint64signed('1footrue');
      expect(typeof signed).toBe('bigint');
      // Signed must have different string value if BigInt.asIntN "flips" high bit
      expect(
        signed.toString() === unsigned.toString() ||
        signed.toString() === (-1n*(2n**64n - unsigned)).toString()
      ).toBe(true);
    });

    it('returns a signed bigint for buffer', () => {
      const buffer = Buffer.from('1footrue');
      const unsigned = farmhash.fingerprint64(buffer);
      const signed = farmhash.fingerprint64signed(buffer);
      expect(typeof signed).toBe('bigint');
      expect(
        signed.toString() === unsigned.toString() ||
        signed.toString() === (-1n*(2n**64n - unsigned)).toString()
      ).toBe(true);
    });
  });
});