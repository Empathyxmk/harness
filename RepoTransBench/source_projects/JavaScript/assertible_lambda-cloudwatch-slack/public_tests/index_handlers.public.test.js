const index = require('../index');
const _ = require('lodash');

// Helper for Elastic Beanstalk events (public data)
function makeElasticBeanstalkEvent(message, subject) {
  return {
    Records: [{
      Sns: {
        Message: message,
        Subject: subject !== undefined ? subject : 'EbEnv Subject',
        Timestamp: '2022-08-15T12:34:56Z'
      }
    }]
  };
}

// Helper for CodeDeploy events (public data)
function makeCodeDeployEvent(msg, subject) {
  return {
    Records: [{
      Sns: {
        Message: typeof msg === 'string' ? msg : JSON.stringify(msg),
        Subject: subject !== undefined ? subject : 'CD Deployment',
        Timestamp: '2023-02-21T15:24:10Z'
      }
    }]
  };
}

describe('index.js handlers (public test data)', () => {
  describe('handleElasticBeanstalk', () => {
    it('returns good color for alternative message', () => {
      const event = makeElasticBeanstalkEvent('Deployment completed successfully');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('good');
      expect(result.attachments[0].fields[1].value).toContain('Deployment');
    });
    it('returns danger for RED alert message', () => {
      const event = makeElasticBeanstalkEvent('ALERT: Environment status changed to RED state.');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('danger');
    });
    it('returns danger for severity indicated', () => {
      const event = makeElasticBeanstalkEvent('CRITICAL severity warning detected.');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('danger');
    });
    it('returns warning for yellow notification', () => {
      const event = makeElasticBeanstalkEvent('Warning: YELLOW health level reported.');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('warning');
    });
    it('returns warning when info is present', () => {
      const event = makeElasticBeanstalkEvent('Info: Environment running smoothly.');
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.attachments[0].color).toBe('warning');
    });
    it('uses hardcoded subject when SNS subject is removed', () => {
      const event = makeElasticBeanstalkEvent('Recovery notice', undefined);
      delete event.Records[0].Sns.Subject;
      const result = index.handleElasticBeanstalk(event, {});
      expect(result.text).toMatch(/AWS Elastic Beanstalk Notification/);
    });
  });

  describe('handleCodeDeploy', () => {
    const demoMessage = {
      deploymentGroupName: "AnotherGroup",
      applicationName: "SampleApp",
      status: "FAILED"
    };
    it('parses JSON message with FAILED status (public)', () => {
      const event = makeCodeDeployEvent({ ...demoMessage, status: "FAILED" });
      const result = index.handleCodeDeploy(event, {});
      expect(result.attachments[0].color).toBe('danger');
      expect(result.attachments[0].fields[1].title).toBe('Deployment Group');
    });
    it('parses JSON message with SUCCEEDED status (good) in public data', () => {
      const event = makeCodeDeployEvent({ ...demoMessage, status: "SUCCEEDED" });
      const result = index.handleCodeDeploy(event, {});
      expect(result.attachments[0].color).toBe('good');
    });
    it('parses JSON message with IN_PROGRESS status (warning)', () => {
      const event = makeCodeDeployEvent({ ...demoMessage, status: "IN_PROGRESS" });
      const result = index.handleCodeDeploy(event, {});
      expect(result.attachments[0].color).toBe('warning');
    });
    it('falls back to string message on parse error (public)', () => {
      const event = makeCodeDeployEvent("deployment event string");
      const result = index.handleCodeDeploy(event, {});
      expect(result.attachments[0].fields[1].title).toBe('Message');
    });
    it('handles JSON without deploymentGroupName (public)', () => {
      const event = makeCodeDeployEvent({ status: "SUCCEEDED" });
      const result = index.handleCodeDeploy(event, {});
      expect(result.attachments[0].fields[1].title).toBe('Deployment Group');
    });
    it('works when SNS subject missing (public)', () => {
      const event = makeCodeDeployEvent({ ...demoMessage });
      delete event.Records[0].Sns.Subject;
      const result = index.handleCodeDeploy(event, {});
      expect(result.text).toMatch(/AWS CodeDeploy Notification/);
    });
    it('works with missing SNS and falls back (public)', () => {
      const event = { Records: [{ Sns: {} }] };
      const result = index.handleCodeDeploy(event, {});
      expect(typeof result).toBe('object');
      expect(result.attachments[0].fields.length).toBeGreaterThan(0);
    });
    it('handles no Records (public fallback)', () => {
      const event = {};
      const result = index.handleCodeDeploy(event, {});
      expect(typeof result).toBe('object');
    });
  });
});