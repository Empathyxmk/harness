'use strict';

const chai = require('chai');
const sinon = require('sinon');
const expect = chai.expect;

const proxyquire = require('proxyquire').noCallThru();

describe('jobQueue', () => {
  let jobQueue, utilStub, underscore, JobStub;

  beforeEach(() => {
    underscore = require('underscore');
    utilStub = {
      getJobs: sinon.stub().returns([
        { name: 'foo', config: { dependsOn: [] } },
        { name: 'bar', config: { dependsOn: ['foo'] } }
      ])
    };
    JobStub = function (name) {
      this.name = name;
      this.config = { name, dependsOn: name === 'bar' ? ['foo'] : [] };
    };
    jobQueue = proxyquire('../lib/jobQueue.js', {
      './util.js': utilStub,
      'underscore': underscore,
      './Job.js': JobStub
    });
  });

  it('creates jobs for empty arguments', () => {
    let jq = jobQueue([]);
    let instance = jq.getInstance();
    expect(instance.isEmpty()).to.be.false;
    let items = instance.pop();
    expect(items.foo).to.be.an('object');
  });

  it('completes and queues next jobs', () => {
    let jq = jobQueue(['foo', 'bar']);
    let instance = jq.getInstance();
    let items1 = instance.pop();
    expect(items1.foo).to.exist;
    instance.complete('foo');
    let items2 = instance.pop();
    expect(items2.bar).to.exist;
    instance.complete('bar');
    expect(instance.isEmpty()).to.be.true;
  });

  it('handles isEmpty properly when nothing left', () => {
    let jq = jobQueue(['foo']);
    let instance = jq.getInstance();
    expect(instance.isEmpty()).to.be.false;
    // pop and complete
    let items = instance.pop();
    instance.complete('foo');
    expect(instance.isEmpty()).to.be.true;
  });
});