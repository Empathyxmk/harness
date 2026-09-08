const { parseEvent } = require('../index');

describe('parseEvent (public test cases with unique data)', () => {
  it('should resolve with data including email and recipients for a valid SES event (public test)', async () => {
    const mockLog = jest.fn();
    // Use a different Message-Id for public test than traditional test would
    const data = {
      event: {
        Records: [
          {
            eventSource: "aws:ses",
            eventVersion: "1.0",
            ses: {
              mail: {
                messageId: "unique-public-id-6789",
                source: "another.sender@example.net"
              },
              receipt: {
                recipients: [
                  "public.test1@otherdomain.org",
                  "public.test2@otherdomain.net"
                ]
              }
            }
          }
        ]
      },
      log: mockLog
    };
    const result = await parseEvent(data);
    expect(result.email).toEqual({
      messageId: "unique-public-id-6789",
      source: "another.sender@example.net"
    });
    expect(result.recipients).toEqual([
      "public.test1@otherdomain.org",
      "public.test2@otherdomain.net"
    ]);
  });

  it('should reject and log error on invalid SES event (public test, different structure)', async () => {
    const mockLog = jest.fn();
    const data = {
      event: {
        Records: [
          {
            eventSource: "aws:sns", // Not SES, should fail
            eventVersion: "1.0"
          }
        ]
      },
      log: mockLog
    };
    await expect(parseEvent(data)).rejects.toThrow(/invalid SES message/);
    expect(mockLog).toHaveBeenCalledWith(
      expect.objectContaining({ level: 'error' })
    );
  });

  it('should reject if Records is empty (public test)', async () => {
    const mockLog = jest.fn();
    const data = {
      event: {
        Records: []
      },
      log: mockLog
    };
    await expect(parseEvent(data)).rejects.toThrow(/invalid SES message/);
    expect(mockLog).toHaveBeenCalledWith(
      expect.objectContaining({ level: 'error' })
    );
  });
});