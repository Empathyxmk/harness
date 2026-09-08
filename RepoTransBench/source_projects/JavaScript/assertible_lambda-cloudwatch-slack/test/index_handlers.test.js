const index = require('../index');
const _ = require('lodash');

// Helper for Elastic Beanstalk events
function makeElasticBeanstalkEvent(message, subject) {
  return {
    Records: [{
      Sns: {
        Message: message,
        Subject: subject !== undefined ? subject : 'TestBeBe Subject',
        Timestamp: '2021-01-01T00:00:00Z'
      }
    }]
  };
}

// Helper for CodeDeploy events
function makeCodeDeployEvent(msg, subject) {
  return {
    Records: [{
      Sns: {
        Message: typeof msg === 'string' ? msg : JSON.stringify(msg),
        Subject: subject !== undefined ? subject : 'TestCD Subject',
        Timestamp: '2021-01-01T00:00:00Z'
      }
    }]
  };
}

describe('index.js handlers', () => {
  describe('handleElasticBeanstalk', () => {
    it('returns good color for standard message', () => {
      const event = makeElasticBeanstalkEvent('Application update finished');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('good');
      expect(result.attachments[0].fields[1].value).toContain('Application');
    });
    it('returns danger for RED state', () => {
      const event = makeElasticBeanstalkEvent('Environment health has transitioned to RED.');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('danger');
    });
    it('returns danger for Severe', () => {
      const event = makeElasticBeanstalkEvent('Environment health has transitioned to Severe');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('danger');
    });
    it('returns warning for yellow', () => {
      const event = makeElasticBeanstalkEvent('Environment health has transitioned to YELLOW');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('warning');
    });
    it('returns warning for info', () => {
      const event = makeElasticBeanstalkEvent('Environment health has transitioned to Info');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('warning');
    });
    it('falls back to default subject', () => {
      const event = makeElasticBeanstalkEvent('OK again', undefined);
      delete event.Records[0].Sns.Subject;
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.text).toMatch(/AWS Elastic Beanstalk Notification/);
    });
  });

  describe('handleCodeDeploy', () => {
    const minimalMessage = {
      deploymentGroupName: "SomeGroup",
      applicationName: "AppA",
      status: "FAILED"
    };
    it('parses JSON message with FAILED status', () => {
      const event = makeCodeDeployEvent({ ...minimalMessage, status: "FAILED" });
      const result = index.handleCodeDeploy(event, {});
      expect(result.attachments[0].color).toBe('danger');
      expect(result.attachments[0].fields[1].title).toBe('Deployment Group');
    });
    it('parses JSON message with SUCCEEDED status (good)', () => {
      const event = makeCodeDeployEvent({ ...minimalMessage, status: "SUCCEEDED" });
      const result = index.handleCodeDeploy(event, {});
      expect(result.attachments[0].color).toBe('good');
    });
    it('parses JSON message with neutral status (warning)', () => {
      const event = makeCodeDeployEvent({ ...minimalMessage, status: "STOPPED" });
      const result = index.handleCodeDeploy(event, {});
      expect(result.attachments[0].color).toBe('warning');
    });
    it('falls back to simple string message on parse failure', () => {
      const event = makeCodeDeployEvent("just a string");
      const result = index.handleCodeDeploy(event, {});
      // When not JSON, first field is Time, second is Message
      expect(result.attachments[0].fields[1].title).toBe('Message');
    });
    it('handles JSON w/o deploymentGroupName keys', () => {
      const event = makeCodeDeployEvent({ status: "FAILED" });
      const result = index.handleCodeDeploy(event, {});
      // When not falling back, should still show "Deployment Group"
      expect(result.attachments[0].fields[1].title).toBe('Deployment Group');
    });
    it('works with missing SNS subject', () => {
      const event = makeCodeDeployEvent({ ...minimalMessage });
      delete event.Records[0].Sns.Subject;
      const result = index.handleCodeDeploy(event, {});
      expect(result.text).toMatch(/AWS CodeDeploy Notification/);
    });
    it('works with missing SNS and falls back', () => {
      const event = { Records: [{ Sns: {} }] };
      const result = index.handleCodeDeploy(event, {});
      expect(typeof result).toBe('object');
      expect(result.attachments[0].fields.length).toBeGreaterThan(0);
    });
    it('handles no Records (default fallback)', () => {
      const event = {};
      const result = index.handleCodeDeploy(event, {});
      expect(typeof result).toBe('object');
    });
  });
});