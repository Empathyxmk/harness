/*
 * @fileoverview Public test cases for strict parse functionality
 */
const fs = require('fs');
const path = require('path');
const root = path.join(path.dirname(fs.realpathSync(__filename)), '..');
const doctrine = require(path.join(root, 'lib', 'doctrine.js'));
require('should');

describe('strict parse (public)', function () {
    // Similar coverage, but using slightly different tag names and types
    it('unbalanced braces (public)', function () {
        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * @return {num",
                    " */"
                ].join('\n'), { unwrap: true, strict: true });
        }).should.throw('Braces are not balanced');

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * @return {num",
                    " */"
                ].join('\n'), { unwrap: true });
        }).should.not.throw();

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * Description",
                    " * @prop {array name Prop description",
                    " * @prop {Object} bar Prop bar",
                    " */"
                ].join('\n'), { unwrap: true, strict: true });
        }).should.throw('Braces are not balanced');

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * Description",
                    " * @prop {array name Prop description",
                    " * @prop {Object} bar Prop bar",
                    " */"
                ].join('\n'), { unwrap: true });
        }).should.not.throw();

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * Description",
                    " * @yields {float",
                    " */"
                ].join('\n'), { unwrap: true, strict: true });
        }).should.throw('Braces are not balanced');

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * Description",
                    " * @yields {float",
                    " */"
                ].join('\n'), { unwrap: true });
        }).should.not.throw();
    });

    it('incorrect tag starting with @@ (public)', function () {
        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * @@version_info",
                    " */"
                ].join('\n'), { unwrap: true, strict: true });
        }).should.throw('Missing or invalid title');

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * @@version_info",
                    " */"
                ].join('\n'), { unwrap: true });
        }).should.not.throw();

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * Description",
                    " * @@throws {Error} reason for throwing",
                    " */"
                ].join('\n'), { unwrap: true, strict: true });
        }).should.throw('Missing or invalid title');

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * Description",
                    " * @@throws {Error} reason for throwing",
                    " */"
                ].join('\n'), { unwrap: true });
        }).should.not.throw();

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * Description",
                    " * @kind publicAPI",
                    " */"
                ].join('\n'), { unwrap: true, strict: true });
        }).should.throw("Invalid kind name 'publicAPI'");

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * Description",
                    " * @variation Beta",
                    " */"
                ].join('\n'), { unwrap: true, strict: true });
        }).should.throw("Invalid variation 'Beta'");

        (() => {
            doctrine.parse(
                [
                    "/**",
                    " * Description",
                    " * @access internal",
                    " */"
                ].join('\n'), { unwrap: true, strict: true });
        }).should.throw("Invalid access name 'internal'");
    });
});