// public_tests/test.public.js
// Public test: different values for redis integer/list tests

const redis = require("redis");
const client = redis.createClient();
const util = require("util");

beforeAll(done => {
  client.on("ready", done);
});
afterAll(done => {
  client.quit(done);
});

describe("[PUBLIC] test.js migrated with alternate data", () => {

  test("Can store and retrieve integers with different keys", done => {
    client.set("num_users_public", 2024, (err, reply) => {
      expect(err).toBeNull();
      client.get("num_users_public", (err, value) => {
        expect(Number(value)).toBe(2024);
        done();
      });
    });
  });

  test("Can increment values with new key", done => {
    client.set("views_public", 101, (err, reply) => {
      client.incr("views_public", (err, value) => {
        expect(value).toBe(102);
        client.incr("views_public", (err, value) => {
          expect(value).toBe(103);
          done();
        });
      });
    });
  });

  test("Handles list operations: lpush/rpush/lrange with public data", done => {
    client.del("queue_public", () => {
      client.lpush("queue_public", "taskC", (err, l) => {
        client.rpush("queue_public", "taskD", (err, l) => {
          client.lrange("queue_public", 0, -1, (err, list) => {
            expect(list).toEqual(["taskC", "taskD"]);
            done();
          });
        });
      });
    });
  });
});