const path = require('path');
const _ = require('lodash');
const index = require('../index');

describe('index.js - Smoke tests & module', () => {
  it('should have expected exports and util', () => {
    expect(typeof index).toBe('object');
    expect(typeof index.postMessage).toBe('function');
    expect(typeof index.handleElasticBeanstalk).toBe('function');
    expect(typeof index.handleCodeDeploy).toBe('function');
  });
});