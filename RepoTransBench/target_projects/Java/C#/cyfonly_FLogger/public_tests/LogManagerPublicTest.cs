using Xunit;

namespace cyfonly_FLogger.Tests.Public
{
    public class LogManagerPublicTest
    {
        [Fact]
        public void TestSingletonAndClosePublic()
        {
            var logManager1 = cyfonly_FLogger.strategy.LogManager.GetInstance();
            var logManager2 = cyfonly_FLogger.strategy.LogManager.GetInstance();
            Assert.Same(logManager1, logManager2);

            // Just call close to make sure no exception (cannot assert file contents)
            logManager1.Close();
            // No assertion needed, just ensuring no exception thrown
        }
    }
}