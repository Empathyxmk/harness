'use strict';

// Public tests: use different keys/items than original test/client.js, but the same logic.

const Catbox = require('..');
const Code = require('@hapi/code');
const Lab = require('@hapi/lab');

const Connection = require('../test/connection'); // relative path

const { describe, it } = exports.lab = Lab.script();
const expect = Code.expect;

describe('Client (public)', () => {

    it('uses prototype engine with new key/item', async () => {

        const client = new Catbox.Client(Connection);
        await client.start();

        const key = { id: 'y', segment: 'demo' };
        await client.set(key, 'ABC', 1500);

        const result = await client.get(key);

        expect(result.item).to.equal('ABC');
    });

    it('supports empty keys (different segment)', async () => {

        const client = new Catbox.Client(Connection);
        await client.start();

        const key = { id: '', segment: 'public_segment' };
        await client.set(key, 'XYZ', 2000);

        const result = await client.get(key);

        expect(result.item).to.equal('XYZ');
    });

    // Add more analogs to other tests in test/client.js using different values as appropriate.
});