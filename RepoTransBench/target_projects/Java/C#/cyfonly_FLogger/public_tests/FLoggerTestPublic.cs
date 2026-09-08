using Xunit;

namespace cyfonly_FLogger.Tests.Public
{
    public class FLoggerTestPublic
    {
        [Fact]
        public void TestLoggerInfoAndWarnPublic()
        {
            var logger = cyfonly_FLogger.FLogger.GetInstance();
            logger.Info("Public INFO message for FLoggerTestPublic");
            logger.Warn("Public WARN message for FLoggerTestPublic");
        }
    }
}