// Migrated simple coverage test for Redis set/get with more key types
const redis = require('redis');

describe('test.js migrated', () => {
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

  test('Can store and retrieve integers', done => {
    client.set("NumKey", 42, (err, res) => {
      expect(err).toBeNull();
      expect(res).toBe('OK');
      client.get("NumKey", (err2, reply) => {
        expect(err2).toBeNull();
        expect(reply).toBe("42");
        done();
      });
    });
  });

  test('Can increment values', done => {
    client.set("Counter", 10, () => {
      client.incr("Counter", (err, val) => {
        expect(err).toBeNull();
        expect(val).toBe(11);
        done();
      });
    });
  });

  test('Handles list operations: lpush/rpush/lrange', done => {
    client.del("mylist", () => {
      client.lpush("mylist", "a", "b", "c", (err, len) => {
        expect(err).toBeNull();
        expect(len).toBeGreaterThan(0);
        client.rpush("mylist", "x", (err2) => {
          expect(err2).toBeNull();
          client.lrange("mylist", 0, -1, (err3, list) => {
            expect(list).toContain("a");
            expect(list).toContain("x");
            done();
          });
        });
      });
    });
  });
});