using Unterstein.BinanceTrader;
using Xunit;

namespace PublicTests
{
    public class TradingClientPublicTests
    {
        private TradingClient client;

        public TradingClientPublicTests()
        {
            client = new TradingClient();
            client.Connect();
        }

        [Fact]
        public void TestBuyWithDifferentSymbolPublic()
        {
            // Use a symbol that is NOT supported by dummy impl; expect failure!
            int result = client.Buy("XRPUSDT", 150);
            Assert.Equal(-1, result);
        }

        [Fact]
        public void TestSellWithDifferentSymbolPublic()
        {
            // Use a symbol that is NOT supported by dummy impl; expect failure!
            int result = client.Sell("LTCUSDT", 200);
            Assert.Equal(-1, result);
        }

        [Fact]
        public void TestBuySellInvalidAmountPublic()
        {
            // Use a different invalid negative amount
            int resultBuy = client.Buy("BTCUSDT", -77);
            Assert.Equal(-1, resultBuy);

            int resultSell = client.Sell("ETHUSDT", -33);
            Assert.Equal(-1, resultSell);
        }

        [Fact]
        public void TestBuySellInvalidInputPublic()
        {
            // Use null and empty string, should still fail
            int resultBuyNull = client.Buy(null, 10);
            Assert.Equal(-1, resultBuyNull);

            int resultBuyEmpty = client.Buy(string.Empty, 10);
            Assert.Equal(-1, resultBuyEmpty);

            int resultSellNull = client.Sell(null, 5);
            Assert.Equal(-1, resultSellNull);

            int resultSellEmpty = client.Sell(string.Empty, 5);
            Assert.Equal(-1, resultSellEmpty);
        }
    }
}