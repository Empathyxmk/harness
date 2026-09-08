using System;
using Xunit;
using AESCryptLib;
using System.Security.Cryptography;

namespace AESCryptPublicTests
{
    public class AESCryptDebugPublicTest
    {
        [Fact]
        public void TestEncryptDecryptWithDebugPublic()
        {
            bool oldDebug = AESCrypt.DEBUG_LOG_ENABLED;
            AESCrypt.DEBUG_LOG_ENABLED = true;
            string password = "pubDebugPass128";
            string message = "Debug public test message with 128";
            string encryptedMsg = AESCrypt.Encrypt(password, message);
            string decryptedMsg = AESCrypt.Decrypt(password, encryptedMsg);
            Assert.Equal(message, decryptedMsg);
            AESCrypt.DEBUG_LOG_ENABLED = oldDebug;
        }

        [Fact]
        public void TestWrongPasswordDecryptionPublic()
        {
            string password = "pubDebugPassword";
            string wrongPassword = "pubDebugWrongPwd";
            string message = "Different message for debug";
            string encryptedMsg = null;
            try
            {
                encryptedMsg = AESCrypt.Encrypt(password, message);
            }
            catch (CryptographicException e)
            {
                Assert.True(false, $"Encrypt should not throw in debug public test: {e.Message}");
            }

            Assert.Throws<CryptographicException>(() => AESCrypt.Decrypt(wrongPassword, encryptedMsg));
        }

        [Fact]
        public void TestEncryptDecryptWithUnicodePublic()
        {
            string password = "Pública123!";
            string message = "Тестовое сообщение 🌍";
            string encryptedMsg = AESCrypt.Encrypt(password, message);
            string decryptedMsg = AESCrypt.Decrypt(password, encryptedMsg);
            Assert.Equal(message, decryptedMsg);
        }
    }
}