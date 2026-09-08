using System;
using Xunit;
using AESCryptLib;
using System.Security.Cryptography;

namespace AESCryptOriginalTests
{
    public class AESCryptDebugTest
    {
        private const string PASSWORD = "mypassword";
        private const string MESSAGE = "test message for debug";
        private static readonly string ENCRYPTED = AESCrypt.Encrypt(PASSWORD, MESSAGE);

        public AESCryptDebugTest()
        {
            AESCrypt.DEBUG_LOG_ENABLED = true;
        }

        [Fact]
        public void TestEncryptDecrypt_DebugLog_Enabled()
        {
            string encrypted = AESCrypt.Encrypt(PASSWORD, MESSAGE);
            Assert.NotNull(encrypted);

            string decrypted = AESCrypt.Decrypt(PASSWORD, encrypted);
            Assert.Equal(MESSAGE, decrypted);
        }

        [Fact]
        public void TestEncrypt_InvalidAlgorithm_DebugLog()
        {
            byte[] badKey = System.Text.Encoding.UTF8.GetBytes("1234567890123456");
            byte[] iv = System.Text.Encoding.UTF8.GetBytes("1234567890123456");
            byte[] messageBytes = System.Text.Encoding.UTF8.GetBytes("hello");
            // Force an invalid key by corrupting it length for AES- use DES (invalid for AES)
            byte[] key = new byte[8]; Array.Copy(badKey, key, 8);

            Assert.ThrowsAny<CryptographicException>(() =>
            {
                // This should throw due to invalid key size for AES
                AESCrypt.Encrypt(key, iv, messageBytes);
            });
        }

        [Fact]
        public void TestDecrypt_InvalidBase64_DebugLog()
        {
            Assert.Throws<CryptographicException>(() =>
            {
                AESCrypt.Decrypt(PASSWORD, "not-base64-***");
            });
        }

        [Fact]
        public void TestDecrypt_InvalidCipher_DebugLog()
        {
            byte[] invalidBytes = System.Text.Encoding.UTF8.GetBytes("NotCipherText");
            string invalidBase64 = Convert.ToBase64String(invalidBytes);
            Assert.Throws<CryptographicException>(() =>
            {
                AESCrypt.Decrypt(PASSWORD, invalidBase64);
            });
        }
    }
}