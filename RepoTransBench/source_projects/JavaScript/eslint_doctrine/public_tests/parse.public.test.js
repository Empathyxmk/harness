/*
 * @fileoverview Public test cases for doctrine.parse with different data.
 */

/*global require describe it*/
/*jslint node:true */
'use strict';

const fs = require('fs');
const path = require('path');
const root = path.join(path.dirname(fs.realpathSync(__filename)), '..');
const doctrine = require(path.join(root, 'lib', 'doctrine.js'));
require('should');

describe('parse (public)', function () {
    it('other alias', function () {
        var res = doctrine.parse('/** @aliasAnother */', { unwrap: true });
        res.tags.should.have.length(0);
    });

    it('alias with different name', function () {
        var res = doctrine.parse('/** @alias alternativeName */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'alias');
        res.tags[0].should.have.property('name', 'alternativeName');
    });

    it('alias with different namepath', function () {
        var res = doctrine.parse('/** @alias anotherName.XY */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'alias');
        res.tags[0].should.have.property('name', 'anotherName.XY');
    });

    it('alias with another module path', function () {
        var res = doctrine.parse('/** @alias module:yourmodule/yourmodule.init2 */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'alias');
        res.tags[0].should.have.property('name', 'module:yourmodule/yourmodule.init2');
    });

    it('alias with namepath with underscore', function () {
        var res = doctrine.parse('/** @alias module:yourmodule/your_module */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'alias');
        res.tags[0].should.have.property('name', 'module:yourmodule/your_module');
    });

    it('enum', function () {
        var res = doctrine.parse('/** @enum */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'enum');
    });

    it('enum with name', function () {
        var res = doctrine.parse('/** @enum enumname */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'enum');
        res.tags[0].should.have.property('name', 'enumname');
    });

    it('enumeration with name', function () {
        var res = doctrine.parse('/** @enumeration enumname */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'enumeration');
        res.tags[0].should.have.property('name', 'enumname');
    });

    it('enum with type and name', function () {
        var res = doctrine.parse('/** @enum {Number} enumname */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'enum');
        res.tags[0].should.have.property('name', 'enumname');
        res.tags[0].should.have.property('type');
        res.tags[0].type.should.eql({
            type: 'NameExpression',
            name: 'Number'
        });
    });

    it('Enum with type and name', function () {
        var res = doctrine.parse('/** @Enum {Number} enumname */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'Enum');
        res.tags[0].should.have.property('name', 'enumname');
        res.tags[0].should.have.property('type');
        res.tags[0].type.should.eql({
            type: 'NameExpression',
            name: 'Number'
        });
    });

    it('enumeration with type and name', function () {
        var res = doctrine.parse('/** @enumeration {Number} enumname */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'enumeration');
        res.tags[0].should.have.property('name', 'enumname');
        res.tags[0].should.have.property('type');
        res.tags[0].type.should.eql({
            type: 'NameExpression',
            name: 'Number'
        });
    });

    it('enum multiple', function () {
        var res = doctrine.parse("/**@enum\n @enum*/", { unwrap: true });
        res.tags.should.have.length(2);
        res.tags[0].should.have.property('title', 'enum');
        res.tags[1].should.have.property('title', 'enum');
    });

    it('enum double', function () {
        var res = doctrine.parse("/**@enum\n @enum*/", { unwrap: true });
        res.tags.should.have.length(2);
        res.tags[0].should.have.property('title', 'enum');
        res.tags[1].should.have.property('title', 'enum');
    });

    it('enum triple', function () {
        var res = doctrine.parse([
            "/**",
            " * @enum @enum",
            " * @enum @enum",
            " * @enum @enum",
            " */"
        ].join('\n'), { unwrap: true });
        res.tags.should.have.length(3);
        res.tags[0].should.have.property('title', 'enum');
        res.tags[1].should.have.property('title', 'enum');
        res.tags[2].should.have.property('title', 'enum');
    });

    it('factory', function () {
        var res = doctrine.parse('/** @factory */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'factory');
    });

    it('factory with type', function () {
        var res = doctrine.parse('/** @factory {Array} */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'factory');
        res.tags[0].type.should.eql({
            type: 'NameExpression',
            name: 'Array'
        });
    });

    it('factory with type and name', function () {
        var res = doctrine.parse('/** @factory {Array} arrayName */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'factory');
        res.tags[0].should.have.property('name', 'arrayName');
        res.tags[0].type.should.eql({
            type: 'NameExpression',
            name: 'Array'
        });
    });

    it('deprecated public variant', function () {
        var res = doctrine.parse('/** @deprecated2 */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'deprecated2');
    });

    it('deprecated alt with description', function () {
        var res = doctrine.parse('/** @deprecated No longer maintained */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'deprecated');
        res.tags[0].should.have.property('description', 'No longer maintained');
    });

    it('method', function () {
        var res = doctrine.parse('/** @method */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'method');
    });

    it('method with name', function () {
        var res = doctrine.parse('/** @method customMethod */', { unwrap: true });
        res.tags.should.have.length(1);
        res.tags[0].should.have.property('title', 'method');
        res.tags[0].should.have.property('name', 'customMethod');
    });
});