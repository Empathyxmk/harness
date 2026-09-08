using Xunit;
using Moq;
using FastDFSClient;

namespace FastDFSClient.PublicTests
{
    public class TrackerClientPublicTest
    {
        [Fact]
        public void TestConstructorsAndGetErrorCodePublic()
        {
            var groupMock = new Mock<TrackerGroup>();
            var client = new TrackerClient(groupMock.Object);

            Assert.Same(groupMock.Object, client.TrackerGroup);

            var client2 = new TrackerClient();
            Assert.NotNull(client2.TrackerGroup);

            client.errno = 10;
            Assert.Equal(10, client.GetErrorCode());
        }

        [Fact]
        public void TestGetTrackerServerPublic()
        {
            var groupMock = new Mock<TrackerGroup>();
            var serverMock = new Mock<TrackerServer>().Object;
            groupMock.Setup(g => g.GetTrackerServer()).Returns(serverMock);

            var client = new TrackerClient(groupMock.Object);
            var result = client.GetTrackerServer();
            Assert.Same(serverMock, result);
        }

        [Fact]
        public void TestGetConnectionFailoverPublic()
        {
            var groupMock = new Mock<TrackerGroup>();
            var servers = new[] {
                new Mock<TrackerServer>(),
                new Mock<TrackerServer>()
            };
            var connection1 = new Mock<IConnection>().Object;
            groupMock.Setup(g => g.TrackerServers).Returns(new TrackerServer[] { servers[0].Object, servers[1].Object });
            groupMock.Setup(g => g.GetTrackerServer()).Returns(servers[0].Object);
            servers[0].Setup(s => s.GetConnection()).Throws(new System.IO.IOException("fail1"));
            servers[0].Setup(s => s.Index).Returns(0);
            groupMock.Setup(g => g.GetTrackerServer(1)).Returns(servers[1].Object);
            servers[1].Setup(s => s.GetConnection()).Returns(connection1);

            var client = new TrackerClient(groupMock.Object);
            var result = client.GetConnection(null);
            Assert.Same(connection1, result);
        }
    }
}