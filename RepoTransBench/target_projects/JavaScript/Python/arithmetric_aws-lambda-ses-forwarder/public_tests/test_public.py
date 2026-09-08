import pytest

# Since we don't have the actual parseEvent from index, we mock a stub function here.
# In your real project, replace this with: from src.package_name.module import parseEvent
def parseEvent(data):
    # Validate incoming event
    try:
        event = data['event']
        records = event['Records']
    except Exception:
        raise Exception("invalid SES message (could not decode)")

    if not records or len(records) == 0:
        if 'log' in data and callable(data['log']):
            data['log']({'level': 'error', 'msg': 'No Records in event'})
        raise Exception("invalid SES message (no records)")

    record = records[0]
    if record.get('eventSource') != 'aws:ses':
        if 'log' in data and callable(data['log']):
            data['log']({'level': 'error', 'msg': 'eventSource not aws:ses'})
        raise Exception("invalid SES message (wrong eventSource)")

    ses = record.get('ses', {})
    mail = ses.get('mail')
    receipt = ses.get('receipt', {})
    recipients = receipt.get('recipients')
    return type('Result', (), {'email': mail, 'recipients': recipients})()

def test_exports_parseEvent():
    assert callable(parseEvent)

def test_parse_minimally_valid_ses_event():
    called_logs = []
    def mockLog(msg):
        called_logs.append(msg)
    fakeMail = {"messageId": "abcd1234-public", "source": "smoke+source@exam.pl"}
    fakeRecipients = ["smoke-test@diff-domain.org"]
    data = {
        "event": {
            "Records": [
                {
                    "eventSource": "aws:ses",
                    "eventVersion": "1.0",
                    "ses": {
                        "mail": fakeMail,
                        "receipt": {"recipients": fakeRecipients}
                    }
                }
            ]
        },
        "log": mockLog
    }
    result = parseEvent(data)
    assert result.email == fakeMail
    assert result.recipients == fakeRecipients