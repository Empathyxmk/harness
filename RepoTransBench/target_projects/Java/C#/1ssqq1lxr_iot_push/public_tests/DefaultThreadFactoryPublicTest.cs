using Xunit;
using System.Threading;

namespace PublicTests
{
    public class DefaultThreadFactoryPublicTest
    {
        [Fact]
        public void TestNewThreadPublic()
        {
            var factory = new ProjectName.DefaultThreadFactory("public-thread");
            Thread threadRef = null;
            Thread t = factory.NewThread(() => threadRef = Thread.CurrentThread);
            t.Start();
            t.Join();
            Assert.NotNull(threadRef);
            Assert.Contains("public-thread", threadRef.Name);
        }
    }
}