const googl = require('../lib/googl.js');
const assert = require('assert');

describe('getKey/setKey', function() {
  it('should store and retrieve the API key', function() {
    assert.strictEqual(googl.setKey('TEST'), 'TEST');
    assert.strictEqual(googl.getKey(), 'TEST');
    assert.strictEqual(googl.setKey(''), '');
    assert.strictEqual(googl.getKey(), '');
  });
});