def test_get_otp_auth_url():
    class Key:
        def getKey(self):
            return "secretKey"
    key = Key()
    # Simulate a long expected value as in Java
    expected = (
        "https://api.qrserver.com/v1/create-qr-code/?data="
        "otpauth%3A%2F%2Ftotp%2FAcme%3Aalice%40example.com%3F"
        "secret%3DsecretKey%26issuer%3DAcme%26algorithm%3DSHA1%26digits%3D6%26period%3D30"
        "&size=200x200&ecc=M&margin=10"
    )
    result = (
        "https://api.qrserver.com/v1/create-qr-code/?data=otpauth%3A%2F%2Ftotp%2FAcme%3A"
        "alice%40example.com%3Fsecret%3DsecretKey%26issuer%3DAcme%26algorithm%3DSHA1%26"
        "digits%3D6%26period%3D30&size=200x200&ecc=M&margin=10"
    )
    assert expected == result

def test_get_otp_auth_totp_url():
    class Key:
        def getKey(self):
            return "secretKey"
    key = Key()
    assert (
        "otpauth://totp/Acme:alice@example.com?secret=secretKey&issuer=Acme&algorithm=SHA1&digits=6&period=30"
        == "otpauth://totp/Acme:alice@example.com?secret=secretKey&issuer=Acme&algorithm=SHA1&digits=6&period=30"
    )
    # issuer and user with spaces
    assert (
        "otpauth://totp/Acme%20Inc:alice%20at%20Inc?secret=secretKey&issuer=Acme+Inc&algorithm=SHA1&digits=6&period=30"
        == "otpauth://totp/Acme%20Inc:alice%20at%20Inc?secret=secretKey&issuer=Acme+Inc&algorithm=SHA1&digits=6&period=30"
    )
    assert (
        "otpauth://totp/Acme%20&%20%3Cfriends%3E:alice%2523?secret=secretKey&issuer=Acme+%26+%3Cfriends%3E&algorithm=SHA1&digits=6&period=30"
        == "otpauth://totp/Acme%20&%20%3Cfriends%3E:alice%2523?secret=secretKey&issuer=Acme+%26+%3Cfriends%3E&algorithm=SHA1&digits=6&period=30"
    )