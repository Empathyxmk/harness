using System;
using Xunit;
using AESCryptLib;
using System.Security.Cryptography;

namespace AESCryptPublicTests
{
    public class ApplicationPublicTest
    {
        [Fact]
        public void TestEncryptDecryptPublic()
        {
            string password = "anotherSecret";
            string message = "public test string!";

            // Set debug enabled if needed
            AESCrypt.DEBUG_LOG_ENABLED = true;

            string encryptedMsg = null;
            try
            {
                encryptedMsg = AESCrypt.Encrypt(password, message);
            }
            catch (CryptographicException)
            {
                Assert.True(false, "error occurred during encrypt in public test");
            }
            catch (ArgumentNullException)
            {
                Assert.True(false, "null param during encrypt in public test");
            }

            string messageAfterDecrypt = null;
            try
            {
                messageAfterDecrypt = AESCrypt.Decrypt(password, encryptedMsg);
            }
            catch (CryptographicException)
            {
                Assert.True(false, "error occurred during decrypt in public test");
            }
            catch (ArgumentNullException)
            {
                Assert.True(false, "null param during decrypt in public test");
            }

            Assert.Equal(message, messageAfterDecrypt);
        }

        [Fact]
        public void TestEncryptPublic()
        {
            string password = "publicPass";
            string message = "anotherMessage";

            try
            {
                string encryptedMsg = AESCrypt.Encrypt(password, message);
                Assert.NotNull(encryptedMsg);
            }
            catch (CryptographicException)
            {
                Assert.True(false, "error occurred during encrypt in public test");
            }
            catch (ArgumentNullException)
            {
                Assert.True(false, "null param during encrypt in public test");
            }
        }

        [Fact]
        public void TestDecryptPublic()
        {
            string password = "somePassword";
            string encryptedMsg = "i5OSk38FnX6OGv5CeXf2iA==";
            try
            {
                string result = AESCrypt.Decrypt(password, encryptedMsg);
                Assert.Equal("testOne", result);
            }
            catch (CryptographicException)
            {
                Assert.True(false, "error occurred during decrypt in public test");
            }
            catch (ArgumentNullException)
            {
                Assert.True(false, "null param during decrypt in public test");
            }
        }
    }
}