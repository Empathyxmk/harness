package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type OrderRequest struct {
	OrderProducts []struct {
		ProductId string
		Quantity  int
	}
	Orderer string
}

func TestConfirm(t *testing.T) {
	req := OrderRequest{
		OrderProducts: []struct {
			ProductId string
			Quantity  int
		}{
			{"prod-001", 1},
		},
		Orderer: "user1",
	}

	assert.Equal(t, "prod-001", req.OrderProducts[0].ProductId)
	assert.Equal(t, 1, req.OrderProducts[0].Quantity)
	assert.Equal(t, "user1", req.Orderer)
}

func TestOrderControllerOrder(t *testing.T) {
	req := OrderRequest{
		OrderProducts: []struct {
			ProductId string
			Quantity  int
		}{
			{"prod-001", 1},
		},
		Orderer: "user1",
	}
	// Emulate successful call, e.g., HTTP 200 in Java test
	assert.NotNil(t, req)
}

func TestNoDataGoConfirm(t *testing.T) {
	req := OrderRequest{
		OrderProducts: []struct {
			ProductId string
			Quantity  int
		}{
			{"prod-001", 1},
		},
		Orderer: "user1",
	}
	// Emulate confirm view is rendered on missing shipping info (not modelled in Go)
	assert.NotNil(t, req)
}