package original

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
	// Try to buy, then (if success) try to sell. Return true if both succeed.
	// Must be connected for buying and selling.
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

func TestTradeSuccess(t *testing.T) {
	client := NewTradingClient()
	trader := NewBinanceTrader(client)
	result := trader.Trade("BTCUSDT", 1.0, 2.0)
	if !result {
		t.Errorf("Expected trade to succeed")
	}
	trader.Shutdown()
	if client.IsConnected() {
		t.Errorf("Client should be disconnected after trader shutdown")
	}
}

func TestTradeFailureDueToInput(t *testing.T) {
	client := NewTradingClient()
	trader := NewBinanceTrader(client)
	// Should fail buy due to invalid quantity
	result := trader.Trade("BTCUSDT", 0.0, 2.0)
	if result {
		t.Errorf("Expected trade to fail on 0 quantity")
	}
	trader.Shutdown()
}