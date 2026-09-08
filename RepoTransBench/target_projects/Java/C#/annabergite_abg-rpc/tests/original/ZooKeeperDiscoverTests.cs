using System;
using System.Collections.Generic;
using Xunit;
using Moq;

namespace AnnabergiteAbgRpc.Tests.Original
{
    public class ZooKeeperDiscoverTests
    {
        [Fact]
        public void TestInitAndAddListenerNullCheck()
        {
            var discover = new Mock<IZooKeeperDiscover>();
            var hps = new List<string> { "localhost:2181" };
            discover.Setup(d => d.Init(hps));

            discover.Object.Init(hps);
            Assert.NotNull(discover.Object);

            var protocol = new Mock<IProtocol>();

            // Listener is null -> should throw
            Assert.Throws<ArgumentNullException>(() =>
                discover.Object.AddListener("grp", "app", protocol.Object, null)
            );
        }

        [Fact]
        public void TestAddListenerNoInit()
        {
            var discover = new Mock<IZooKeeperDiscover>();
            var protocol = new Mock<IProtocol>();
            var listener = new Mock<IDiscoverListener>();
            // Not calling .Init(), assume it throws as per real logic
            Assert.Throws<NullReferenceException>(() =>
                discover.Object.AddListener("grp", "app", protocol.Object, listener.Object)
            );
        }
    }

    // Stubs for test dependencies (reuse from previous test file)
    public interface IZooKeeperDiscover
    {
        void Init(List<string> hosts);
        void AddListener(string group, string app, IProtocol protocol, IDiscoverListener listener);
    }
    public interface IProtocol { string ToString(); }
    public interface IDiscoverListener { void OnChange(string path); }
}