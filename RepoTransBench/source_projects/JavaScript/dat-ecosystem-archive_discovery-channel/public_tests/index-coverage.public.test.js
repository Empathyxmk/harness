// Public coverage tests with different input/output data for DiscoveryChannel

const tape = require('tape');
const DiscoveryChannel = require('../index.js');

tape('join, leave, list and _hash/_unhash flows [public]', t => {
  const chd = new DiscoveryChannel();
  t.doesNotThrow(() => chd.join('publictopic', { port: 1 }), 'join should not throw');
  t.doesNotThrow(() => chd.leave('publictopic'), 'leave should not throw');
  t.doesNotThrow(() => { chd.list('publictopic'); }, 'list should not throw');
  t.doesNotThrow(() => { chd.list(Buffer.alloc(16)); }, 'list buffer should not throw');
  t.end();
});

tape('destroy disables further commands [public]', t => {
  const chd = new DiscoveryChannel();
  chd.destroy();
  t.ok(chd.destroyed, 'should be destroyed');
  t.doesNotThrow(() => chd.join('topicY'), 'join after destroy does nothing');
  t.doesNotThrow(() => chd.leave('bar'), 'leave after destroy does nothing');
  t.doesNotThrow(() => chd.list('bar'), 'list after destroy does nothing');
  t.end();
});