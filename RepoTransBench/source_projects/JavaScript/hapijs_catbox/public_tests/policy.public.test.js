'use strict';

// Public tests: use different keys/items/stats than original test/policy.js, but same coverage.

const Catbox = require('..');
const Code = require('@hapi/code');
const Lab = require('@hapi/lab');

const Connection = require('../test/connection'); // relative path

const { describe, it } = exports.lab = Lab.script();
const expect = Code.expect;

describe('Policy (public)', { retry: true }, () => {

    it('returns cached item with different value', async () => {

        const client = new Catbox.Client(Connection);
        const policy = new Catbox.Policy({ expiresIn: 1200 }, client, 'public');
        expect(policy.client).to.shallow.equal(client);

        await client.start();

        await policy.set('myKey', 'publicItem', null);

        const value = await policy.get('myKey');

        expect(value).to.equal('publicItem');
        expect(policy.stats).to.equal({ sets: 1, gets: 1, hits: 1, stales: 0, generates: 0, errors: 0 });
    });

    it('works with special property names (different key names)', async () => {

        const client = new Catbox.Client(Connection);
        const policy = new Catbox.Policy({ expiresIn: 900 }, client, 'public_test');
        await client.start();

        await policy.set('__proto__', 'foo', null);
        await policy.set('constructor', 'bar', null);

        const v1 = await policy.get('__proto__');
        const v2 = await policy.get('constructor');

        expect(v1).to.equal('foo');
        expect(v2).to.equal('bar');
    });

    // Additional analogs can be added as needed using different data
});