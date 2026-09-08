using Xunit;

namespace NettyImServer.PublicTests
{
    public class ImServerPublicTests
    {
        [Fact]
        public void TestImServerConstructorPublic()
        {
            // More coverage: check class name after instantiation
            var server = new NettyImServer.Core.ImServer();
            Assert.Equal("ImServer", server.GetType().Name);
        }
    }
}