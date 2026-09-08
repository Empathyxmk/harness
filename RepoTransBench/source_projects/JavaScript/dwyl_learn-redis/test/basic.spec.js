// Migrated from tape to jest for compatibility and coverage
const redis = require('redis');

describe('basic.spec.js migrated', () => {
  let client;

  beforeAll(done => {
    client = redis.createClient();
    client.on('ready', done);
    client.on('error', err => {
      done(err);
    });
  });

  afterAll(done => {
    client.quit(() => done());
  });

  test('Set and get works for string values', done => {
    client.set("Hello", "World", function(err, res) {
      expect(err).toBeNull();
      expect(res).toBe("OK");
      client.get("Hello", function(err2, reply) {
        expect(err2).toBeNull();
        expect(reply).toBe("World");
        done();
      });
    });
  });

  test('Del returns 1 or 0 depending on existing key', done => {
    client.set("DeleteMe", "SomeValue", function() {
      client.del("DeleteMe", function(err, res) {
        expect(err).toBeNull();
        expect(res === 1 || res === 0).toBeTruthy();
        done();
      });
    });
  });

  test('Returns null for non-existent key', done => {
    client.get("KeyThatDoesNotExist", function(err, reply) {
      expect(err).toBeNull();
      expect(reply).toBeNull();
      done();
    });
  });
});