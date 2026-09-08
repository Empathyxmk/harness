using Xunit;

namespace cyfonly_FLogger.Tests.Public
{
    public class FloggerThroughputPublicTest
    {
        [Fact]
        public void PublicThroughputDifferentLoop()
        {
            var logger = cyfonly_FLogger.FLogger.GetInstance();
            int cnt = 10;
            for (int i = 0; i < cnt; i++)
            {
                logger.Info("Public throughput message #" + i);
            }
        }
    }
}