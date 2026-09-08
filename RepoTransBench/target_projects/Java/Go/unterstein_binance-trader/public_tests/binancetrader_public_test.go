package public_tests

import (
	"testing"
)

type BinanceTrader struct {
	client *TradingClient
}

func NewBinanceTrader(client *TradingClient) *BinanceTrader {
	return &BinanceTrader{client: client}
}

func (b *BinanceTrader) Trade(symbol string, buyQty float64, sellQty float64) bool {
	b.client.Connect()
	if b.client.Buy(symbol, buyQty) != 1 {
		return false
	}
	if b.client.Sell(symbol, sellQty) != 1 {
		return false
	}
	return true
}

func (b *BinanceTrader) Shutdown() {
	b.client.Disconnect()
}

func TestTradeSuccessPublic(t *testing.T) {
	client := NewTradingClient()
	trader := NewBinanceTrader(client)
	result := trader.Trade("ETHUSDT", 3.0, 1.0)
	if !result {
		t.Errorf("Expected trade to succeed with symbol ETHUSDT and quantities 3.0 & 1.0")
	}
	trader.Shutdown()
	if client.IsConnected() {
		t.Errorf("Client should be disconnected after trader shutdown")
	}
}

func TestTradeFailureDueToInputPublic(t *testing.T) {
	client := NewTradingClient()
	trader := NewBinanceTrader(client)
	result := trader.Trade("", 2.0, 1.5)
	if result {
		t.Errorf("Expected trade to fail for empty symbol")
	}
	trader.Shutdown()
}