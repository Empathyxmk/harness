const test = require('tape');

test('config uses defaults in non-production', t => {
  process.env.NODE_ENV = '';
  delete require.cache[require.resolve('./config')];
  const config = require('./config');
  t.equal(config.express.port, 3000, 'Default EXPRESS_PORT is 3000');
  t.equal(config.express.ip, '127.0.0.1', 'Default IP is 127.0.0.1');
  t.equal(config.mongodb.port, 27017, 'Default MongoDB PORT is 27017');
  t.equal(config.mongodb.host, 'localhost', 'Default MongoDB HOST is localhost');
  t.end();
});

test('config reads from environment and switches in production', t => {
  process.env.EXPRESS_PORT = '5555';
  process.env.MONGODB_PORT = '9999';
  process.env.MONGODB_HOST = 'remotehost';
  process.env.NODE_ENV = 'production';
  delete require.cache[require.resolve('./config')];
  const config = require('./config');
  t.equal(config.express.port, '5555', 'Custom EXPRESS_PORT is used');
  t.equal(config.express.ip, '0.0.0.0', 'Production IP is 0.0.0.0');
  t.equal(config.mongodb.port, '9999', 'Custom MongoDB PORT is used');
  t.equal(config.mongodb.host, 'remotehost', 'Custom MongoDB HOST is used');
  t.end();

  // Clean up for others
  delete process.env.EXPRESS_PORT;
  delete process.env.MONGODB_PORT;
  delete process.env.MONGODB_HOST;
  process.env.NODE_ENV = '';
});