using Xunit;
using FastDFSClient;

namespace FastDFSClient.Tests
{
    public class IniFileReaderTests
    {
        [Fact]
        public void TestReadConfig()
        {
            string conf_filename = "fdfs_client.conf";
            var iniFileReader = new IniFileReader(conf_filename);
            Assert.Equal(conf_filename, iniFileReader.ConfFilename);
            Assert.Equal(3, iniFileReader.GetIntValue("connect_timeout", 3));
            Assert.Equal(45, iniFileReader.GetIntValue("network_timeout", 45));
            Assert.Equal("UTF-8", iniFileReader.GetStrValue("charset"));
            Assert.Equal(8080, iniFileReader.GetIntValue("http.tracker_http_port", 8080));
            Assert.False(iniFileReader.GetBoolValue("http.anti_steal_token", false));
            Assert.Equal("secret", iniFileReader.GetStrValue("http.secret_key"));

            string[] tracker_servers = iniFileReader.GetValues("tracker_server");
            Assert.NotNull(tracker_servers);
            Assert.True(tracker_servers.Length > 0);
        }
    }
}