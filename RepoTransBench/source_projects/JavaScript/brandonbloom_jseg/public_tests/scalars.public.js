let assert = require('assert');
let jseg = require('../src');
let {TestGraph} = require('../test/util');

let [b, t] = jseg.newSchema();

b.entity('Object');

b.finalize({

  attributes: {
    Object: {
      any: t.Scalar,
      text: t.Text,
      removeme: t.Text,
      bool: t.Bool,
    },
  },

  relationships: [],

});

let tg = new TestGraph(t);

// Use a different unknown field name.
tg.expectMessage('unknown field "secret"', () => {
  tg.g.put({
    type: t.Object,
    lid: 'y',
    text: 'z',
    secret: 'hidden',
    removeme: 'ok',
  });
});

tg.check('y', {
  type: t.Object,
  lid: 'y',
  text: 'z',
  removeme: 'ok',
  any: null,
  bool: null,
});

class Bar {
  constructor(foo) {
    this.foo = foo;
  }
}
let bar = new Bar();

tg.g.put({
  lid: 'y',
  removeme: null,
  bool: true,
  any: bar,
});

tg.check('y', {
  lid: 'y',
  type: t.Object,
  text: 'z',
  removeme: null,
  bool: true,
  any: bar,
});