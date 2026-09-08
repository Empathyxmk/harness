// Smoke test that index exports parseEvent and it works with a minimal valid event (different test data)
const { parseEvent } = require('../index');

describe('aws-lambda-ses-forwarder index smoke (public test, different data)', () => {
  it('should export a parseEvent function', () => {
    expect(typeof parseEvent).toBe('function');
  });

  it('should parse a minimally valid SES event (public test)', async () => {
    const mockLog = jest.fn();
    const fakeMail = { messageId: 'abcd1234-public', source: 'smoke+source@exam.pl' };
    const fakeRecipients = ['smoke-test@diff-domain.org'];
    const data = {
      event: {
        Records: [
          {
            eventSource: 'aws:ses',
            eventVersion: '1.0',
            ses: {
              mail: fakeMail,
              receipt: { recipients: fakeRecipients }
            }
          }
        ]
      },
      log: mockLog
    };
    const result = await parseEvent(data);
    expect(result.email).toEqual(fakeMail);
    expect(result.recipients).toEqual(fakeRecipients);
  });
});