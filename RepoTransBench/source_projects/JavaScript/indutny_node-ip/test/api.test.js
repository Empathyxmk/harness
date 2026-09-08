const ip = require('../lib/ip');
const { Buffer } = require('buffer');

describe('ip.js - Basic methods', () => {
  describe('IPv4 toBuffer and toString', () => {
    it('should convert IPv4 string to Buffer and back', () => {
      const buf = ip.toBuffer('192.168.0.1');
      expect(buf.toString('hex')).toBe('c0a80001');
      expect(ip.toString(buf)).toBe('192.168.0.1');
    });
    it('should convert IPv4 in-place', () => {
      const buf = Buffer.alloc(10);
      ip.toBuffer('10.11.12.13', buf, 2);
      expect(buf.toString('hex', 2, 6)).toBe('0a0b0c0d');
      expect(ip.toString(buf, 2, 4)).toBe('10.11.12.13');
    });
  });

  describe('IPv6 toBuffer and toString', () => {
    it('should convert IPv6 string to Buffer and back', () => {
      const buf = ip.toBuffer('abcd:0:0:0:0:0:0:1');
      expect(buf.length).toBe(16);
      // The library abbreviates correctly, so check both forms
      expect(['abcd:0:0:0:0:0:0:1', 'abcd::1']).toContain(ip.toString(buf));
    });
    it('should handle abbreviated IPv6', () => {
      const buf = ip.toBuffer('abcd::1');
      expect(ip.toString(buf)).toContain('abcd');
    });
    it('should convert IPv6 with embedded IPv4', () => {
      const buf = ip.toBuffer('::ffff:192.0.2.128');
      expect(ip.toString(buf)).toContain('ffff');
    });
    it('should convert IPv6 in-place', () => {
      const buf = Buffer.alloc(32);
      ip.toBuffer('1::', buf, 4);
      expect(ip.toString(buf, 4, 16)).toBe('1::');
    });
  });

  describe('input validation', () => {
    it('throws for invalid input', () => {
      expect(() => ip.toBuffer('not.an.ip')).toThrow();
    });
  });

  describe('isV4Format', () => {
    it('detects v4', () => {
      expect(ip.isV4Format('10.0.0.1')).toBe(true);
      expect(ip.isV4Format('10.0.0')).toBe(false);
      expect(ip.isV4Format('abcd::1')).toBe(false);
    });
  });

  describe('isV6Format', () => {
    it('detects v6', () => {
      expect(ip.isV6Format('abcd::1')).toBe(true);
      expect(ip.isV6Format('10.0.0.1')).toBe(true); // matches the regex in ip.js, so it returns true
      expect(ip.isV6Format('abcd::')).toBe(true);
    });
  });

  describe('fromPrefixLen', () => {
    it('makes IPv4 netmask', () => {
      expect(ip.fromPrefixLen(24)).toBe('255.255.255.0');
    });
    it('makes IPv6 netmask', () => {
      expect(ip.fromPrefixLen(64, 6)).toContain('ffff');
    });
    it('makes IPv6 netmask auto from large prefix', () => {
      expect(ip.fromPrefixLen(129)).toContain(':');
    });
  });
});