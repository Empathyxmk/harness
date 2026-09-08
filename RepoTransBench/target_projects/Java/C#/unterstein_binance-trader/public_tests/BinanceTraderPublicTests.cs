using Unterstein.BinanceTrader;
using Xunit;

namespace PublicTests
{
    public class BinanceTraderPublicTests
    {
        [Fact]
        public void TestTradeSuccessPublic()
        {
            var client = new TradingClient();
            var trader = new BinanceTrader(client);
            var result = trader.Trade("ETHUSDT", 3.0, 1.0); // Different symbol, different quantities
            Assert.True(result);
            trader.Shutdown();
            Assert.False(client.IsConnected());
        }

        [Fact]
        public void TestTradeFailureDueToInputPublic()
        {
            var client = new TradingClient();
            var trader = new BinanceTrader(client);
            // Should fail buy due to null symbol
            var result = trader.Trade(null, 2.0, 1.5);
            Assert.False(result);
            trader.Shutdown();
        }
    }
}