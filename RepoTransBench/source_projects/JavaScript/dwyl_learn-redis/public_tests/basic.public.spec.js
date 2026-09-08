// Public variant: use different string/key/value names
const redis = require('redis');

describe('[PUBLIC] basic.spec.js variant', () => {
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

  test('Set and get works for alternate string values', done => {
    client.set("Alpha", "Beta", function(err, res) {
      expect(err).toBeNull();
      expect(res).toBe("OK");
      client.get("Alpha", function(err2, reply) {
        expect(err2).toBeNull();
        expect(reply).toBe("Beta");
        done();
      });
    });
  });

  test('Del returns 1 or 0 for a new key', done => {
    client.set("TempToDelete", "TmpVal", function() {
      client.del("TempToDelete", function(err, res) {
        expect(err).toBeNull();
        expect(res === 1 || res === 0).toBeTruthy();
        done();
      });
    });
  });

  test('Returns null for someother non-existent key', done => {
    client.get("SomeKeyThatIsNotSet", function(err, reply) {
      expect(err).toBeNull();
      expect(reply).toBeNull();
      done();
    });
  });
});