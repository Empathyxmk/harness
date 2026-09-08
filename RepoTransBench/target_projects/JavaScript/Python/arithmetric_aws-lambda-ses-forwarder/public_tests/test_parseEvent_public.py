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

def test_resolves_with_email_and_recipients_for_valid_ses_event():
    called_logs = []
    def mockLog(msg):
        called_logs.append(msg)
    data = {
        "event": {
            "Records": [
                {
                    "eventSource": "aws:ses",
                    "eventVersion": "1.0",
                    "ses": {
                        "mail": {
                            "messageId": "unique-public-id-6789",
                            "source": "another.sender@example.net"
                        },
                        "receipt": {
                            "recipients": [
                                "public.test1@otherdomain.org",
                                "public.test2@otherdomain.net"
                            ]
                        }
                    }
                }
            ]
        },
        "log": mockLog
    }
    result = parseEvent(data)
    assert result.email == {
        "messageId": "unique-public-id-6789",
        "source": "another.sender@example.net"
    }
    assert result.recipients == [
        "public.test1@otherdomain.org",
        "public.test2@otherdomain.net"
    ]

def test_rejects_and_logs_error_on_invalid_ses_event():
    called_logs = []
    def mockLog(msg):
        called_logs.append(msg)
    data = {
        "event": {
            "Records": [
                {
                    "eventSource": "aws:sns",  # Not SES, should fail
                    "eventVersion": "1.0"
                }
            ]
        },
        "log": mockLog
    }
    with pytest.raises(Exception, match="invalid SES message"):
        parseEvent(data)
    # Was error log called?
    assert any(log.get("level") == "error" for log in called_logs)

def test_rejects_if_records_is_empty():
    called_logs = []
    def mockLog(msg):
        called_logs.append(msg)
    data = {
        "event": {
            "Records": []
        },
        "log": mockLog
    }
    with pytest.raises(Exception, match="invalid SES message"):
        parseEvent(data)
    # Was error log called?
    assert any(log.get("level") == "error" for log in called_logs)