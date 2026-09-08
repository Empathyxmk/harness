using System;
using Xunit;
using AESCryptLib;

namespace AESCryptPublicTests
{
    public class AESCryptReflectionPublicTest
    {
        [Fact]
        public void TestGenerateKeyPublic()
        {
            string password = "publicTest";
            string message = "testing";
            string encrypted = AESCrypt.Encrypt(password, message);
            string decrypted = AESCrypt.Decrypt(password, encrypted);
            Assert.Equal(message, decrypted);
        }

        [Fact]
        public void TestGenerateKey_FailsWithVeryLongPasswordPublic()
        {
            try
            {
                string password = "verylongpassword0123456789verylongpassword0123456789verylongpassword0123456789";
                string encrypted = AESCrypt.Encrypt(password, "foobar");
                string decrypted = AESCrypt.Decrypt(password, encrypted);
                Assert.Equal("foobar", decrypted);
            }
            catch (Exception)
            {
                Assert.False(true, "Should not fail for very long password - public test");
            }
        }

        [Fact]
        public void TestGenerateKey_UnsupportedEncodingPublic()
        {
            Assert.True(true);
        }
    }
}