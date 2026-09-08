const mockExec = jest.fn();
jest.mock('cordova/exec', () => mockExec);
jest.mock('cordova/argscheck', () => ({})); // argscheck stub

const whitelist = require('../whitelist');

describe('whitelist.js (public)', () => {
  afterEach(() => {
    mockExec.mockReset();
  });

  describe('match', () => {
    it('calls exec with different url and patterns', () => {
      const callback = jest.fn();
      const url = 'https://publictest.org';
      const patterns = ['https://*/*', 'http://allowed.org/*'];
      whitelist.match(url, patterns, callback);

      expect(mockExec).toHaveBeenCalledWith(
        callback,
        callback,
        'WhitelistAPI',
        'URLMatchesPatterns',
        [url, patterns]
      );
    });

    it('calls exec with empty patterns and different url', () => {
      const callback = jest.fn();
      const url = 'https://newsite.io';
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

    it('handles undefined callback gracefully with different values', () => {
      const url = 'ftp://example.net';
      const patterns = ['ftp://*/*'];
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
    it('calls exec with different url', () => {
      const callback = jest.fn();
      const url = 'https://newallowed.com';
      whitelist.test(url, callback);

      expect(mockExec).toHaveBeenCalledWith(
        callback,
        callback,
        'WhitelistAPI',
        'URLIsAllowed',
        [url]
      );
    });

    it('calls exec when url is null', () => {
      const callback = jest.fn();
      whitelist.test(null, callback);

      expect(mockExec).toHaveBeenCalledWith(
        callback,
        callback,
        'WhitelistAPI',
        'URLIsAllowed',
        [null]
      );
    });

    it('handles undefined callback gracefully with different url', () => {
      const url = 'https://anotherurl.org';
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
});