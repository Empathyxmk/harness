const ip = require('../lib/ip');
const { Buffer } = require('buffer');

describe('ip.js - Basic methods (Public Tests)', () => {
  describe('IPv4 toBuffer and toString', () => {
    it('should convert IPv4 string to Buffer and back', () => {
      const buf = ip.toBuffer('8.8.8.8');
      expect(buf.toString('hex')).toBe('08080808');
      expect(ip.toString(buf)).toBe('8.8.8.8');
    });
    it('should convert IPv4 in-place', () => {
      const buf = Buffer.alloc(12);
      ip.toBuffer('123.45.67.89', buf, 4);
      expect(buf.toString('hex', 4, 8)).toBe('7b2d4359');
      expect(ip.toString(buf, 4, 4)).toBe('123.45.67.89');
    });
  });

  describe('IPv6 toBuffer and toString', () => {
    it('should convert IPv6 string to Buffer and back', () => {
      const buf = ip.toBuffer('cafe:0:0:0:0:0:0:3');
      expect(buf.length).toBe(16);
      expect(['cafe:0:0:0:0:0:0:3', 'cafe::3']).toContain(ip.toString(buf));
    });
    it('should handle abbreviated IPv6', () => {
      const buf = ip.toBuffer('f00d::4');
      expect(ip.toString(buf)).toContain('f00d');
    });
    it('should convert IPv6 with embedded IPv4', () => {
      const buf = ip.toBuffer('::ffff:198.51.100.42');
      expect(ip.toString(buf)).toContain('ffff');
    });
    it('should convert IPv6 in-place', () => {
      const buf = Buffer.alloc(32);
      ip.toBuffer('3::', buf, 2);
      expect(ip.toString(buf, 2, 16)).toBe('3::');
    });
  });

  describe('input validation', () => {
    it('throws for invalid input', () => {
      expect(() => ip.toBuffer('hello.world')).toThrow();
    });
  });

  describe('isV4Format', () => {
    it('detects v4', () => {
      expect(ip.isV4Format('172.16.0.1')).toBe(true);
      expect(ip.isV4Format('172.16.0')).toBe(false);
      expect(ip.isV4Format('f00d::4')).toBe(false);
    });
  });

  describe('isV6Format', () => {
    it('detects v6', () => {
      expect(ip.isV6Format('babe::10')).toBe(true);
      expect(ip.isV6Format('123.45.67.89')).toBe(true); // as per implementation detail
      expect(ip.isV6Format('babe::')).toBe(true);
    });
  });

  describe('fromPrefixLen', () => {
    it('makes IPv4 netmask', () => {
      expect(ip.fromPrefixLen(8)).toBe('255.0.0.0');
    });
    it('makes IPv6 netmask', () => {
      expect(ip.fromPrefixLen(32, 6)).toContain('ffff');
    });
    it('makes IPv6 netmask auto from large prefix', () => {
      expect(ip.fromPrefixLen(132)).toContain(':');
    });
  });
});