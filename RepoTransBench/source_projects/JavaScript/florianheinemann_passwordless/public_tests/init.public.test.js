'use strict';

var expect = require('chai').expect;
var express = require('express');
var request = require('supertest');
var passwordlessInst = require('../');
var Passwordless = require('../').Passwordless;
var TokenStoreMock = require('../test/mock/tokenstoremock');

describe('passwordless (public)', function() {
	describe('singleton', function() {
		it('should still provide only one Passwordless instance', function () {
			// Different form: check that two requires are strictly equal by deep equality
			const inst1 = require('../');
			const inst2 = require('../lib');
			expect(inst1 === inst2).to.be.true;
		})
	})

	describe('constructor', function() {		
		it('should instantiate a new Passwordless instance with arguments', function () {
			const passwordless = new Passwordless();
			expect(Object.getPrototypeOf(passwordless)).to.equal(Passwordless.prototype);
		})
	})

	describe('init', function() {
		it('should throw if called with null', function () {
			const passwordless = new Passwordless();
			expect(function() { passwordless.init(null) }).to.throw(Error);
		})

		it('should succeed with a new TokenStoreMock, twice', function () {
			const passwordless = new Passwordless();
			passwordless.init(new TokenStoreMock());
			const passwordless2 = new Passwordless();
			passwordless2.init(new TokenStoreMock());
		})

		it('should succeed with options using a different userProperty', function () {
			const passwordless = new Passwordless();
			passwordless.init(new TokenStoreMock(), { userProperty: 'foo' });
		})
	})
});