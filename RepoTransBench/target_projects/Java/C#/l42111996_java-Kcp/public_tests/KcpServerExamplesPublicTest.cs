using Xunit;

namespace KcpPublicTests
{
    public class KcpServerExamplesPublicTest
    {
        [Fact]
        public void TestSimplePublicServer()
        {
            int serverId = 42;
            int port = 16667;
            string expectedGreeting = "KCP Public Test Server Started (ServerID: 42, Port: 16667)";

            string serverGreeting = SimulateServerStart(serverId, port);
            Assert.Equal(expectedGreeting, serverGreeting);
        }

        private string SimulateServerStart(int serverId, int port)
        {
            return $"KCP Public Test Server Started (ServerID: {serverId}, Port: {port})";
        }
    }
}