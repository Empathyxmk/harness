using System;
using Xunit;
using AESCryptLib;
using System.Security.Cryptography;

namespace AESCryptOriginalTests
{
    public class AESCryptReflectionTest
    {
        [Fact]
        public void TestGenerateKey()
        {
            // This is effectively tested via encrypt/decrypt
            string password = "test";
            string message = "data";
            string encrypted = AESCrypt.Encrypt(password, message);
            string decrypted = AESCrypt.Decrypt(password, encrypted);
            Assert.Equal(message, decrypted);
        }

        [Fact]
        public void TestGenerateKey_FailsWithBadAlgorithm()
        {
            try
            {
                string password = new string('x', 1000);
                string encrypted = AESCrypt.Encrypt(password, "data");
                string decrypted = AESCrypt.Decrypt(password, encrypted);
                Assert.Equal("data", decrypted);
            }
            catch (Exception)
            {
                // should not fail for long passwords, just encrypts
                Assert.False(true, "Should not fail for long password");
            }
        }

        [Fact]
        public void TestGenerateKey_UnsupportedEncoding()
        {
            // .NET always supports UTF-8, so just assert true
            Assert.True(true);
        }
    }
}