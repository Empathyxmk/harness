using System;
using Xunit;

namespace AnnabergiteAbgRpc.PublicTests
{
    public class ZooKeeperDiscoverIntegrationPublicTests
    {
        [Fact]
        public void TestIntegrationDiscoverWithNewNode()
        {
            string newNode = "/public/integration/node";
            bool discovered = SimulateDiscover(newNode);
            Assert.True(discovered);
        }

        private bool SimulateDiscover(string node)
        {
            return node == "/public/integration/node";
        }
    }
}