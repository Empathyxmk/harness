package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Mocks and dummies for public XiaoMi test
type DummyApplicationPublic struct{}
type DummyNotificationPublic struct {
	ExtraNotification *TestExtraNotificationPublic
}
type TestExtraNotificationPublic struct {
	messageCount int
}

func (e *TestExtraNotificationPublic) SetMessageCount(count int) {
	e.messageCount = count
}

func (e *TestExtraNotificationPublic) GetMessageCount() int {
	return e.messageCount
}

// XiaoMiModelImpl dummy for public test
type XiaoMiModelImplPublic struct{}

func (x *XiaoMiModelImplPublic) SetIconBadgeNum(app *DummyApplicationPublic, notification *DummyNotificationPublic, count int) (*DummyNotificationPublic, error) {
	if notification == nil {
		return nil, errors.New("Xiaomi phones must send notification")
	}
	if notification.ExtraNotification == nil {
		notification.ExtraNotification = &TestExtraNotificationPublic{}
	}
	notification.ExtraNotification.SetMessageCount(count)
	return notification, nil
}

func TestXiaoMiModelImplPublic_SetIconBadgeNum_NullNotification(t *testing.T) {
	model := &XiaoMiModelImplPublic{}
	app := &DummyApplicationPublic{}
	_, err := model.SetIconBadgeNum(app, nil, 99)
	assert.Error(t, err)
	assert.Equal(t, "Xiaomi phones must send notification", err.Error())
}

func TestXiaoMiModelImplPublic_SetIconBadgeNum_ValidNotification(t *testing.T) {
	model := &XiaoMiModelImplPublic{}
	app := &DummyApplicationPublic{}
	notif := &DummyNotificationPublic{ExtraNotification: &TestExtraNotificationPublic{}}
	testCount := 12

	result, err := model.SetIconBadgeNum(app, notif, testCount)
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, notif, result)
	assert.Equal(t, testCount, notif.ExtraNotification.GetMessageCount())
}