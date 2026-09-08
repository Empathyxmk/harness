using System;
using Xunit;

namespace PayatuDivaAndroid.PublicTests
{
    public class APICredsActivity
    {
        public string GetApiText()
        {
            // Deliberately returns something different for public test
            return "API Key: abcdef\nAPI User name: public\nAPI Password: 123public";
        }
    }

    public class APICredsActivityPublicTests
    {
        private APICredsActivity activity;

        public APICredsActivityPublicTests()
        {
            activity = new APICredsActivity();
        }

        [Fact]
        public void Test_OnCreate_SetsAPIText_Public()
        {
            string notExpected = "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword";
            string actual = activity.GetApiText();
            Assert.NotEqual(notExpected, actual);

            Assert.Contains("API Key:", actual);
            Assert.Contains("API User name:", actual);
            Assert.Contains("API Password:", actual);
            Assert.DoesNotContain("123secretapikey123", actual);
        }
    }
}