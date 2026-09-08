// Public counterpart for test/cookie-session.spec.js
const http = require('http');
const cookieSession = require('../index');

// Different test but same logic: check if not undefined/null
describe('cookie-session (public)', () => {
  it('should export a non-null value', () => {
    expect(cookieSession).not.toBeNull();
  });

  // Placeholder for further public tests
});