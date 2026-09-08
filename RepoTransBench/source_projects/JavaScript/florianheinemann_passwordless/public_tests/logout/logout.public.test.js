'use strict';

var expect = require('chai').expect;
var express = require('express');
var passwordless = require('../../');

describe('logout (public)', function () {
    it('should be a function', function () {
        expect(passwordless.logout).to.be.a('function');
    });

    it('should return a middleware function when invoked', function () {
        var mw = passwordless.logout();
        expect(mw).to.be.a('function');
    });
});