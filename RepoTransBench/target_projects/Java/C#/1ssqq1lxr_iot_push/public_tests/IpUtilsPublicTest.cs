using System.Net;
using Xunit;

namespace PublicTests
{
    public class IpUtilsPublicTest
    {
        [Fact]
        public void TestHostIpIsConsistentWithInetAddress()
        {
            string hostIp = Dns.GetHostAddresses(Dns.GetHostName())[0].ToString();
            Assert.False(string.IsNullOrWhiteSpace(hostIp));
            Assert.NotEqual("0.0.0.0", hostIp);
        }
    }
}