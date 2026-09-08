using Unterstein.BinanceTrader;
using Xunit;

namespace OriginalTests
{
    public class BinanceTraderTests
    {
        [Fact]
        public void TestTradeSuccess()
        {
            var client = new TradingClient();
            var trader = new BinanceTrader(client);
            var result = trader.Trade("BTCUSDT", 1.0, 2.0);
            Assert.True(result);
            trader.Shutdown();
            Assert.False(client.IsConnected());
        }

        [Fact]
        public void TestTradeFailureDueToInput()
        {
            var client = new TradingClient();
            var trader = new BinanceTrader(client);
            var result = trader.Trade("BTCUSDT", 0.0, 2.0); // should fail buy due to invalid quantity
            Assert.False(result);
            trader.Shutdown();
        }
    }
}