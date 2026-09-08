from itsdangerous.exc import BadSignature, BadPayload, BadTimeSignature, SignatureExpired

def test_bad_signature_str_public():
    # Only the reason arg is supported in public API
    sig = BadSignature("Diff reason")
    assert "Diff reason" in str(sig)

def test_bad_payload_str_public():
    bp = BadPayload("Different")
    assert "Different" in str(bp)

def test_bad_time_signature_str_public():
    # Only message arg is guaranteed (payload/date_signed are non-API)
    bts = BadTimeSignature("ReasonZZZ")
    out = str(bts)
    assert "ReasonZZZ" in out

def test_signature_expired_str_public():
    # Only message arg is guaranteed (payload/date_signed are non-API)
    se = SignatureExpired("Late!")
    out = str(se)
    assert "Late!" in out