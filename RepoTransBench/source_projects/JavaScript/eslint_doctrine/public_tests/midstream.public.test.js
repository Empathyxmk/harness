/*
 * @fileoverview Public tests for midstream.js
 */

const fs = require('fs');
const path = require('path');
const root = path.join(path.dirname(fs.realpathSync(__filename)), '..');
const doctrine = require(path.join(root, 'lib', 'doctrine.js'));
require('should');

describe('midstream (public)', function () {
    it('parseType with a different type', function () {
        const res = doctrine.parseType('number value', { midstream: true });
        res.should.eql({
            "expression": {
                "name": "number",
                "type": "NameExpression"
            },
            "index": 6
        });
    });

    it('parseParamType with different rest parameter', function () {
        const res = doctrine.parseParamType('...args rest', { midstream: true });
        res.should.eql({
            "expression": {
                "expression": {
                    "name": "args",
                    "type": "NameExpression"
                },
                "type": "RestType"
            },
            "index": 7
        });
    });
});