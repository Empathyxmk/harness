let assert = require('assert');
let jseg = require('../src');
let {TestGraph} = require('../test/util');

let [b, t] = jseg.newSchema();

b.entity('Object');

b.finalize({

  attributes: {
    Object: {
      key: t.Key,
      creator: t.Key,
    },
  },

  relationships: [],

});

let tg = new TestGraph(t);

tg.g.put({
  type: t.Object,
  lid: 'a',
  key: 'alpha',
});

tg.g.put({
  type: t.Object,
  lid: 'b',
  key: 'beta',
});

tg.expectMessage('expected non-empty string', () => {
  tg.g.put({
    type: t.Object,
    lid: 'c',
    key: 42,
  });
});
tg.checkLookup(t.Object, 'key', '42', null);

tg.checkLookup(t.Object, 'key', 'alpha', {
  type: t.Object,
  lid: 'a',
  key: 'alpha',
  creator: null,
});

tg.checkLookup('Object', 'key', 'beta', {
  type: t.Object,
  lid: 'b',
  key: 'beta',
  creator: null,
});

tg.g.put({lid: 'a', key: null});
tg.g.put({lid: 'b'});

tg.checkLookup(t.Object, 'key', 'alpha', null);

tg.checkLookup(t.Object, 'key', 'beta', {
  type: t.Object,
  lid: 'b',
  key: 'beta',
  creator: null,
});

tg.g.put({lid: 'b', key: 'delta'});

tg.checkLookup(t.Object, 'key', 'beta', null);

tg.checkLookup(t.Object, 'key', 'delta', {
  type: t.Object,
  lid: 'b',
  key: 'delta',
  creator: null,
});

tg.checkLookup(t.Object, 'creator', '' + ({}).constructor, null);