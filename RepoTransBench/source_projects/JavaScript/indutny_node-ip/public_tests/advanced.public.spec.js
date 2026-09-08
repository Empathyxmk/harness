const ip = require('../lib/ip');

describe('ip.js - Advanced and less common functionality (Public Tests)', () => {
  describe('mask', () => {
    it('correctly masks IPv4', () => {
      expect(ip.mask('203.0.113.25', '255.255.255.240')).toBe('203.0.113.16');
      expect(ip.mask('172.16.5.7', '255.255.0.0')).toBe('172.16.0.0');
    });

    it('correctly masks IPv6', () => {
      expect(ip.mask('fe80::abcd', 'ffff:ffff:ff00::')).toContain('fe80');
    });
  });

  describe('not', () => {
    it('correctly inverts IPv4', () => {
      expect(ip.not('255.255.255.255')).toBe('0.0.0.0');
      expect(ip.not('128.0.0.0')).toBe('127.255.255.255');
    });
    it('correctly inverts IPv6', () => {
      expect(ip.not('abcd::1234')).toMatch(/^[\da-f:]+$/i);
    });
  });

  describe('or', () => {
    it('bitwise OR for IPv4', () => {
      expect(ip.or('203.0.113.10', '255.255.255.240')).toBe('255.255.255.250');
    });
    it('bitwise OR for IPv6', () => {
      expect(ip.or('::2', '::f0f0')).toMatch(/2|f0f0/i);
    });
  });

  describe('subnet', () => {
    it('creates subnet for IPv4', () => {
      const res = ip.subnet('203.0.113.25', '255.255.255.240');
      expect(res.networkAddress).toBe('203.0.113.16');
      expect(res.broadcastAddress).toBe('203.0.113.31');
      expect(res.contains('203.0.113.30')).toBe(true);
      expect(res.contains('203.0.113.32')).toBe(false);
    });

    it('creates subnet for IPv6', () => {
      const res = ip.subnet('fe80::', 'ffff:ffff:ff00::');
      expect(typeof res.networkAddress).toBe('string');
      expect(res.contains('fe80::f00d')).toBe(true);
    });
  });

  describe('cidrSubnet', () => {
    it('creates subnet from cidr for IPv4', () => {
      const res = ip.cidrSubnet('203.0.113.25/28');
      expect(res.networkAddress).toBe('203.0.113.16');
      expect(res.broadcastAddress).toBe('203.0.113.31');
      expect(res.contains('203.0.113.17')).toBe(true);
      expect(res.contains('203.0.113.44')).toBe(false);
    });
    it('creates subnet from cidr for IPv6', () => {
      const res = ip.cidrSubnet('fe80::/56');
      expect(typeof res.networkAddress).toBe('string');
      expect(res.contains('fe80::babe')).toBe(true);
    });
  });

  describe('cidr and isEqual', () => {
    it('returns network address for IPv4', () => {
      expect(ip.cidr('203.0.113.25/28')).toBe('203.0.113.16');
    });
    it('returns network address for IPv6', () => {
      const res = ip.cidr('fe80::2/56');
      expect(typeof res).toBe('string');
    });
    it('isEqual returns true for equal', () => {
      expect(ip.isEqual('203.0.113.25', '203.0.113.25')).toBe(true);
      expect(ip.isEqual('fe80::1', 'fe80::1')).toBe(true);
    });
    it('isEqual returns false for not equal', () => {
      expect(ip.isEqual('203.0.113.25', '203.0.113.26')).toBe(false);
      expect(ip.isEqual('fe80::1', 'fe80::2')).toBe(false);
    });
  });

  describe('calculate CIDR length and range', () => {
    it('returns subnet info', () => {
      expect(ip.cidrSubnet('10.0.0.1/12').subnetMaskLength).toBe(12);
    });
    it('range for IPv4', () => {
      expect(Array.isArray(ip.cidrSubnet('10.0.0.1/20').subnetMask)).toBe(false);
    });
  });

  describe('loopback', () => {
    it('returns loopback v4', () => {
      expect(ip.loopback('ipv4')).toBe('127.0.0.1');
    });
    it('returns loopback v6', () => {
      expect(["::1","fe80::1"]).toContain(ip.loopback('ipv6'));
    });
    it('defaults to ipv4', () => {
      expect(ip.loopback()).toBe('127.0.0.1');
    });
  });

  describe('address', () => {
    it('returns a valid address (string)', () => {
      const addr = ip.address();
      expect(typeof addr).toBe('string');
    });
  });

  describe('toLong/toString', () => {
    it('converts IPv4 to long and back', () => {
      const str = '10.1.2.3';
      const longVal = ip.toLong(str);
      expect(ip.fromLong(longVal)).toBe(str);
    });
  });
});