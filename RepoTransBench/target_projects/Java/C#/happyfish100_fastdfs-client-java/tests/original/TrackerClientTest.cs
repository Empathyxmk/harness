using Xunit;
using Moq;
using FastDFSClient;

namespace FastDFSClient.Tests
{
    public class TrackerClientTest
    {
        [Fact]
        public void TestConstructorsAndGetErrorCode()
        {
            var group = new Mock<TrackerGroup>().Object;
            var client = new TrackerClient(group);
            Assert.Same(group, client.TrackerGroup);

            var defaultClient = new TrackerClient();
            var _ = defaultClient.GetErrorCode(); // Just ensure no exception etc.
        }

        [Fact]
        public void TestGetTrackerServer()
        {
            var groupMock = new Mock<TrackerGroup>();
            var serverMock = new Mock<TrackerServer>().Object;
            groupMock.Setup(g => g.GetTrackerServer()).Returns(serverMock);

            var client = new TrackerClient(groupMock.Object);
            Assert.Same(serverMock, client.GetTrackerServer());
        }

        [Fact]
        public void TestGetConnectionSuccess()
        {
            var groupMock = new Mock<TrackerGroup>();
            var serverMock = new Mock<TrackerServer>();
            var connMock = new Mock<IConnection>().Object;

            serverMock.Setup(s => s.GetConnection()).Returns(connMock);
            groupMock.Setup(g => g.TrackerServers).Returns(new TrackerServer[] { serverMock.Object });

            var client = new TrackerClient(groupMock.Object);
            Assert.Same(connMock, client.GetConnection(serverMock.Object));
        }

        [Fact]
        public void TestGetConnectionWithFailover()
        {
            var groupMock = new Mock<TrackerGroup>();
            var server1Mock = new Mock<TrackerServer>();
            var server2Mock = new Mock<TrackerServer>();
            var conn2 = new Mock<IConnection>().Object;
            server1Mock.Setup(s => s.GetConnection()).Throws(new System.IO.IOException("fail!"));
            server1Mock.Setup(s => s.Index).Returns(0);

            groupMock.Setup(g => g.TrackerServers).Returns(new TrackerServer[] { server1Mock.Object, server2Mock.Object });
            groupMock.Setup(g => g.GetTrackerServer()).Returns(server1Mock.Object);
            groupMock.Setup(g => g.GetTrackerServer(1)).Returns(server2Mock.Object);

            server2Mock.Setup(s => s.GetConnection()).Returns(conn2);

            var client = new TrackerClient(groupMock.Object);
            var conn = client.GetConnection(null);
            Assert.Same(conn2, conn);
        }
    }
}