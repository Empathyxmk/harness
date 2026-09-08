let assert = require('assert');
let jseg = require('../src');
let {TestGraph} = require('../test/util');

let [b, t] = jseg.newSchema();

b.entity('Object');

b.scalar('Ceil', {
  validate: Math.ceil,
});
b.scalar('Odd', {
  validate: (x) => {
    if (x % 2 === 0) {
      throw Error('expected odd number');
    }
    return x;
  },
});

b.finalize({

  attributes: {
    Object: {
      ceil: t.Ceil,
      odd: t.Odd,
    },
  },

  relationships: [],

});

let tg = new TestGraph(t);

tg.g.put({
  type: t.Object,
  lid: 'great',
  ceil: 7.2,
  odd: 9,
});

tg.check('great', {
  type: t.Object,
  lid: 'great',
  ceil: 8,
  odd: 9,
});

tg.expectMessage('expected odd number', () => {
  tg.g.put({
    type: t.Object,
    lid: 'notgreat',
    ceil: 4.9,
    odd: 10,
  });
});

tg.check('notgreat', {
  type: t.Object,
  lid: 'notgreat',
  ceil: 5,
  odd: null,
});