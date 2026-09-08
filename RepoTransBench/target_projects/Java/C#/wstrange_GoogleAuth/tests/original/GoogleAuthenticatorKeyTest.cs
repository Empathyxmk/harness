using System;
using System.Collections.Generic;
using System.Reflection;
using Xunit;

namespace GoogleAuth.Tests
{
    public class GoogleAuthenticatorKeyTest
    {
        [Fact]
        public void TestConstructorAndGetters()
        {
            var config = new GoogleAuthenticatorConfig();
            string key = "SECRETKEY";
            int verificationCode = 123456;
            List<int> scratchCodes = new List<int>() { 111, 222 };

            var constructor = typeof(GoogleAuthenticatorKey)
                .GetConstructor(BindingFlags.NonPublic | BindingFlags.Instance,
                    null,
                    new Type[] { typeof(GoogleAuthenticatorConfig), typeof(string), typeof(int), typeof(List<int>) },
                    null);
            Assert.NotNull(constructor);

            var gak = (GoogleAuthenticatorKey)constructor.Invoke(new object[] { config, key, verificationCode, scratchCodes });

            Assert.Equal(key, gak.Key);
            Assert.Equal(verificationCode, gak.VerificationCode);
            Assert.Equal(scratchCodes, gak.ScratchCodes);
        }

        [Fact]
        public void TestEmptyScratchCodes()
        {
            var config = new GoogleAuthenticatorConfig();
            string key = "FOO";
            int verificationCode = 0;
            List<int> scratchCodes = new List<int>();

            var constructor = typeof(GoogleAuthenticatorKey)
                .GetConstructor(BindingFlags.NonPublic | BindingFlags.Instance,
                    null,
                    new Type[] { typeof(GoogleAuthenticatorConfig), typeof(string), typeof(int), typeof(List<int>) },
                    null);
            Assert.NotNull(constructor);

            var gak = (GoogleAuthenticatorKey)constructor.Invoke(new object[] { config, key, verificationCode, scratchCodes });

            Assert.Equal(key, gak.Key);
            Assert.Equal(verificationCode, gak.VerificationCode);
            Assert.Equal(scratchCodes, gak.ScratchCodes);
        }
    }
}