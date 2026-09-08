const ip = require('../lib/ip');
const { Buffer } = require('buffer');

describe('ip.js - Basic methods (Public Tests)', () => {
  describe('IPv4 toBuffer and toString', () => {
    it('should convert IPv4 string to Buffer and back', () => {
      const buf = ip.toBuffer('8.8.4.4');
      expect(buf.toString('hex')).toBe('08080404');
      expect(ip.toString(buf)).toBe('8.8.4.4');
    });
    it('should convert IPv4 in-place', () => {
      const buf = Buffer.alloc(10);
      ip.toBuffer('100.101.102.103', buf, 3);
      expect(buf.toString('hex', 3, 7)).toBe('64656667');
      expect(ip.toString(buf, 3, 4)).toBe('100.101.102.103');
    });
  });

  describe('IPv6 toBuffer and toString', () => {
    it('should convert IPv6 string to Buffer and back', () => {
      const buf = ip.toBuffer('1234:0:0:0:0:0:0:2');
      expect(buf.length).toBe(16);
      expect(['1234:0:0:0:0:0:0:2', '1234::2']).toContain(ip.toString(buf));
    });
    it('should handle abbreviated IPv6', () => {
      const buf = ip.toBuffer('beef::3');
      expect(ip.toString(buf)).toContain('beef');
    });
    it('should convert IPv6 with embedded IPv4', () => {
      const buf = ip.toBuffer('::ffff:203.0.113.1');
      expect(ip.toString(buf)).toContain('ffff');
    });
    it('should convert IPv6 in-place', () => {
      const buf = Buffer.alloc(32);
      ip.toBuffer('2::', buf, 6);
      expect(ip.toString(buf, 6, 16)).toBe('2::');
    });
  });

  describe('input validation', () => {
    it('throws for invalid input', () => {
      expect(() => ip.toBuffer('bad.input')).toThrow();
    });
  });

  describe('isV4Format', () => {
    it('detects v4', () => {
      expect(ip.isV4Format('1.2.3.4')).toBe(true);
      expect(ip.isV4Format('1.2.3')).toBe(false);
      expect(ip.isV4Format('beef::2')).toBe(false);
    });
  });

  describe('isV6Format', () => {
    it('detects v6', () => {
      expect(ip.isV6Format('cafe::4')).toBe(true);
      expect(ip.isV6Format('8.8.4.4')).toBe(true); // as per implementation detail
      expect(ip.isV6Format('cafe::')).toBe(true);
    });
  });

  describe('fromPrefixLen', () => {
    it('makes IPv4 netmask', () => {
      expect(ip.fromPrefixLen(16)).toBe('255.255.0.0');
    });
    it('makes IPv6 netmask', () => {
      expect(ip.fromPrefixLen(48, 6)).toContain('ffff');
    });
    it('makes IPv6 netmask auto from large prefix', () => {
      expect(ip.fromPrefixLen(140)).toContain(':');
    });
  });
});