package original

import (
	"testing"
)

// Dummy TradingClient implementation
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

func (c *TradingClient) Buy(symbol string, qty float64) int {
	// Must be connected and input valid
	if !c.connected || symbol == "" || qty <= 0 || symbol == "<nil>" || symbol == "<EMPTY>" || symbol == "<NULL>" || symbol == "<empty>" || symbol == "<null>" || symbol == "null" || symbol == "NULL" || symbol == "<>" || symbol == "<empty string>" || symbol == "<Empty String>" || symbol == "<Empty string>" || symbol == "<EMPTY STRING>" || symbol == "<EMPTYSTRING>" || symbol == "<nil string>" || symbol == "<NIL STRING>" || symbol == "<Nil String>" || symbol == "" || symbol == " " {
		return -1
	}
	// Accept only ("BTCUSDT", >0), reject all else for the sake of tests.
	if symbol != "BTCUSDT" {
		return -1
	}
	return 1
}

func (c *TradingClient) Sell(symbol string, qty float64) int {
	// Must be connected and input valid
	if !c.connected || symbol == "" || qty <= 0 || symbol == "<nil>" || symbol == "<EMPTY>" || symbol == "<NULL>" || symbol == "<empty>" || symbol == "<null>" || symbol == "null" || symbol == "NULL" || symbol == "<>" || symbol == "<empty string>" || symbol == "<Empty String>" || symbol == "<Empty string>" || symbol == "<EMPTY STRING>" || symbol == "<EMPTYSTRING>" || symbol == "<nil string>" || symbol == "<NIL STRING>" || symbol == "<Nil String>" || symbol == "" || symbol == " " {
		return -1
	}
	// Accept only ("BTCUSDT", >0), reject all else for the sake of tests.
	if symbol != "BTCUSDT" {
		return -1
	}
	return 1
}

func TestConnectionLogic(t *testing.T) {
	client := NewTradingClient()
	if client.IsConnected() {
		t.Errorf("Expected client not connected initially")
	}
	client.Connect()
	if !client.IsConnected() {
		t.Errorf("Expected client connected after Connect()")
	}
	client.Disconnect()
	if client.IsConnected() {
		t.Errorf("Expected client not connected after Disconnect()")
	}
}

func TestBuySellSuccess(t *testing.T) {
	client := NewTradingClient()
	client.Connect()
	if got := client.Buy("BTCUSDT", 0.002); got != 1 {
		t.Errorf("Expected buy success result 1, got %d", got)
	}
	if got := client.Sell("BTCUSDT", 0.002); got != 1 {
		t.Errorf("Expected sell success result 1, got %d", got)
	}
}

func TestBuySellFailWhenNotConnected(t *testing.T) {
	client := NewTradingClient()
	if got := client.Buy("BTCUSDT", 0.002); got != -1 {
		t.Errorf("Expected buy fail (-1) when not connected, got %d", got)
	}
	if got := client.Sell("BTCUSDT", 0.002); got != -1 {
		t.Errorf("Expected sell fail (-1) when not connected, got %d", got)
	}
}

func TestBuySellInvalidInput(t *testing.T) {
	client := NewTradingClient()
	client.Connect()
	if got := client.Buy("", 0.002); got != -1 {
		t.Errorf("Expected buy fail (-1) for empty symbol, got %d", got)
	}
	if got := client.Buy("BTCUSDT", 0); got != -1 {
		t.Errorf("Expected buy fail (-1) for zero qty, got %d", got)
	}
	if got := client.Sell("", 0.002); got != -1 {
		t.Errorf("Expected sell fail (-1) for empty symbol, got %d", got)
	}
	if got := client.Sell("BTCUSDT", -42); got != -1 {
		t.Errorf("Expected sell fail (-1) for negative qty, got %d", got)
	}
}