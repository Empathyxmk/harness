using Unterstein.BinanceTrader;
using Xunit;

namespace OriginalTests
{
    public class TradingClientTests
    {
        [Fact]
        public void TestConnectionLogic()
        {
            var client = new TradingClient();
            Assert.False(client.IsConnected());
            client.Connect();
            Assert.True(client.IsConnected());
            client.Disconnect();
            Assert.False(client.IsConnected());
        }

        [Fact]
        public void TestBuySellSuccess()
        {
            var client = new TradingClient();
            client.Connect();
            Assert.Equal(1, client.Buy("BTCUSDT", 0.002));
            Assert.Equal(1, client.Sell("BTCUSDT", 0.002));
        }

        [Fact]
        public void TestBuySellFailWhenNotConnected()
        {
            var client = new TradingClient();
            Assert.Equal(-1, client.Buy("BTCUSDT", 0.002));
            Assert.Equal(-1, client.Sell("BTCUSDT", 0.002));
        }

        [Fact]
        public void TestBuySellInvalidInput()
        {
            var client = new TradingClient();
            client.Connect();
            Assert.Equal(-1, client.Buy(null, 0.002));
            Assert.Equal(-1, client.Buy("BTCUSDT", 0));
            Assert.Equal(-1, client.Sell(null, 0.002));
            Assert.Equal(-1, client.Sell("BTCUSDT", -42));
        }
    }
}