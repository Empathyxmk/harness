/*
 * @fileoverview Public test cases for type stringify functionality
 */

const fs = require('fs');
const path = require('path');
const root = path.join(path.dirname(fs.realpathSync(__filename)), '..');
const doctrine = require(path.join(root, 'lib', 'doctrine.js'));
require('should');

describe('stringify (public)', function () {
    function testStringifyPublic(text) {
        it('should stringify correctly: ' + text, function() {
            const result = doctrine.parse("@param {" + text + "} val");
            const stringed = doctrine.type.stringify(result.tags[0].type, {compact:true});
            stringed.should.equal(text);
        });
    }

    // Different simple types/values from the original suite
    testStringifyPublic("Boolean");
    testStringifyPublic("Object");
    testStringifyPublic("Date");
    testStringifyPublic("RegExp");
    testStringifyPublic("number");
    testStringifyPublic("?number");
    testStringifyPublic("number=");
    testStringifyPublic("Array.<Boolean>");
    testStringifyPublic("(Boolean|Date)");
    testStringifyPublic("[Boolean,Date]");
    testStringifyPublic("{b:Boolean,c:Date}");
    testStringifyPublic("function(b:Boolean):Date");
    testStringifyPublic("function(x:number,y:number):boolean");
    testStringifyPublic("...Boolean");
    testStringifyPublic("[[Boolean]]");
    testStringifyPublic("{d:(Boolean|Date),e,f:Array.<Boolean>}");
    testStringifyPublic("...{d:(Boolean|Date),e,f:Array.<Boolean>}");
    testStringifyPublic("{d:(Boolean|Date),e,f:Array.<Boolean>}=");

    // literal types
    testStringifyPublic('"Goodbye, World!"');
    testStringifyPublic("9000");
});

describe('literals (public)', function() {
    it('NullableLiteral', function () {
        doctrine.type.stringify({
            type: doctrine.Syntax.NullableLiteral
        }).should.equal('?');
    });

    it('AllLiteral', function () {
        doctrine.type.stringify({
            type: doctrine.Syntax.AllLiteral
        }).should.equal('*');
    });

    it('NullLiteral', function () {
        doctrine.type.stringify({
            type: doctrine.Syntax.NullLiteral
        }).should.equal('null');
    });

    it('UndefinedLiteral', function () {
        doctrine.type.stringify({
            type: doctrine.Syntax.UndefinedLiteral
        }).should.equal('undefined');
    });

    it('StringLiteralType', function () {
        doctrine.type.stringify({
            type: doctrine.Syntax.StringLiteralType,
            value: 'Goodbye, World!'
        }).should.equal('"Goodbye, World!"');
    });

    it('NumericLiteralType', function () {
        doctrine.type.stringify({
            type: doctrine.Syntax.NumericLiteralType,
            value: 9000
        }).should.equal('9000');
    });

    it('BooleanLiteralType', function () {
        doctrine.type.stringify({
            type: doctrine.Syntax.BooleanLiteralType,
            value: true
        }).should.equal('true');
        doctrine.type.stringify({
            type: doctrine.Syntax.BooleanLiteralType,
            value: false
        }).should.equal('false');
    });
});

describe('Expression (public)', function () {
    it('NameExpression', function () {
        doctrine.type.stringify({
            type: doctrine.Syntax.NameExpression,
            name: 'another.valid.name'
        }).should.equal('another.valid.name');

        doctrine.type.stringify({
            type: doctrine.Syntax.NameExpression,
            name: 'Boolean'
        }).should.equal('Boolean');
    });

    it('ArrayType', function () {
        doctrine.type.stringify({
            type: doctrine.Syntax.ArrayType,
            elements: [{
                type: doctrine.Syntax.NameExpression,
                name: 'Boolean'
            }]
        }).should.equal('[Boolean]');

        doctrine.type.stringify({
            type: doctrine.Syntax.ArrayType,
            elements: [
                { type: doctrine.Syntax.NameExpression, name: 'Boolean' },
                { type: doctrine.Syntax.NameExpression, name: 'Date' }
            ]
        }).should.equal('[Boolean,Date]');
    });

    // ... other publicized expressions could be added similarly ...
});