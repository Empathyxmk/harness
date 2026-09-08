using Xunit;
using System.Collections.Generic;
using FastDFSClient;

namespace FastDFSClient.Tests
{
    public class ClientGlobalTests
    {
        [Fact]
        public void TestInitConfig()
        {
            string trackerServers = "10.0.11.101:22122,10.0.11.102:22122";
            ClientGlobal.InitByTrackers(trackerServers);
            Assert.Contains("10.0.11.101:22122", ClientGlobal.ConfigInfo());
            Assert.Contains("10.0.11.102:22122", ClientGlobal.ConfigInfo());

            string propFilePath = "fastdfs-client.properties";
            ClientGlobal.InitByProperties(propFilePath);
            Assert.Contains("fastdfs-client.properties", ClientGlobal.ConfigInfo());

            var props = new Dictionary<string, string>();
            props[ClientGlobal.PROP_KEY_TRACKER_SERVERS] = "10.0.11.101:22122,10.0.11.102:22122";
            ClientGlobal.InitByProperties(props);
            Assert.Contains("10.0.11.101:22122", ClientGlobal.ConfigInfo());

            string trackerServer = "www.baidu.com:22122";
            ClientGlobal.InitByTrackers(trackerServer);
            Assert.Contains("www.baidu.com:22122", ClientGlobal.ConfigInfo());
        }
    }
}