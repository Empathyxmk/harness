const redis = require('redis');
const assert = require('assert');

describe('Basic Example: examples/basic.js', () => {
  let client;

  beforeAll(done => {
    client = redis.createClient();
    client.on('ready', done);
    client.on('error', err => {
      // handle redis error in tests
      done(err);
    });
  });

  afterAll(done => {
    client.quit(() => done());
  });

  test('set and get Hello', done => {
    client.set("Hello", "World", (setErr, setReply) => {
      expect(setErr).toBeNull();
      expect(setReply).toBe('OK');
      client.get("Hello", (getErr, reply) => {
        expect(getErr).toBeNull();
        expect(reply).toBe("World");
        done();
      });
    });
  });

  test('get on missing key returns null', done => {
    client.del("NoSuchKey", () => {
      client.get("NoSuchKey", (err, reply) => {
        expect(err).toBeNull();
        expect(reply).toBeNull();
        done();
      });
    });
  });

  test('redis.print callback output returns undefined', done => {
    const cb = redis.print;
    expect(cb("err", "reply")).toBe(undefined);
    done();
  });
});