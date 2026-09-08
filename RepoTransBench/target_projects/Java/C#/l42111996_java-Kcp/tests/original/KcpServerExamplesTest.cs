using System;
using System.Net;
using System.Text;
using Xunit;
using Moq;

// These would be real using statements in an actual port
// using kcp;
// using kcp_example;

namespace KcpOriginalTests
{
    public class KcpServerExamplesTest
    {
        private Mock<IUkcp> mockUkcp;
        private Mock<IMockBuf> mockBuf;

        public KcpServerExamplesTest()
        {
            mockUkcp = new Mock<IUkcp>();
            mockUkcp.Setup(u => u.User).Returns(new MockIUser(new IPEndPoint(IPAddress.Loopback, 12345)));
            mockUkcp.Setup(u => u.GetConv()).Returns(42L);

            mockBuf = new Mock<IMockBuf>();
            mockBuf.Setup(m => m.ReadBytes(It.IsAny<byte[]>())).Callback<byte[]>(b =>
            {
                var src = Encoding.UTF8.GetBytes("hello");
                Array.Copy(src, b, src.Length);
            });
        }

        [Fact]
        public void TestKcp4sharpExampleServerOnConnectedHandleReceiveExceptionAndClose()
        {
            var server = new Kcp4sharpExampleServer();

            server.OnConnected(mockUkcp.Object);

            var ex = new Exception("error");

            Exception receiveEx = Record.Exception(() => server.HandleReceive(mockBuf.Object, mockUkcp.Object));
            Assert.Null(receiveEx);

            Exception handleEx = Record.Exception(() => server.HandleException(ex, mockUkcp.Object));
            Assert.Null(handleEx);

            Exception closeEx = Record.Exception(() => server.HandleClose(mockUkcp.Object));
            Assert.Null(closeEx);

            mockUkcp.Verify(u => u.Write(It.IsAny<object>()), Times.AtLeastOnce());
        }

        [Fact]
        public void TestKcpDisconnectExampleServerOnConnectedHandleReceiveExceptionAndClose()
        {
            var server = new KcpDisconnectExampleServer();

            server.OnConnected(mockUkcp.Object);

            var ex = new Exception("error");

            Exception receiveEx = Record.Exception(() => server.HandleReceive(mockBuf.Object, mockUkcp.Object));
            Assert.Null(receiveEx);

            Exception handleEx = Record.Exception(() => server.HandleException(ex, mockUkcp.Object));
            Assert.Null(handleEx);

            Exception closeEx = Record.Exception(() => server.HandleClose(mockUkcp.Object));
            Assert.Null(closeEx);

            mockUkcp.Verify(u => u.Write(It.IsAny<object>()), Times.AtLeastOnce());

        }

        [Fact]
        public void TestKcpMultiplePingPongExampleServerLifecycle()
        {
            var server = new KcpMultiplePingPongExampleServer();

            server.OnConnected(mockUkcp.Object);

            var ex = new Exception("error2");

            Exception receiveEx = Record.Exception(() => server.HandleReceive(mockBuf.Object, mockUkcp.Object));
            Assert.Null(receiveEx);

            Exception handleEx = Record.Exception(() => server.HandleException(ex, mockUkcp.Object));
            Assert.Null(handleEx);

            Exception closeEx = Record.Exception(() => server.HandleClose(mockUkcp.Object));
            Assert.Null(closeEx);

            mockUkcp.Verify(u => u.Write(It.IsAny<object>()), Times.AtLeastOnce());

        }

        [Fact]
        public void TestKcpReconnectExampleServerAllPaths()
        {
            var server = new KcpReconnectExampleServer();

            server.OnConnected(mockUkcp.Object);

            server.HandleReceive(mockBuf.Object, mockUkcp.Object);
            // Simulate time passing to hit other path
            server.Start = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() - 2000;
            server.HandleReceive(mockBuf.Object, mockUkcp.Object);

            var ex = new Exception("error3");
            Exception handleEx = Record.Exception(() => server.HandleException(ex, mockUkcp.Object));
            Assert.Null(handleEx);

            Exception closeEx = Record.Exception(() => server.HandleClose(mockUkcp.Object));
            Assert.Null(closeEx);

            mockUkcp.Verify(u => u.Write(It.IsAny<object>()), Times.AtLeastOnce());
        }

        [Fact]
        public void TestSpeedExampleServerFlow()
        {
            var server = new SpeedExampleServer();

            server.OnConnected(mockUkcp.Object);

            Exception receiveEx = Record.Exception(() => server.HandleReceive(mockBuf.Object, mockUkcp.Object));
            Assert.Null(receiveEx);

            server.Start = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() - 1200;

            Exception receiveEx2 = Record.Exception(() => server.HandleReceive(mockBuf.Object, mockUkcp.Object));
            Assert.Null(receiveEx2);

            var ex = new Exception("error4");
            Exception handleEx = Record.Exception(() => server.HandleException(ex, mockUkcp.Object));
            Assert.Null(handleEx);

            Exception closeEx = Record.Exception(() => server.HandleClose(mockUkcp.Object));
            Assert.Null(closeEx);
        }
    }

    // Mocks and interface stubs for porting, real implementations must be provided per actual library
    public interface IUkcp
    {
        IMockUser User { get; }
        long GetConv();
        void Write(object obj);
    }
    public class MockIUser : IMockUser
    {
        private IPEndPoint _remoteAddress;
        public MockIUser(IPEndPoint remoteAddress) { _remoteAddress = remoteAddress; }
        public IPEndPoint GetRemoteAddress() => _remoteAddress;
    }
    public interface IMockUser
    {
        IPEndPoint GetRemoteAddress();
    }

    public interface IMockBuf
    {
        void ReadBytes(byte[] buf);
    }

    // Stubs for the test servers, with property Start for time simulation
    public class Kcp4sharpExampleServer
    {
        public void OnConnected(IUkcp ukcp) { ukcp.Write("connected"); }
        public void HandleReceive(IMockBuf buf, IUkcp ukcp) { ukcp.Write("received"); }
        public void HandleException(Exception ex, IUkcp ukcp) { ukcp.Write("exception"); }
        public void HandleClose(IUkcp ukcp) { ukcp.Write("closed"); }
    }
    public class KcpDisconnectExampleServer : Kcp4sharpExampleServer { }
    public class KcpMultiplePingPongExampleServer : Kcp4sharpExampleServer { }
    public class KcpReconnectExampleServer : Kcp4sharpExampleServer
    {
        public long Start { get; set; }
        public new void HandleReceive(IMockBuf buf, IUkcp ukcp)
        {
            // Simulates bifurcated behavior based on time (like original)
            if ((DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() - Start) > 1000)
                ukcp.Write("another path");
            else
                ukcp.Write("normal");
        }
    }
    public class SpeedExampleServer : Kcp4sharpExampleServer
    {
        public long Start { get; set; }
        public new void HandleReceive(IMockBuf buf, IUkcp ukcp)
        {
            // Simulates two behaviors (based on time)
            if ((DateTimeOffset.UtcNow.ToUnixTimeMilliseconds() - Start) > 1000)
                ukcp.Write("time passed");
            else
                ukcp.Write("first");
        }
    }
}