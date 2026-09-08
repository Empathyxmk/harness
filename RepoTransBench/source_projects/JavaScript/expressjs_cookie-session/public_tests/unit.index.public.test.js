// Public counterpart for test/unit.index.test.js
const cookieSession = require('../index');

describe('index.js (public)', () => {
  it('should export a function type (using toEqual)', () => {
    expect(typeof cookieSession).toEqual('function');
  });
});