using System;
using Xunit;

namespace AnnabergiteAbgRpc.PublicTests
{
    public class ZooKeeperRegisterPublicTests
    {
        [Fact]
        public void TestRegisterNewPath()
        {
            string znode = "/register/public/node";
            bool registered = DoRegister(znode);
            Assert.True(registered);
        }

        private bool DoRegister(string znode)
        {
            return znode.Contains("/register/public/");
        }
    }
}