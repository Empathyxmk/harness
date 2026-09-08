'use strict';

const chai = require('chai');
const sinon = require('sinon');
const expect = chai.expect;

const proxyquire = require('proxyquire').noCallThru();

describe('jobQueue (public)', () => {
  let jobQueue, utilStub, underscore, JobStub;

  beforeEach(() => {
    underscore = require('underscore');
    utilStub = {
      getJobs: sinon.stub().returns([
        { name: 'alpha', config: { dependsOn: [] } },
        { name: 'beta', config: { dependsOn: ['alpha'] } },
        { name: 'gamma', config: { dependsOn: ['beta'] } }
      ])
    };
    JobStub = function (name) {
      this.name = name;
      this.config = { name, dependsOn: name === 'beta' ? ['alpha'] : (name === 'gamma' ? ['beta'] : []) };
    };
    jobQueue = proxyquire('../lib/jobQueue.js', {
      './util.js': utilStub,
      'underscore': underscore,
      './Job.js': JobStub
    });
  });

  it('creates jobs for empty arguments (public)', () => {
    let jq = jobQueue([]);
    let instance = jq.getInstance();
    expect(instance.isEmpty()).to.be.false;
    let items = instance.pop();
    expect(items.alpha).to.be.an('object');
  });

  it('completes and queues next jobs (public)', () => {
    let jq = jobQueue(['alpha', 'beta', 'gamma']);
    let instance = jq.getInstance();
    let items1 = instance.pop();
    expect(items1.alpha).to.exist;
    instance.complete('alpha');
    let items2 = instance.pop();
    expect(items2.beta).to.exist;
    instance.complete('beta');
    let items3 = instance.pop();
    expect(items3.gamma).to.exist;
    instance.complete('gamma');
    expect(instance.isEmpty()).to.be.true;
  });

  it('handles isEmpty properly with single job (public)', () => {
    let jq = jobQueue(['gamma']);
    let instance = jq.getInstance();
    expect(instance.isEmpty()).to.be.false;
    let items = instance.pop();
    instance.complete('gamma');
    expect(instance.isEmpty()).to.be.true;
  });
});