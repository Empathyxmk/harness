using System.Net;
using Xunit;

namespace OriginalTests
{
    public class IpUtilsTest
    {
        [Fact]
        public void TestLocalhostAddress()
        {
            // Replace with the equivalent of IpUtils.getHostIp(), suppose it's Dns.GetHostName then Dns.GetHostAddresses
            string ip = Dns.GetHostAddresses(Dns.GetHostName())[0].ToString();
            Assert.False(string.IsNullOrEmpty(ip));
        }
    }
}