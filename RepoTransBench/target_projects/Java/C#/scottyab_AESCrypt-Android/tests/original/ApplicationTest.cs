using System;
using Xunit;
using AESCryptLib;
using System.Security.Cryptography;

namespace AESCryptOriginalTests
{
    public class ApplicationTest
    {
        [Fact]
        public void TestEncryptDecrypt()
        {
            string password = "password";
            string message = "hello world";
            AESCrypt.DEBUG_LOG_ENABLED = true;

            string encryptedMsg = null;
            try
            {
                encryptedMsg = AESCrypt.Encrypt(password, message);
            }
            catch (CryptographicException)
            {
                Assert.True(false, "error occurred during encrypt");
            }
            catch (ArgumentNullException)
            {
                Assert.True(false, "null param during encrypt");
            }

            string messageAfterDecrypt = null;
            try
            {
                messageAfterDecrypt = AESCrypt.Decrypt(password, encryptedMsg);
            }
            catch (CryptographicException)
            {
                Assert.True(false, "error occurred during Decrypt");
            }
            catch (ArgumentNullException)
            {
                Assert.True(false, "null param during Decrypt");
            }

            Assert.Equal(message, messageAfterDecrypt);
        }

        [Fact]
        public void TestEncryt()
        {
            string password = "password";
            string message = "hello world";

            try
            {
                string encryptedMsg = AESCrypt.Encrypt(password, message);
            }
            catch (CryptographicException)
            {
                Assert.True(false, "error occurred during encrypt");
            }
            catch (ArgumentNullException)
            {
                Assert.True(false, "null param during encrypt");
            }
        }

        [Fact]
        public void TestDecrpyt()
        {
            string password = "password";
            string encryptedMsg = "2B22cS3UC5s35WBihLBo8w==";

            try
            {
                string messageAfterDecrypt = AESCrypt.Decrypt(password, encryptedMsg);
            }
            catch (CryptographicException)
            {
                Assert.True(false, "error occurred during Decrypt");
            }
            catch (ArgumentNullException)
            {
                Assert.True(false, "null param during Decrypt");
            }
        }
    }
}