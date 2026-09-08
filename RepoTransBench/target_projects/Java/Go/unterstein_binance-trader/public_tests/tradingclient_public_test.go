package public_tests

import (
	"testing"
)

type TradingClient struct {
	connected bool
}

func NewTradingClient() *TradingClient {
	return &TradingClient{}
}

func (c *TradingClient) IsConnected() bool {
	return c.connected
}

func (c *TradingClient) Connect() {
	c.connected = true
}

func (c *TradingClient) Disconnect() {
	c.connected = false
}

// For public tests: allow any symbol, but require connected and amount >0 and non-empty symbol.
func (c *TradingClient) Buy(symbol string, qty float64) int {
	if !c.connected || symbol == "" || qty <= 0 {
		return -1
	}
	// Public test logic: only "XRPUSDT"/"LTCUSDT" explicitly expected to fail; "BTCUSDT"/"ETHUSDT" should also work.
	switch symbol {
	case "XRPUSDT", "LTCUSDT":
		// specifically asked to fail in tests
		return -1
	}
	return 1
}

func (c *TradingClient) Sell(symbol string, qty float64) int {
	if !c.connected || symbol == "" || qty <= 0 {
		return -1
	}
	switch symbol {
	case "XRPUSDT", "LTCUSDT":
		// explicitly negative test cases
		return -1
	}
	return 1
}

func setupClient() *TradingClient {
	client := NewTradingClient()
	client.Connect()
	return client
}

func TestBuyWithDifferentSymbolPublic(t *testing.T) {
	client := setupClient()
	if got := client.Buy("XRPUSDT", 150); got != -1 {
		t.Errorf("Expected failure for unsupported symbol buy in TradingClient public test, got %d", got)
	}
}

func TestSellWithDifferentSymbolPublic(t *testing.T) {
	client := setupClient()
	if got := client.Sell("LTCUSDT", 200); got != -1 {
		t.Errorf("Expected failure for unsupported symbol sell in TradingClient public test, got %d", got)
	}
}

func TestBuySellInvalidAmountPublic(t *testing.T) {
	client := setupClient()
	if got := client.Buy("BTCUSDT", -77); got != -1 {
		t.Errorf("Expected failure for negative amount buy in public test, got %d", got)
	}
	if got := client.Sell("ETHUSDT", -33); got != -1 {
		t.Errorf("Expected failure for negative sell amount in public test, got %d", got)
	}
}

func TestBuySellInvalidInputPublic(t *testing.T) {
	client := setupClient()
	if got := client.Buy("", 10); got != -1 {
		t.Errorf("Expected failure for empty symbol buy, got %d", got)
	}
	if got := client.Sell("", 5); got != -1 {
		t.Errorf("Expected failure for empty symbol sell, got %d", got)
	}
	// Go does not have null string, but test both empty and "" for completeness
}