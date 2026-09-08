package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyApplicationVivoPublic struct{}
type DummyNotificationVivoPublic struct{}

type VIVOModelImplPublic struct{}

func (v *VIVOModelImplPublic) SetIconBadgeNum(app *DummyApplicationVivoPublic, notification *DummyNotificationVivoPublic, count int) error {
	return errors.New("not support : vivo")
}

func TestVIVOModelImplPublic_SetIconBadgeNum_AlwaysThrowsException(t *testing.T) {
	model := &VIVOModelImplPublic{}
	app := &DummyApplicationVivoPublic{}
	notif := &DummyNotificationVivoPublic{}
	err := model.SetIconBadgeNum(app, notif, 17)
	assert.Error(t, err)
	assert.Equal(t, "not support : vivo", err.Error())
}