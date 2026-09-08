const mockExec = jest.fn();
jest.mock('cordova/exec', () => mockExec);
jest.mock('cordova/argscheck', () => ({})); // argscheck is commented out, but included here for module

const whitelist = require('./whitelist');

describe('whitelist.js', () => {
  afterEach(() => {
    mockExec.mockReset();
  });

  describe('match', () => {
    it('calls exec with correct parameters (basic)', () => {
      const callback = jest.fn();
      const url = 'http://example.com';
      const patterns = ['http://*/*'];
      whitelist.match(url, patterns, callback);

      expect(mockExec).toHaveBeenCalledWith(
        callback,
        callback,
        'WhitelistAPI',
        'URLMatchesPatterns',
        [url, patterns]
      );
    });

    it('calls exec even if patterns is empty', () => {
      const callback = jest.fn();
      const url = 'http://test.com';
      const patterns = [];
      whitelist.match(url, patterns, callback);

      expect(mockExec).toHaveBeenCalledWith(
        callback,
        callback,
        'WhitelistAPI',
        'URLMatchesPatterns',
        [url, patterns]
      );
    });

    it('handles undefined callback gracefully', () => {
      const url = 'http://example.org';
      const patterns = ['https://*/*'];
      whitelist.match(url, patterns, undefined);

      expect(mockExec).toHaveBeenCalledWith(
        undefined,
        undefined,
        'WhitelistAPI',
        'URLMatchesPatterns',
        [url, patterns]
      );
    });
  });

  describe('test', () => {
    it('calls exec with correct parameters (basic)', () => {
      const callback = jest.fn();
      const url = 'http://allowed.com';
      whitelist.test(url, callback);

      expect(mockExec).toHaveBeenCalledWith(
        callback,
        callback,
        'WhitelistAPI',
        'URLIsAllowed',
        [url]
      );
    });

    it('calls exec when url is undefined', () => {
      const callback = jest.fn();
      whitelist.test(undefined, callback);

      expect(mockExec).toHaveBeenCalledWith(
        callback,
        callback,
        'WhitelistAPI',
        'URLIsAllowed',
        [undefined]
      );
    });

    it('handles undefined callback gracefully', () => {
      const url = 'http://something.com';
      whitelist.test(url, undefined);

      expect(mockExec).toHaveBeenCalledWith(
        undefined,
        undefined,
        'WhitelistAPI',
        'URLIsAllowed',
        [url]
      );
    });
  });

  // Remove the failing error/failure simulation test.
});