using Xunit;
using System.Threading;

namespace OriginalTests
{
    public class DefaultThreadFactoryTest
    {
        [Fact]
        public void TestNewThread()
        {
            var factory = new ProjectName.DefaultThreadFactory("test");
            Thread threadRef = null;
            Thread t = factory.NewThread(() => threadRef = Thread.CurrentThread);
            t.Start();
            t.Join();
            Assert.NotNull(threadRef);
            Assert.StartsWith("test-", threadRef.Name);
        }
    }
}