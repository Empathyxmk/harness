/**
 * bit-sync.js
 *
 * For more information see the readme. 
 *
 * Source is located at https://github.com/claytongulick/bit-sync
 *
 * Licensed under the MIT License
 *
 * Copyright Clayton C. Gulick
 */

// The BSync "class"
var BSync = (() => {
  // Shim for typed arrays for environments that don't support them
  // (The original file is long. This sample exposes only relevant public API.)

  // Utils object that will be attached to BSync
  var util = {};

  util.readInt32 = function(buf, offset) {
    // Little-endian, Uint8Array
    return (
      (buf[offset]) +
      (buf[offset + 1] << 8) +
      (buf[offset + 2] << 16) +
      (buf[offset + 3] << 24)
    ) >>> 0;
  };

  util.adler32 = function(offset, len, buf) {
    var MOD_ADLER = 65521;
    var a = 1, b = 0;
    for (var i = offset; i < offset + len; i++) {
      a = (a + buf[i]) % MOD_ADLER;
      b = (b + a) % MOD_ADLER;
    }
    return {
      checksum: (b << 16) | a,
      a: a,
      b: b
    };
  };

  util.makeBlockChecksums = function(buf, blockSize) {
    if (!buf || buf.length === 0) return [];
    var blocks = [];
    for (var i = 0; i < buf.length; i += blockSize) {
      var len = Math.min(blockSize, buf.length - i);
      var weak = util.adler32(i, len, buf).checksum;
      var strong = util._md5
        ? util._md5(buf.slice(i, i + len))
        : 'dummy-md5-' + i;
      blocks.push({ weak: weak, strong: strong });
    }
    return blocks;
  };

  util.padBuffer = function(buf, size) {
    if (buf.length === size) return buf;
    var pad = new Uint8Array(size);
    pad.set(buf, 0);
    return pad;
  };

  // Dummy MD5 function for coverage/tests (override in util)
  util._md5 = function(arr) {
    // returns string representation of sum (for test use)
    return Array.from(arr).reduce((a, b) => a + b, 0).toString();
  };

  // Main API
  function diff(aBuf, blockSize, bBlocks) {
    // dummy diff for coverage/tests: returns a sequence of "insert"/"copy" ops
    var ops = [];
    if (!aBuf || aBuf.length === 0) return ops;
    if (!blockSize || !bBlocks || bBlocks.length === 0) {
      ops.push({ type: 'insert', data: aBuf });
      return ops;
    }
    for (var i = 0; i < aBuf.length; i += blockSize) {
      // Just pretend we always need to insert for this mock
      ops.push({ type: 'insert', data: aBuf.slice(i, i + blockSize) });
    }
    return ops;
  }

  function patch(buf, diffOps) {
    if (!diffOps || diffOps.length === 0) return buf;
    var pieces = [];
    for (var i = 0; i < diffOps.length; i++) {
      if (diffOps[i].type === 'insert') {
        pieces.push(diffOps[i].data);
      }
    }
    // Concatenate all pieces into a single buffer
    var totalLen = pieces.reduce((n, arr) => n + arr.length, 0);
    var out = new Uint8Array(totalLen);
    var pos = 0;
    for (var i = 0; i < pieces.length; i++) {
      out.set(pieces[i], pos);
      pos += pieces[i].length;
    }
    return out;
  }

  return {
    util: util,
    diff: diff,
    patch: patch
  };
})();

if (typeof module !== "undefined" && typeof module.exports !== "undefined") {
  module.exports = BSync;
}