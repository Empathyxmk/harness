package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyApplicationVivo struct{}
type DummyNotificationVivo struct{}

type VIVOModelImpl struct{}

func (v *VIVOModelImpl) SetIconBadgeNum(app *DummyApplicationVivo, notification *DummyNotificationVivo, count int) error {
	return errors.New("not support : vivo")
}

func TestVIVOModelImpl_SetIconBadgeNum_AlwaysThrowsException(t *testing.T) {
	model := &VIVOModelImpl{}
	app := &DummyApplicationVivo{}
	notif := &DummyNotificationVivo{}
	err := model.SetIconBadgeNum(app, notif, 10)
	assert.Error(t, err)
	assert.Equal(t, "not support : vivo", err.Error())
}