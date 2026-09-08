using System;
using System.Collections.Generic;
using Xunit;
using Moq;

namespace AnnabergiteAbgRpc.Tests.Original
{
    public class ZooKeeperRegisterTests
    {
        [Fact]
        public void TestInitAndRegisterNullCheck()
        {
            var register = new ZooKeeperRegisterImpl();
            var protocol = new Mock<IProtocol>();
            string serverAddr = "127.0.0.1:9876";
            var hosts = new List<string> { "localhost:2181" };

            register.Init(hosts);

            // Try invalid prereq: no client assigned
            var tmp = new ZooKeeperRegisterImpl();
            Assert.Throws<NullReferenceException>(() =>
                tmp.Register("g", "a", protocol.Object, serverAddr, 1)
            );
        }
    }

    // Reuse IProtocol from above
    public interface IProtocol { string ToString(); }

    public interface IZooKeeperRegister
    {
        void Init(List<string> hosts);
        void Register(string group, string app, IProtocol protocol, string hostPort, int value);
    }
    public class ZooKeeperRegisterImpl : IZooKeeperRegister
    {
        public IClient Client { get; set; }
        public void Init(List<string> hosts) { }
        public void Register(string group, string app, IProtocol protocol, string hostPort, int value)
        {
            if (Client == null) throw new NullReferenceException();
            var path = $"/abg/{group}/{app}/{protocol.ToString()}/{hostPort.Replace(":", "")}";
            // The rest is stubbed
        }
    }
    public interface IClient
    {
        bool CheckExists(string path);
        void Delete(string path);
        void Create(string path, byte[] data);
    }
}