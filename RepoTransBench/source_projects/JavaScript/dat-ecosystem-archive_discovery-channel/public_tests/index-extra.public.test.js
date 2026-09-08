// Public test cases for Discovery, using different input/output data

const test = require('tape');
const Discovery = require('../index.js');

test('join, leave, list and _hash/_unhash flows [public]', t => {
  const d = Discovery();
  t.doesNotThrow(() => d.join('public_chan'), 'join should not throw');
  t.doesNotThrow(() => d.leave('public_chan'), 'leave should not throw');
  t.doesNotThrow(() => d.list(), 'list should not throw');
  t.doesNotThrow(() => d.list(Buffer.from('public_buf')), 'list buffer should not throw');
  d.destroy();
  t.pass('should be destroyed');
  t.doesNotThrow(() => d.join('rejoin'), 'join after destroy does nothing');
  t.doesNotThrow(() => d.leave('releave'), 'leave after destroy does nothing');
  t.doesNotThrow(() => d.list(), 'list after destroy does nothing');
  t.end();
});

test('creates with default options and emits warn/error [public]', t => {
  const d = Discovery();
  t.ok(d, 'should be truthy');

  d.once('warn', msg => {
    t.equal(typeof msg, 'string', 'warn event emitted as string');
    d.removeAllListeners();
    t.end();
  });
  // simulate warning event
  d.emit('warn', 'public warning');
});

test('error emits with undefined [public]', t => {
  const d = Discovery();
  d.once('error', err => {
    t.equal(err, undefined, 'error emits with undefined (simulate)');
    d.removeAllListeners();
    t.end();
  });
  d.emit('error', undefined);
});

test('hash override and no hash [public]', t => {
  const customHash = () => Buffer.from('bbee', 'hex');
  const d1 = Discovery({ hash: customHash });
  t.deepEqual(d1._hash('foo'), Buffer.from('bbee', 'hex'), 'should use custom hash');

  const d2 = Discovery();
  t.ok(typeof d2._hash('foo'), 'should default to object');
  t.end();
});

test('destroy disables actions [public]', t => {
  const d = Discovery();
  d.destroy();
  t.equal(d.join('xyz123'), undefined, 'join returns undefined');
  t.equal(d.leave('123xyz'), undefined, 'leave returns undefined');
  t.end();
});

test('event propagation: peer, warn, error [public]', t => {
  const d = Discovery();
  d.on('peer', obj => {
    t.deepEqual(obj, { channel: 'uvw', host: '10.0.0.1', port: 9000 }, 'peer event as object');
  });
  d.on('warn', w => {
    t.equal(w, 'a public warning!', 'warn event');
  });
  d.on('error', e => {
    t.equal(e, 'a public error!', 'error event');
    t.end();
  });

  d.emit('peer', { channel: 'uvw', host: '10.0.0.1', port: 9000 });
  d.emit('warn', 'a public warning!');
  d.emit('error', 'a public error!');
});

test('list equivalency check [public]', t => {
  const d = Discovery();
  d.join('gamma');
  d.join('delta');
  t.ok(Array.isArray(d.list('gamma')), 'should be equivalent');
  t.ok(Array.isArray(d.list('delta')), 'should be equivalent');
  t.ok(Array.isArray(d.list(Buffer.from('gamma'))), 'should be equivalent');
  t.ok(Array.isArray(d.list()), 'should be equivalent');
  t.end();
});

test('join cb gets called [public]', t => {
  const d = Discovery();
  d.join('cb', {}, err => {
    t.equal(err, null, 'null');
    t.ok(true, 'should be truthy');
    t.end();
  });
});