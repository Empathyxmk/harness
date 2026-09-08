'use strict';

var assert = require('assert'),
  sinon = require('sinon'),
  chai = require('chai');

// Global setup.
global.expect = chai.expect;

var cli = require('../lib/cli');

describe('cli (public)', function () {
  describe('--help', function () {
    it('should log help information');
    it('should not execute Pint');
    it('should ignore other options and parameters');
    it('should return with exit code 0');
  });

  describe('--dry-run', function () {
    it('should take --dry-run');
    it('should simulate Pint execution');
    it('should ignore other options and parameters');
    it('should not spawn actual grunt process');
    it('should return with exit code 0');
  });

  describe('--quiet', function () {
    it('should take --quiet');
    it('should execute Pint');
    it('should suppress standard output');
    it('should return with exit code 0');
  });

  describe('custom runners', function () {
    it('should ignore other options and parameters');
    it('should execute only the specified runners without dependencies');
  });
});