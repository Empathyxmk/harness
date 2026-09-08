using Xunit;

namespace cyfonly_FLogger.Tests.Public
{
    public class FLoggerCorePublicTest
    {
        [Fact]
        public void TestVariousLevelsPublic()
        {
            var logger = cyfonly_FLogger.FLogger.GetInstance();
            // Use different messages and levels compared to original, including more threads
            logger.Debug("Debugging - public core test!");
            logger.Fatal("This is a public fatal log!");
            logger.WriteLog("public_logfile", 2, "This is a public WARN log in a special file!");
        }
    }
}