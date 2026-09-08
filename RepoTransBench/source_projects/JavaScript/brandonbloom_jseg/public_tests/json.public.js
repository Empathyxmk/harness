let assert = require('assert');
let jseg = require('../src');
let {TestGraph} = require('../test/util');

let [b, t] = jseg.newSchema();

b.entity('Object');

b.finalize({

  attributes: {
    Object: {
      eventTime: t.Time,
    },
  },

  relationships: [],

});

let tg = new TestGraph(t);

let eventTime = new Date(1577836800000); // Different epoch: 2020-01-01T00:00:00.000Z

tg.g.put({
  type: 'Object',
  lid: 'y',
  eventTime,
});

tg.check('y', {
  type: t.Object,
  lid: 'y',
  eventTime,
});

tg.check('y', {
  lid: 'y',
  type: 'Object',
  eventTime: '2020-01-01T00:00:00.000Z',
}, {json: true});