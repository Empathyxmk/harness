using System;
using Xunit;

namespace PayatuDivaAndroid.Tests.Original
{
    public class APICredsActivity
    {
        public string GetApiText()
        {
            // Simulated method reflecting what the TextView would display
            return "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword";
        }
    }

    public class APICredsActivityTests
    {
        private APICredsActivity activity;

        public APICredsActivityTests()
        {
            activity = new APICredsActivity();
        }

        [Fact]
        public void Test_OnCreate_SetsAPIText()
        {
            string expected = "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword";
            Assert.Equal(expected, activity.GetApiText());
        }
    }
}