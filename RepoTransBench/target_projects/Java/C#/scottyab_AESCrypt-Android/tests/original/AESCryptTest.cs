using System;
using Xunit;
using AESCryptLib;
using System.Security.Cryptography;

namespace AESCryptOriginalTests
{
    public class AESCryptTest
    {
        [Fact]
        public void TestBasicEncryptDecrypt()
        {
            string password = "password";
            string message = "hello world";
            string encryptedMsg = AESCrypt.Encrypt(password, message);
            string decryptedMsg = AESCrypt.Decrypt(password, encryptedMsg);
            Assert.Equal(message, decryptedMsg);
        }

        [Fact]
        public void TestEncryptDecrypt_EmptyString()
        {
            string password = "password";
            string message = "";
            string encryptedMsg = AESCrypt.Encrypt(password, message);
            string decryptedMsg = AESCrypt.Decrypt(password, encryptedMsg);
            Assert.Equal(message, decryptedMsg);
        }

        [Fact]
        public void TestEncryptDecrypt_NonAscii()
        {
            string password = "password";
            string message = "こんにちは世界";
            string encryptedMsg = AESCrypt.Encrypt(password, message);
            string decryptedMsg = AESCrypt.Decrypt(password, encryptedMsg);
            Assert.Equal(message, decryptedMsg);
        }

        [Fact]
        public void TestDecrypt_WrongPassword()
        {
            string password = "password";
            string wrongPassword = "notMyPassword";
            string message = "hello world";
            string encryptedMsg = AESCrypt.Encrypt(password, message);
            Assert.Throws<CryptographicException>(() => AESCrypt.Decrypt(wrongPassword, encryptedMsg));
        }

        [Fact]
        public void TestDecrypt_InvalidBase64()
        {
            string password = "password";
            string invalidBase64 = "not_base64!";
            Assert.Throws<CryptographicException>(() => AESCrypt.Decrypt(password, invalidBase64));
        }

        [Fact]
        public void TestDecrypt_InvalidData()
        {
            string password = "password";
            string invalidData = "MTIzNA=="; // "1234" base64
            Assert.Throws<CryptographicException>(() => AESCrypt.Decrypt(password, invalidData));
        }

        [Fact]
        public void TestEncryptDecrypt_NullPassword()
        {
            string message = "hello";
            Assert.Throws<ArgumentNullException>(() => AESCrypt.Encrypt(null, message));
        }

        [Fact]
        public void TestEncryptDecrypt_NullMessage()
        {
            string password = "pw";
            Assert.Throws<ArgumentNullException>(() => AESCrypt.Encrypt(password, null));
        }

        [Fact]
        public void TestDirectEncryptDecrypt()
        {
            string pw = "testing";
            string msg = "msg";
            string encrypted = AESCrypt.Encrypt(pw, msg);
            string decrypted = AESCrypt.Decrypt(pw, encrypted);
            Assert.Equal(msg, decrypted);
        }
    }
}