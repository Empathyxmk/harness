"use strict";

const assert = require("assert");
const Keygrip = require("..");

// Test static methods throw as documented
describe("Keygrip static method error throws", function () {
  it("Keygrip.sign throws on static invocation", () => {
    assert.throws(() => Keygrip.sign(), /Usage: require\('keygrip'\)\(<array-of-keys>\)/);
  });

  it("Keygrip.verify throws on static invocation", () => {
    assert.throws(() => Keygrip.verify(), /Usage: require\('keygrip'\)\(<array-of-keys>\)/);
  });

  it("Keygrip.index throws on static invocation", () => {
    assert.throws(() => Keygrip.index(), /Usage: require\('keygrip'\)\(<array-of-keys>\)/);
  });
});

// Additional edge-case tests for constructor and instance methods
describe("Keygrip class edge and args checks", function () {
  it("constructor throws if given null keys", function () {
    assert.throws(() => new Keygrip(null), /Keys must be provided/);
  });

  it("constructor throws if given undefined keys", function () {
    assert.throws(() => new Keygrip(undefined), /Keys must be provided/);
  });

  it("constructor throws if key array is sparse ([,])", function () {
    assert.throws(() => new Keygrip([,]), /Keys must be provided/);
  });

  it("constructor works when keys is an array with empty string", function () {
    const keys = new Keygrip([""]);
    assert.ok(keys instanceof Keygrip);
  });

  it("sign/verify with empty string key produces value", function () {
    const keys = new Keygrip([""]);
    const data = "test";
    const sig = keys.sign(data);
    assert.strictEqual(typeof sig, "string");
    // verify always fails with incorrect signature
    assert.strictEqual(keys.verify(data, "bad-digest"), false);
  });

  it("sign/verify with unusual chars in data", function () {
    const keys = new Keygrip(["SEKRIT"]);
    const data = "\0🔥foo=/+=";
    const signature = keys.sign(data);
    assert(keys.verify(data, signature));
  });

  it("verify returns false with empty digest", function () {
    const keys = new Keygrip(["SEKRIT"]);
    assert.strictEqual(keys.verify("anything", ""), false);
  });

  it("index returns -1 when digest is falsy", function () {
    const keys = new Keygrip(["SEKRIT"]);
    assert.strictEqual(keys.index("anything", null), -1);
    assert.strictEqual(keys.index("anything", undefined), -1);
  });
});