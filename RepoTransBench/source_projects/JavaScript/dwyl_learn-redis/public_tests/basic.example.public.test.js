const redis = require('redis');

describe('[PUBLIC] Basic Example with different data', () => {
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

  test('set and get Foo', done => {
    client.set("Foo", "Bar", (setErr, setReply) => {
      expect(setErr).toBeNull();
      expect(setReply).toBe('OK');
      client.get("Foo", (getErr, reply) => {
        expect(getErr).toBeNull();
        expect(reply).toBe("Bar");
        done();
      });
    });
  });

  test('get on different missing key returns null', done => {
    client.del("DefinitelyMissingKey", () => {
      client.get("DefinitelyMissingKey", (err, reply) => {
        expect(err).toBeNull();
        expect(reply).toBeNull();
        done();
      });
    });
  });

  test('redis.print callback output remains undefined with new args', done => {
    const cb = redis.print;
    expect(cb("randomError", "randomReply")).toBe(undefined);
    done();
  });
});