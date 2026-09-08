package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

// --- Mocks and dummies ---

type DummyApplication struct{}
type DummyNotification struct {
	ExtraNotification *TestExtraNotification
}
type TestExtraNotification struct {
	messageCount int
}

func (e *TestExtraNotification) SetMessageCount(count int) {
	e.messageCount = count
}

func (e *TestExtraNotification) GetMessageCount() int {
	return e.messageCount
}

// XiaoMiModelImpl implementation (dummy for test scaffolding)
type XiaoMiModelImpl struct{}

func (x *XiaoMiModelImpl) SetIconBadgeNum(app *DummyApplication, notification *DummyNotification, count int) (*DummyNotification, error) {
	if notification == nil {
		return nil, errors.New("Xiaomi phones must send notification")
	}
	if notification.ExtraNotification == nil {
		notification.ExtraNotification = &TestExtraNotification{}
	}
	notification.ExtraNotification.SetMessageCount(count)
	return notification, nil
}

// ---- TESTS ----

func TestXiaoMiModelImpl_SetIconBadgeNum_NullNotification(t *testing.T) {
	model := &XiaoMiModelImpl{}
	app := &DummyApplication{}
	_, err := model.SetIconBadgeNum(app, nil, 10)
	assert.Error(t, err)
	assert.Equal(t, "Xiaomi phones must send notification", err.Error())
}

func TestXiaoMiModelImpl_SetIconBadgeNum_ValidNotification(t *testing.T) {
	model := &XiaoMiModelImpl{}
	app := &DummyApplication{}
	notif := &DummyNotification{ExtraNotification: &TestExtraNotification{}}
	testCount := 5

	result, err := model.SetIconBadgeNum(app, notif, testCount)
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, notif, result)
	assert.Equal(t, testCount, notif.ExtraNotification.GetMessageCount())
}