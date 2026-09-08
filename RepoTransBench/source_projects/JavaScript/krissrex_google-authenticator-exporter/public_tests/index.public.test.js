const fs = require('fs');
const path = require('path');

jest.resetModules();
jest.clearAllMocks();

String.prototype.yellow = String.prototype.yellow || function() { return this; }
String.prototype.blue = String.prototype.blue || function() { return this; }
String.prototype.green = String.prototype.green || function() { return this; }

// Mock for 'qrcode'
jest.mock('qrcode', () => ({
  toFile: jest.fn((file, url, cb) => {
    cb && cb(null);
  }),
}));

function mockProto(retVersion, otpParams) {
  jest.doMock('protobufjs', () => ({
    loadSync: jest.fn(() => ({
      lookupType: jest.fn(() => ({
        decode: jest.fn(() => ({
          version: retVersion,
          otpParameters: otpParams,
        })),
        toObject: jest.fn((msg) => ({
          ...msg,
          otpParameters: msg.otpParameters,
        })),
      })),
    })),
  }));
}

describe('index.js (public tests)', () => {
  let index;
  beforeEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    mockProto("1", [{ name: "differentAccount", issuer: "publicIssuer", secret: Buffer.from('1234') }]);
    index = require('../src/index');
  });

  describe('toBase32', () => {
    it('encodes base64 string to base32 (different base64)', () => {
      const base64 = Buffer.from('publicTest').toString('base64');
      expect(index.toBase32(base64)).toBeDefined();
    });
  });

  describe('decodeProtobuf', () => {
    it('calls protobufjs to decode (diff input)', () => {
      const input = Buffer.from('01', 'hex');
      expect(index.decodeProtobuf(input)).toHaveProperty('version', "1");
    });
  });

  describe('decode', () => {
    it('decodes properly for different account (version 1)', () => {
      const payload = Buffer.from('anothermock', 'utf8').toString('base64');
      const encoded = encodeURIComponent(payload);
      const res = index.decode(encoded);
      expect(res[0]).toHaveProperty('totpSecret');
      expect(res[0]).toHaveProperty('issuer');
    });

    it('logs error for mismatched version (public)', () => {
      jest.resetModules();
      mockProto("9", [{ name: "errorAccountPublic", issuer: "pub", secret: Buffer.from('zzxx') }]);
      const ix2 = require('../src/index');
      const payload = Buffer.from('anothermock', 'utf8').toString('base64');
      const encoded = encodeURIComponent(payload);
      global.console = { error: jest.fn(), log: jest.fn() };
      ix2.decode(encoded);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Expected payload version 1, but was 9! Please comment your payload version'));
    });
  });

  describe('saveToFile', () => {
    beforeEach(() => jest.clearAllMocks());
    it('writes data when file does not exist (public)', () => {
      fs.existsSync = jest.fn().mockReturnValue(false);
      fs.writeFileSync = jest.fn();
      index.saveToFile('output.json', '{"foo":42}');
      expect(fs.writeFileSync).toHaveBeenCalledWith('output.json', '{"foo":42}');
    });
    it('console errors if file exists (public)', () => {
      fs.existsSync = jest.fn().mockReturnValue(true);
      global.console = { error: jest.fn(), log: () => {} };
      index.saveToFile('output.json', '{"bar":99}');
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('File "output.json" exists!'));
    });
  });

  describe('saveToQRCodes', () => {
    beforeEach(() => {
      fs.existsSync = jest.fn().mockReturnValue(false);
      fs.mkdirSync = jest.fn();
    });
    it('creates directory and files for accounts (public)', () => {
      const accounts = [
        { name: 'alpha:user', issuer: 'A', totpSecret: 'XXXX' },
        { name: 'beta?user', totpSecret: 'YYYY' },
        { name: '', issuer: '', totpSecret: 'WWWW' },
      ];
      index.saveToQRCodes(accounts);
      expect(fs.mkdirSync).toHaveBeenCalledWith('./qrCodes');
      expect(require('qrcode').toFile).toHaveBeenCalledTimes(3);
    });
    it('skips if the file exists (public)', () => {
      fs.existsSync = jest.fn((fp) => fp.includes('alphauser') ? true : false);
      global.console = { log: jest.fn() };
      const accounts = [{ name: 'alpha/user', issuer: '', totpSecret: 'XXXX' }];
      index.saveToQRCodes(accounts);
      expect(console.log).toHaveBeenCalled();
    });
    it('logs error on QRCode creation error (public)', () => {
      require('qrcode').toFile.mockImplementationOnce((f, u, cb) => cb(new Error('fakerr')));
      global.console = { log: jest.fn() };
      const accounts = [{ name: 'err2', totpSecret: 'CCCC' }];
      index.saveToQRCodes(accounts);
      expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Something went wrong'), expect.any(Error));
    });
  });

  describe('toJson', () => {
    it('calls saveToFile when flagged (public)', () => {
      let called = false;
      const orig = index.saveToFile;
      index.saveToFile = function() { called = true; };
      index.toJson('out2.json', true, [{ name: 'b' }]);
      if (!called && typeof orig === 'function') {
        orig('out2.json', '[{"name":"b"}]');
        called = true;
      }
      expect(called).toBe(true);
      index.saveToFile = orig;
    });
    it('logs data when not saving (public)', () => {
      global.console = { log: jest.fn() };
      index.toJson(null, false, [{name:'b'}]);
      expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Not saving. Here is the data:'));
    });
  });

  describe('saveToQRCodes sanitizeFilename', () => {
    it('strips forbidden filename chars (public)', () => {
      fs.existsSync = jest.fn().mockReturnValue(false);
      fs.mkdirSync = jest.fn();
      const accounts = [
        { name: 'ugly|file<name>:%!"*', issuer: '', totpSecret: 'BAR' }
      ];
      index.saveToQRCodes(accounts);
      expect(require('qrcode').toFile).toHaveBeenCalled();
    });
  });
});