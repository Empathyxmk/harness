const crc32 = require('..');
const test = require('tap').test;

test('crc32 different string', function (t) {
  var input = Buffer.from('hello world');
  var expected = Buffer.from([0x1c, 0x29, 0x7d, 0x87]);
  t.same(crc32(input), expected);
  t.end();
});

test('another short string', function (t) {
  var input = Buffer.from('DATA');
  var expected = Buffer.from([0x8d, 0xe5, 0x8c, 0x46]);
  t.same(crc32(input), expected);
  t.end();
});

test('byte array of different values', function (t) {
  var input = Buffer.from([0x01, 0x02, 0x03, 0x04]);
  var expected = Buffer.from([0xb1, 0x67, 0x9e, 0xd6]);
  t.same(crc32(input), expected);
  t.end();
});

test('crc32 of utf-8 string', function (t) {
  var input = Buffer.from('测试');
  var expected = Buffer.from([0x91, 0xca, 0xd8, 0xeb]);
  t.same(crc32(input), expected);
  t.end();
});

test('casts to buffer for utf-8 string', function (t) {
  var input = '测试';
  var expected = Buffer.from([0x91, 0xca, 0xd8, 0xeb]);
  t.same(crc32(input), expected);
  t.end();
});

test('signed value, different input', function (t) {
  var input = 'grilled cheese';
  var expected = -1929599608;
  t.same(crc32.signed(input), expected);
  t.end();
});

test('unsigned value, different input', function (t) {
  var input = 'turkey sandwich';
  var expected = 1477935989;
  t.same(crc32.unsigned(input), expected);
  t.end();
});

test('crc32 with append mode, alternate strings', function (t) {
  var input = [
    Buffer.from('foo'),
    Buffer.from(' '),
    Buffer.from('bar'),
    Buffer.from(' '),
    Buffer.from('baz'),
  ];
  var expected = Buffer.from([0x25, 0x4b, 0xa2, 0x5d]);
  for (var crc = 0, i = 0; i < input.length; i++) {
    crc = crc32(input[i], crc);
  }
  t.same(crc, expected);
  t.end();
});

test('signed in append mode, alternate', function (t) {
  var input1 = 'grilled';
  var input2 = ' ';
  var input3 = 'cheese';
  var expected = -1929599608;

  var crc = crc32.signed(input1);
  crc = crc32.signed(input2, crc);
  crc = crc32.signed(input3, crc);

  t.same(crc, expected);
  t.end();
});

test('accepts integer 12345 as input', function (t) {
  try {
    t.same(crc32(12345), Buffer.from([0x00, 0x00, 0x30, 0x39]));
  } catch (e) {
    t.fail('should be able to accept integer');
  } finally {
    t.end();
  }
});

test('throws on array input', function (t) {
  try {
    crc32([]);
    t.fail('should fail on garbage input');
  } catch (e) {
    t.ok('should pass');
  } finally {
    t.end();
  }
});

test('unsigned in append mode, alternate', function (t) {
  var input1 = 'turkey sand';
  var input2 = 'wich';
  var expected = 1477935989;

  var crc = crc32.unsigned(input1);
  crc = crc32.unsigned(input2, crc);
  t.same(crc, expected);
  t.end();
});