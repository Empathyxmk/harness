'use strict';

// Public tests: use a different flow/key/segment but same functional coverage.

const Catbox = require('..');
const Code = require('@hapi/code');
const Lab = require('@hapi/lab');

const Connection = require('../test/connection'); // relative path

const { describe, it } = exports.lab = Lab.script();
const expect = Code.expect;

describe('Catbox (public)', () => {

    it('creates a new connection (public)', async () => {

        const client = new Catbox.Client(Connection);
        await client.start();

        expect(client.isReady()).to.equal(true);
    });

    it('closes the connection (public)', async () => {

        const client = new Catbox.Client(Connection);
        await client.start();

        expect(client.isReady()).to.equal(true);

        await client.stop();
        expect(client.isReady()).to.equal(false);
    });

    // More analogs to test/index.js can be added here.
});