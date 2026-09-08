package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type BlockMemberService struct {
	membersBlocked map[string]bool
}

func (b *BlockMemberService) block(user string, role string) error {
	if role != "ROLE_ADMIN" {
		return errors.New("AccessDeniedException")
	}
	b.membersBlocked[user] = true
	return nil
}

func TestNoAdminCantBlockMember(t *testing.T) {
	bms := &BlockMemberService{membersBlocked: make(map[string]bool)}
	err := bms.block("user1", "ROLE_USER")
	assert.Error(t, err)
	assert.Equal(t, "AccessDeniedException", err.Error())
}

func TestAdminCanBlockMember(t *testing.T) {
	bms := &BlockMemberService{membersBlocked: make(map[string]bool)}
	err := bms.block("user1", "ROLE_ADMIN")
	assert.NoError(t, err)
}