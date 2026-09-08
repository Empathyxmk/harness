'use strict';

const farmhash = require('../index');

describe('farmhash public API (public tests)', () => {
  // Different string and buffer data
  const inputString = 'Pack my box with five dozen liquor jugs!';
  const inputBuffer = Buffer.from(inputString);
  const seed = 321;
  const seed2 = 654;

  describe('hash32', () => {
    it('returns a number for string input', () => {
      expect(typeof farmhash.hash32(inputString)).toBe('number');
    });

    it('returns a number for buffer input', () => {
      expect(typeof farmhash.hash32(inputBuffer)).toBe('number');
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.hash32(false)).toThrow();
      expect(() => farmhash.hash32([])).toThrow();
      expect(() => farmhash.hash32(undefined)).toThrow();
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
      expect(() => farmhash.hash32WithSeed(inputString, 'seed')).toThrow();
      expect(() => farmhash.hash32WithSeed(inputString, -2.5)).toThrow();
      expect(() => farmhash.hash32WithSeed(inputString)).toThrow();
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.hash32WithSeed(undefined, seed)).toThrow();
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
      expect(() => farmhash.hash64(false)).toThrow();
      expect(() => farmhash.hash64([])).toThrow();
      expect(() => farmhash.hash64(undefined)).toThrow();
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
      expect(() => farmhash.hash64WithSeed(inputString, {})).toThrow();
      expect(() => farmhash.hash64WithSeed(inputString, 8.9)).toThrow();
      expect(() => farmhash.hash64WithSeed(inputString)).toThrow();
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.hash64WithSeed([], seed)).toThrow();
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
      expect(() => farmhash.hash64WithSeeds(inputString, 'foo', seed2)).toThrow();
      expect(() => farmhash.hash64WithSeeds(inputString, seed, [])).toThrow();
      expect(() => farmhash.hash64WithSeeds(inputString, {}, seed2)).toThrow();
      expect(() => farmhash.hash64WithSeeds(inputString, seed)).toThrow();
      expect(() => farmhash.hash64WithSeeds(inputString)).toThrow();
    });

    it('throws for invalid input', () => {
      expect(() => farmhash.hash64WithSeeds(undefined, seed, seed2)).toThrow();
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
      expect(() => farmhash.fingerprint32(true)).toThrow();
      expect(() => farmhash.fingerprint32([])).toThrow();
      expect(() => farmhash.fingerprint32(undefined)).toThrow();
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
      expect(() => farmhash.fingerprint64(true)).toThrow();
      expect(() => farmhash.fingerprint64([])).toThrow();
      expect(() => farmhash.fingerprint64(undefined)).toThrow();
    });
  });

  describe('fingerprint64signed', () => {
    it('returns a signed bigint for string', () => {
      const unsigned = farmhash.fingerprint64('xyzzytest');
      const signed   = farmhash.fingerprint64signed('xyzzytest');
      expect(typeof signed).toBe('bigint');
      expect(
        signed.toString() === unsigned.toString() ||
        signed.toString() === (-1n*(2n**64n - unsigned)).toString()
      ).toBe(true);
    });

    it('returns a signed bigint for buffer', () => {
      const buffer = Buffer.from('xyzzytest');
      const unsigned = farmhash.fingerprint64(buffer);
      const signed   = farmhash.fingerprint64signed(buffer);
      expect(typeof signed).toBe('bigint');
      expect(
        signed.toString() === unsigned.toString() ||
        signed.toString() === (-1n*(2n**64n - unsigned)).toString()
      ).toBe(true);
    });
  });
});