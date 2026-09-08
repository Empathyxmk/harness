using System.Collections.Generic;
using Xunit;

namespace GoogleAuth.Tests
{
    public class GoogleAuthenticatorQRGeneratorTest
    {
        private GoogleAuthenticatorKey credentials;

        public GoogleAuthenticatorQRGeneratorTest()
        {
            var config = new GoogleAuthenticatorConfigBuilder().Build();
            credentials = new GoogleAuthenticatorKey
                    .Builder("secretKey")
                    .SetConfig(config)
                    .SetVerificationCode(123456)
                    .SetScratchCodes(new List<int>())
                    .Build();
        }

        [Fact]
        public void TestGetOtpAuthURL()
        {
            Assert.Equal(
                "https://api.qrserver.com/v1/create-qr-code/?data=otpauth%3A%2F%2Ftotp%2FAcme%3Aalice%40example.com%3Fsecret%3DsecretKey%26issuer%3DAcme%26algorithm%3DSHA1%26digits%3D6%26period%3D30&size=200x200&ecc=M&margin=10",
                GoogleAuthenticatorQRGenerator.GetOtpAuthURL("Acme", "alice@example.com", credentials)
            );
        }

        [Fact]
        public void TestGetOtpAuthTotpURL()
        {
            Assert.Equal(
                "otpauth://totp/Acme:alice@example.com?secret=secretKey&issuer=Acme&algorithm=SHA1&digits=6&period=30",
                GoogleAuthenticatorQRGenerator.GetOtpAuthTotpURL("Acme", "alice@example.com", credentials));

            Assert.Equal(
                "otpauth://totp/Acme%20Inc:alice%20at%20Inc?secret=secretKey&issuer=Acme+Inc&algorithm=SHA1&digits=6&period=30",
                GoogleAuthenticatorQRGenerator.GetOtpAuthTotpURL("Acme Inc", "alice at Inc", credentials));

            Assert.Equal(
                "otpauth://totp/Acme%20&%20%3Cfriends%3E:alice%2523?secret=secretKey&issuer=Acme+%26+%3Cfriends%3E&algorithm=SHA1&digits=6&period=30",
                GoogleAuthenticatorQRGenerator.GetOtpAuthTotpURL("Acme & <friends>", "alice%23", credentials));
        }
    }
}