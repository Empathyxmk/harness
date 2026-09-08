package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type OrderView struct {
	OrderNo string
	Amount  int
}

type OrderViewDAO struct{}

func (dao *OrderViewDAO) FindByOrderNo(orderNo string) OrderView {
	if orderNo == "ORDER-001" {
		return OrderView{OrderNo: "ORDER-001", Amount: 100}
	}
	return OrderView{}
}

func TestOrderViewDAOFindByOrderNo(t *testing.T) {
	dao := &OrderViewDAO{}
	result := dao.FindByOrderNo("ORDER-001")
	assert.Equal(t, "ORDER-001", result.OrderNo)
	assert.Equal(t, 100, result.Amount)
}