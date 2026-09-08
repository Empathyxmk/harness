/*
 * @fileoverview Public test cases for doctrine.unwrapComment
 */

/*jslint node:true */
'use strict';

const fs = require('fs');
const path = require('path');
const root = path.join(path.dirname(fs.realpathSync(__filename)), '..');
const doctrine = require(path.join(root, 'lib', 'doctrine.js'));
require('should');

describe('unwrapComment (public)', function () {
    it('different normal', function () {
        doctrine.unwrapComment('/**\n * @foo\n * @bar\n */').should.equal('\n@foo\n@bar');
    });

    it('single char with space', function () {
        doctrine.unwrapComment('/** y */').should.equal(' y ');
    });

    it('more stars alternative', function () {
        doctrine.unwrapComment('/***z*/').should.equal('z');
        doctrine.unwrapComment('/****z*/').should.equal('*z');
    });

    it('2 lines alternative', function () {
        doctrine.unwrapComment('/**abc\n * def\n*/').should.equal('abc\ndef');
    });

    it('2 lines with leading space', function () {
        doctrine.unwrapComment('/**abc\n *    def\n*/').should.equal('abc\n   def');
    });

    it('3 lines with different blank line', function () {
        doctrine.unwrapComment('/**abc\n *\n \* def\n*/').should.equal('abc\n\ndef');
    });
});