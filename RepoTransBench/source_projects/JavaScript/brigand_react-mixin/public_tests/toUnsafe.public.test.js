const toUnsafe = require('../toUnsafe');
var expect = require('expect.js');

it(`works with different functions and keys (public test)`, () => {
  const x = () => 'foo';
  const y = () => 'bar';
  const z = () => 'baz';

  const m1 = { componentWillMount: x, componentWillReceiveProps: y, componentWillUpdate: z };
  const m2 = toUnsafe(m1);

  expect(m1).to.eql({ componentWillMount: x, componentWillReceiveProps: y, componentWillUpdate: z }, 'm1 not modified');
  expect(m2).to.eql({ UNSAFE_componentWillMount: x, UNSAFE_componentWillReceiveProps: y, UNSAFE_componentWillUpdate: z });
  expect(Object.keys(m2).sort()).to.eql(['UNSAFE_componentWillMount', 'UNSAFE_componentWillReceiveProps', 'UNSAFE_componentWillUpdate']);
});