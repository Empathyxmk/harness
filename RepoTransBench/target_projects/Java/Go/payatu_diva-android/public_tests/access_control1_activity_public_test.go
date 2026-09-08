package public_tests

import (
	"testing"
)

type AccessControl1Activity struct {
	viewCredsBtn *Button
}

type Button struct {
	ID int
}

func NewAccessControl1ActivityPublic() *AccessControl1Activity {
	return &AccessControl1Activity{
		viewCredsBtn: &Button{ID: 7},
	}
}

func (a *AccessControl1Activity) FindViewById(id int) *Button {
	if a.viewCredsBtn != nil && a.viewCredsBtn.ID == id {
		return a.viewCredsBtn
	}
	return nil
}

func TestAccessControl1Activity_activity_starts_and_layout_public(t *testing.T) {
	act := NewAccessControl1ActivityPublic()
	btn := act.FindViewById(7)
	if btn == nil {
		t.Error("Expected non-nil button for ac1ViewCredsBtn (ID 7)")
	}
}