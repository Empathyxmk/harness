using System.Threading.Tasks;
using Xunit;

namespace OriginalTests
{
    public class StandardThreadExecutorTest
    {
        [Fact]
        public async Task TestExecuteAndShutdown()
        {
            var executor = new ProjectName.StandardThreadExecutor(1, 2, 1000);
            var future = executor.Submit(() => "executed");
            Assert.Equal("executed", await future);
            executor.Shutdown();
            Assert.True(executor.IsShutdown || executor.IsTerminated);
        }
    }
}