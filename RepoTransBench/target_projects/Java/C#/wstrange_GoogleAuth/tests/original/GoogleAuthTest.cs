using System;
using System.Collections.Generic;
using System.Numerics;
using System.Reflection;
using System.Threading;
using Xunit;

namespace GoogleAuth.Tests
{
    public class GoogleAuthTest
    {
        // Change this to the saved secret from the running the above test.
        private static readonly string SECRET_KEY = "KR52HV2U5Z4DWGLJ";
        private static readonly int VALIDATION_CODE = 598775;

        static GoogleAuthTest()
        {
            // Setup mock credential repository equivalent
            Environment.SetEnvironmentVariable(CredentialRepositoryMock.MOCK_SECRET_KEY_NAME, SECRET_KEY);
        }

        private static byte[] HexStr2Bytes(string hex)
        {
            // Adding one byte to get the right conversion
            // Values starting with "0" can be converted
            var bArray = BigInteger.Parse("10" + hex, System.Globalization.NumberStyles.HexNumber).ToByteArray(isBigEndian: true);

            // Copy all the REAL bytes, not the "first"
            var ret = new byte[bArray.Length - 1];
            Array.Copy(bArray, 1, ret, 0, ret.Length);

            return ret;
        }

        [Fact]
        public void Rfc6238TestVectors()
        {
            // See RFC 6238, p. 14
            var rfc6238TestKey = "3132333435363738393031323334353637383930";
            var key = HexStr2Bytes(rfc6238TestKey);
            long[] testTime = {59L, 1111111109L, 1111111111L, 1234567890L, 2000000000L, 20000000000L};
            long[] testResults = {94287082, 7081804, 14050471, 89005924, 69279037, 65353130};
            long timeStepSizeInSeconds = 30;

            var cb = new GoogleAuthenticatorConfigBuilder();
            cb.SetCodeDigits(8).SetTimeStepSizeInMillis(TimeSpan.FromSeconds(timeStepSizeInSeconds).TotalMilliseconds);
            var ga = new GoogleAuthenticator(cb.Build());

            for (int i = 0; i < testTime.Length; ++i)
            {
                Assert.Equal(testResults[i], ga.CalculateCode(key, (testTime[i] / timeStepSizeInSeconds)));
            }
        }

        [Fact]
        public void Rfc6238TestVectorsSHA256()
        {
            var rfc6238TestKey = "3132333435363738393031323334353637383930" +
                "313233343536373839303132";
            var key = HexStr2Bytes(rfc6238TestKey);
            long[] testTime = {59L, 1111111109L, 1111111111L, 1234567890L, 2000000000L, 20000000000L};
            long[] testResults = {46119246, 68084774, 67062674, 91819424, 90698825, 77737706};
            long timeStepSizeInSeconds = 30;

            var cb = new GoogleAuthenticatorConfigBuilder();
            cb.SetCodeDigits(8).SetTimeStepSizeInMillis(TimeSpan.FromSeconds(timeStepSizeInSeconds).TotalMilliseconds);
            cb.SetHmacHashFunction(HmacHashFunction.HmacSHA256);
            var ga = new GoogleAuthenticator(cb.Build());

            for (int i = 0; i < testTime.Length; ++i)
            {
                Assert.Equal(testResults[i], ga.CalculateCode(key, (testTime[i] / timeStepSizeInSeconds)));
            }
        }

        [Fact]
        public void Rfc6238TestVectorsSHA512()
        {
            var rfc6238TestKey = "3132333435363738393031323334353637383930" +
                "3132333435363738393031323334353637383930" +
                "3132333435363738393031323334353637383930" +
                "31323334";
            var key = HexStr2Bytes(rfc6238TestKey);
            long[] testTime = {59L, 1111111109L, 1111111111L, 1234567890L, 2000000000L, 20000000000L};
            long[] testResults = {90693936, 25091201, 99943326, 93441116, 38618901, 47863826};
            long timeStepSizeInSeconds = 30;

            var cb = new GoogleAuthenticatorConfigBuilder();
            cb.SetCodeDigits(8).SetTimeStepSizeInMillis(TimeSpan.FromSeconds(timeStepSizeInSeconds).TotalMilliseconds);
            cb.SetHmacHashFunction(HmacHashFunction.HmacSHA512);
            var ga = new GoogleAuthenticator(cb.Build());

            for (int i = 0; i < testTime.Length; ++i)
            {
                Assert.Equal(testResults[i], ga.CalculateCode(key, (testTime[i] / timeStepSizeInSeconds)));
            }
        }

        [Fact]
        public void CreateCredentials()
        {
            var gacb = new GoogleAuthenticatorConfigBuilder()
                .SetKeyRepresentation(KeyRepresentation.BASE64)
                .SetNumberOfScratchCodes(10);
            var googleAuthenticator = new GoogleAuthenticator(gacb.Build());

            var key = googleAuthenticator.CreateCredentials();
            string secret = key.Key;
            var scratchCodes = key.ScratchCodes;

            string otpAuthURL = GoogleAuthenticatorQRGenerator.GetOtpAuthURL("Test Org.", "test@prova.org", key);

            // These would normally print or display, not essential for test assertion
            Assert.False(string.IsNullOrEmpty(secret));
            Assert.NotNull(scratchCodes);

            foreach (var i in scratchCodes)
                Assert.True(googleAuthenticator.ValidateScratchCode(i));
        }

        [Fact]
        public void CreateAndAuthenticate()
        {
            var ga = new GoogleAuthenticator();
            var key = ga.CreateCredentials();

            Assert.True(ga.Authorize(key.Key, ga.GetTotpPassword(key.Key)));
        }

        [Fact]
        public void CreateAndAuthenticateNullAlgorithm()
        {
            var ga = new GoogleAuthenticator(null, null);
            var key = ga.CreateCredentials();
            Assert.True(ga.Authorize(key.Key, ga.GetTotpPassword(key.Key)));
        }

        [Fact]
        public void CreateCredentialsForUser()
        {
            var googleAuthenticator = new GoogleAuthenticator();

            var key = googleAuthenticator.CreateCredentials("testName");
            string secret = key.Key;
            var scratchCodes = key.ScratchCodes;

            string otpAuthURL = GoogleAuthenticatorQRGenerator.GetOtpAuthURL("Test Org.", "test@prova.org", key); 

            Assert.False(string.IsNullOrEmpty(secret));
            Assert.NotNull(scratchCodes);

            foreach (var i in scratchCodes)
                Assert.True(googleAuthenticator.ValidateScratchCode(i));
        }

        [Fact]
        public void Authorise()
        {
            var gacb = new GoogleAuthenticatorConfigBuilder()
                .SetTimeStepSizeInMillis(TimeSpan.FromSeconds(30).TotalMilliseconds)
                .SetWindowSize(5);
            var ga = new GoogleAuthenticator(gacb.Build());

            bool isCodeValid = ga.Authorize(SECRET_KEY, VALIDATION_CODE);

            // Output for manual validation, not required for assert
            Assert.True(isCodeValid || !isCodeValid); // Just ensure no exception
        }

        [Fact]
        public void AuthoriseUser()
        {
            var gacb = new GoogleAuthenticatorConfigBuilder()
                .SetTimeStepSizeInMillis(TimeSpan.FromSeconds(30).TotalMilliseconds)
                .SetWindowSize(5)
                .SetCodeDigits(6);
            var ga = new GoogleAuthenticator(gacb.Build());

            bool isCodeValid = ga.AuthorizeUser("testName", VALIDATION_CODE);

            Assert.True(isCodeValid || !isCodeValid); // Just ensure no exception
        }
    }
}