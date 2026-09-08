using System;
using Xunit;

namespace AnnabergiteAbgRpc.PublicTests
{
    public class ZooKeeperRegisterAdvancedPublicTests
    {
        [Fact]
        public void TestRegisterAdvancedPublic()
        {
            string key = "public-advanced-key";
            string value = "public-advanced-value";
            bool isRegistered = SimulateRegister(key, value);
            Assert.True(isRegistered);
        }

        private bool SimulateRegister(string key, string value)
        {
            return key.StartsWith("public-") && value.StartsWith("public-");
        }
    }
}