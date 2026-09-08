package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type User struct {
	Id string
}
type Order struct {
	OrdererId string
	Status    string
}

type CancelPolicy struct{}

func (c *CancelPolicy) CanCancel(u User, o Order) bool {
	return u.Id == o.OrdererId && o.Status == "ORDERED"
}

func TestOrdererCanCancelOrderedOrder(t *testing.T) {
	user := User{Id: "user1"}
	order := Order{OrdererId: "user1", Status: "ORDERED"}
	policy := &CancelPolicy{}
	assert.True(t, policy.CanCancel(user, order))
}

func TestOrdererCannotCancelShippedOrder(t *testing.T) {
	user := User{Id: "user1"}
	order := Order{OrdererId: "user1", Status: "SHIPPED"}
	policy := &CancelPolicy{}
	assert.False(t, policy.CanCancel(user, order))
}

func TestNotOrdererCannotCancelOrder(t *testing.T) {
	user := User{Id: "user2"}
	order := Order{OrdererId: "user1", Status: "ORDERED"}
	policy := &CancelPolicy{}
	assert.False(t, policy.CanCancel(user, order))
}