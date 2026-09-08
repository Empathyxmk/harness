"use strict";

const assert = require("assert");
const Keygrip = require("..");

// Test static methods throw as documented
describe("Keygrip static method error throws - public", function () {
  it("Keygrip.sign throws on static invocation", () => {
    assert.throws(() => Keygrip.sign("public"), /Usage: require\('keygrip'\)\(<array-of-keys>\)/);
  });

  it("Keygrip.verify throws on static invocation", () => {
    assert.throws(() => Keygrip.verify("value"), /Usage: require\('keygrip'\)\(<array-of-keys>\)/);
  });

  it("Keygrip.index throws on static invocation", () => {
    assert.throws(() => Keygrip.index(123), /Usage: require\('keygrip'\)\(<array-of-keys>\)/);
  });
});

// Additional edge-case tests for constructor and instance methods
describe("Keygrip class edge and args checks - public", function () {
  it("constructor throws if given empty string keys", function () {
    assert.throws(() => new Keygrip(""), /Keys must be provided/);
  });

  it("constructor throws if given 0 as keys", function () {
    assert.throws(() => new Keygrip(0), /Keys must be provided/);
  });

  it("constructor throws if key array is undefined slot ([,,])", function () {
    assert.throws(() => new Keygrip([,,]), /Keys must be provided/);
  });

  it("constructor works when keys is an array with a non-empty string", function () {
    const keys = new Keygrip(["publicKey"]);
    assert.ok(keys instanceof Keygrip);
  });

  it("sign/verify with non-empty string key produces value", function () {
    const keys = new Keygrip(["publicKey"]);
    const data = "data-test";
    const sig = keys.sign(data);
    assert.strictEqual(typeof sig, "string");
    // verify always fails with incorrect signature
    assert.strictEqual(keys.verify(data, "wrong-digest"), false);
  });

  it("sign/verify with special chars in data", function () {
    const keys = new Keygrip(["DIFFERENT-SECRET"]);
    const data = "\x01💥bar!=...";
    const signature = keys.sign(data);
    assert(keys.verify(data, signature));
  });

  it("verify returns false with undefined digest", function () {
    const keys = new Keygrip(["DIFFERENT-SECRET"]);
    assert.strictEqual(keys.verify("another", undefined), false);
  });

  it("index returns -1 when digest is falsy (empty string)", function () {
    const keys = new Keygrip(["DIFFERENT-SECRET"]);
    assert.strictEqual(keys.index("another", ""), -1);
    assert.strictEqual(keys.index("another", 0), -1);
  });
});