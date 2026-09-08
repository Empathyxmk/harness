package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type OrderSummary struct {
	OrderNo string
	Count   int
}

type OrderSummaryDAO struct{}

func (dao *OrderSummaryDAO) ListByOrdererId(ordererId string) []OrderSummary {
	if ordererId == "user1" {
		return []OrderSummary{
			{OrderNo: "ORDER-001", Count: 2},
			{OrderNo: "ORDER-002", Count: 1},
		}
	}
	return nil
}

func TestOrderSummaryDAOListByOrdererId(t *testing.T) {
	dao := &OrderSummaryDAO{}
	list := dao.ListByOrdererId("user1")
	assert.Len(t, list, 2)
	assert.Equal(t, "ORDER-001", list[0].OrderNo)
	assert.Equal(t, 2, list[0].Count)
}