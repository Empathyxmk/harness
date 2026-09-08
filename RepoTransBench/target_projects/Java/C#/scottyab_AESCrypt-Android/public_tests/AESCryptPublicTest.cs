using System;
using Xunit;
using AESCryptLib;
using System.Security.Cryptography;

namespace AESCryptPublicTests
{
    public class AESCryptPublicTest
    {
        [Fact]
        public void TestEncryptDecryptWithDifferentDataPublic()
        {
            string password = "321secret";
            string message = "Public AESCrypt test 42.";
            string encryptedMsg = AESCrypt.Encrypt(password, message);
            string decryptedMsg = AESCrypt.Decrypt(password, encryptedMsg);
            Assert.Equal(message, decryptedMsg);
        }

        [Fact]
        public void TestDecryptPrecomputedCiphertextPublic()
        {
            string password = "public123";
            string encryptedMsg = "Ru4RNkDqQboiRkHi7U0koA==";
            string result = AESCrypt.Decrypt(password, encryptedMsg);
            Assert.Equal("helloPublic", result);
        }

        [Fact]
        public void TestEncryptDecryptEmptyStringPublic()
        {
            string password = "emptyCase";
            string message = "";
            string encryptedMsg = AESCrypt.Encrypt(password, message);
            string decryptedMsg = AESCrypt.Decrypt(password, encryptedMsg);
            Assert.Equal(message, decryptedMsg);
        }

        [Fact]
        public void TestEncryptDecryptWithSpecialCharactersPublic()
        {
            string password = "specialP@sswørd";
            string message = "!@#$%^&*()_+-=[]{};':,.<>/?`~";
            string encryptedMsg = AESCrypt.Encrypt(password, message);
            string decryptedMsg = AESCrypt.Decrypt(password, encryptedMsg);
            Assert.Equal(message, decryptedMsg);
        }

        [Fact]
        public void TestDecryptFailWithWrongPasswordPublic()
        {
            string password = "correctPassword";
            string wrongPassword = "incorrectPassword";
            string message = "Mismatch password public";
            string encrypted = AESCrypt.Encrypt(password, message);
            Assert.Throws<CryptographicException>(() => AESCrypt.Decrypt(wrongPassword, encrypted));
        }
    }
}