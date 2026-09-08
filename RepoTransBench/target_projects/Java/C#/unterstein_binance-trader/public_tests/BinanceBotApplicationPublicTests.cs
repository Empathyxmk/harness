using System;
using Unterstein.BinanceTrader;
using Xunit;

namespace PublicTests
{
    public class BinanceBotApplicationPublicTests
    {
        [Fact]
        public void TestMainRunsWithArgs()
        {
            // Use some dummy command-line args
            BinanceBotApplication.Main(new[] { "--simulate", "--config=test.properties" });
        }
    }
}