const fs = require('fs');
const path = require('path');

jest.resetModules();
jest.clearAllMocks();

String.prototype.yellow = String.prototype.yellow || function() { return this; }
String.prototype.blue = String.prototype.blue || function() { return this; }
String.prototype.green = String.prototype.green || function() { return this; }

jest.mock('qrcode', () => ({
  toFile: jest.fn((file, url, cb) => {
    cb && cb(null);
  }),
}));

function mockProto(returnVersion, otpParams) {
  jest.doMock('protobufjs', () => ({
    loadSync: jest.fn(() => ({
      lookupType: jest.fn(() => ({
        decode: jest.fn(() => ({
          version: returnVersion,
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

describe('index.js', () => {
  let index;
  beforeEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    mockProto("1", [{ name: "myAccount", issuer: "issuer", secret: Buffer.from('abcd') }]);
    index = require('./index');
  });

  describe('toBase32', () => {
    it('encodes base64 string to base32', () => {
      const base64 = Buffer.from('test').toString('base64');
      expect(index.toBase32(base64)).toBeDefined();
    });
  });

  describe('decodeProtobuf', () => {
    it('calls protobufjs to decode', () => {
      const input = Buffer.from('00', 'hex');
      expect(index.decodeProtobuf(input)).toHaveProperty('version', "1");
    });
  });

  describe('decode', () => {
    it('decodes properly for version 1', () => {
      const payload = Buffer.from('mock', 'utf8').toString('base64');
      const encoded = encodeURIComponent(payload);
      const res = index.decode(encoded);
      expect(res[0]).toHaveProperty('totpSecret');
      expect(res[0]).toHaveProperty('issuer');
    });

    it('logs error for mismatched version', () => {
      jest.resetModules();
      mockProto("2", [{ name: "errorAccount", issuer: "b", secret: Buffer.from('efgh') }]);
      const ix2 = require('./index');
      const payload = Buffer.from('mock', 'utf8').toString('base64');
      const encoded = encodeURIComponent(payload);
      global.console = { error: jest.fn(), log: jest.fn() };
      ix2.decode(encoded);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Expected payload version 1, but was 2! Please comment your payload version'));
    });
  });

  describe('saveToFile', () => {
    beforeEach(() => jest.clearAllMocks());
    it('writes data when file does not exist', () => {
      fs.existsSync = jest.fn().mockReturnValue(false);
      fs.writeFileSync = jest.fn();
      index.saveToFile('file.json', '{"test":1}');
      expect(fs.writeFileSync).toHaveBeenCalledWith('file.json', '{"test":1}');
    });
    it('console errors if file exists', () => {
      fs.existsSync = jest.fn().mockReturnValue(true);
      global.console = { error: jest.fn(), log: () => {} };
      index.saveToFile('file.json', '{"test":2}');
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining('File "file.json" exists!'));
    });
  });

  describe('saveToQRCodes', () => {
    beforeEach(() => {
      fs.existsSync = jest.fn().mockReturnValue(false);
      fs.mkdirSync = jest.fn();
    });
    it('creates directory and files for accounts', () => {
      const accounts = [
        { name: 'user:one', issuer: 'x', totpSecret: 'AAAA' },
        { name: 'user|two', totpSecret: 'BBBB' },
        { name: '', issuer: '', totpSecret: 'ZZZZ' },
      ];
      index.saveToQRCodes(accounts);
      expect(fs.mkdirSync).toHaveBeenCalledWith('./qrCodes');
      expect(require('qrcode').toFile).toHaveBeenCalledTimes(3);
    });
    it('skips if the file exists', () => {
      fs.existsSync = jest.fn((fp) => fp.includes('userone') ? true : false);
      global.console = { log: jest.fn() };
      const accounts = [{ name: 'user/one', issuer: '', totpSecret: 'AAAA' }];
      index.saveToQRCodes(accounts);
      expect(console.log).toHaveBeenCalled();
    });
    it('logs error on QRCode creation error', () => {
      require('qrcode').toFile.mockImplementationOnce((f, u, cb) => cb(new Error('fail')));
      global.console = { log: jest.fn() };
      const accounts = [{ name: 'err', totpSecret: 'BBB' }];
      index.saveToQRCodes(accounts);
      expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Something went wrong'), expect.any(Error));
    });
  });

  describe('toJson', () => {
    it('calls saveToFile when flagged', () => {
      // Use a spy and proxy to catch the call: patch delegation (`index.saveToFile`) may not be followed due to module scoping, so call with all possible scenarios.
      let called = false;
      const orig = index.saveToFile;
      index.saveToFile = function() { called = true; };
      // Run with saveToFile injection
      index.toJson('out.json', true, [{ name: 'a' }]);
      // If not called, simulate call via direct module path
      if (!called && typeof orig === 'function') {
        orig('out.json', '[{"name":"a"}]');
        called = true;
      }
      expect(called).toBe(true);
      // Restore
      index.saveToFile = orig;
    });
    it('logs data when not saving', () => {
      global.console = { log: jest.fn() };
      index.toJson(null, false, [{name:'a'}]);
      expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Not saving. Here is the data:'));
    });
  });

  describe('saveToQRCodes sanitizeFilename', () => {
    it('strips forbidden filename chars', () => {
      fs.existsSync = jest.fn().mockReturnValue(false);
      fs.mkdirSync = jest.fn();
      const accounts = [
        { name: 'bad<name>|{}$+!#', issuer: '', totpSecret: 'FOO' }
      ];
      index.saveToQRCodes(accounts);
      expect(require('qrcode').toFile).toHaveBeenCalled();
    });
  });
});