const index = require('../index');

describe('index.js - Public exports & module', () => {
  it('should export handleElasticBeanstalk and handleCodeDeploy and postMessage', () => {
    expect(index).toBeInstanceOf(Object);
    expect(typeof index.handleElasticBeanstalk).toBe('function');
    expect(typeof index.handleCodeDeploy).toBe('function');
    expect(typeof index.postMessage).toBe('function');
  });
});