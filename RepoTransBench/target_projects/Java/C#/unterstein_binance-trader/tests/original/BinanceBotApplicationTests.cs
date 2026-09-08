using System;
using Unterstein.BinanceTrader;
using Xunit;

namespace OriginalTests
{
    public class BinanceBotApplicationTests
    {
        [Fact]
        public void TestMainRuns()
        {
            BinanceBotApplication.Main(Array.Empty<string>());
        }
    }
}