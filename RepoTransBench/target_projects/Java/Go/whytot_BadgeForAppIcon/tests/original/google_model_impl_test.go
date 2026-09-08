package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// --- Support structs and dummy mocks for GoogleModelImpl ---

type DummyIntent struct {
	action    string
	extras    map[string]interface{}
}

func NewDummyIntent(action string) *DummyIntent {
	return &DummyIntent{action: action, extras: make(map[string]interface{})}
}
func (d *DummyIntent) SetExtra(key string, val interface{}) {
	d.extras[key] = val
}
func (d *DummyIntent) GetAction() string { return d.action }
func (d *DummyIntent) GetIntExtra(key string, def int) int {
	v, ok := d.extras[key]
	if !ok {
		return def
	}
	i, ok := v.(int)
	if !ok {
		return def
	}
	return i
}
func (d *DummyIntent) GetStringExtra(key string, def string) string {
	v, ok := d.extras[key]
	if !ok {
		return def
	}
	s, ok := v.(string)
	if !ok {
		return def
	}
	return s
}

type DummyApplicationGoogle struct {
	mock.Mock
	PackageName string
}

func (a *DummyApplicationGoogle) SendBroadcast(intent *DummyIntent) {
	a.Called(intent)
}
func (a *DummyApplicationGoogle) GetPackageName() string {
	return a.PackageName
}

type DummyUtilsGoogle struct {
	mock.Mock
}
func (u *DummyUtilsGoogle) GetLaunchIntentForPackage(app *DummyApplicationGoogle) string {
	args := u.Called(app)
	return args.String(0)
}
func (u *DummyUtilsGoogle) CanResolveBroadcast(app *DummyApplicationGoogle, intent *DummyIntent) bool {
	args := u.Called(app, intent)
	return args.Bool(0)
}

type GoogleModelImpl struct {
	Utils *DummyUtilsGoogle
}

var sdkIntForTest = 0

func setSdkIntForTest(val int) {
	sdkIntForTest = val
}

// For test, mimic the logic for API >=26 (O)
func (g *GoogleModelImpl) SetIconBadgeNum(app *DummyApplicationGoogle, notif interface{}, count int) error {
	if sdkIntForTest < 26 {
		return errors.New("google not support before API O")
	}
	intent := NewDummyIntent("android.intent.action.BADGE_COUNT_UPDATE")
	intent.SetExtra("badge_count", count)
	intent.SetExtra("badge_count_package_name", app.GetPackageName())
	intent.SetExtra("badge_count_class_name", g.Utils.GetLaunchIntentForPackage(app))
	app.SendBroadcast(intent)
	return nil
}

func TestGoogleModelImpl_SetIconBadgeNum_SdkBelowO(t *testing.T) {
	setSdkIntForTest(25)
	app := &DummyApplicationGoogle{PackageName: "com.example.package"}
	utilsMock := &DummyUtilsGoogle{}
	googleModel := &GoogleModelImpl{Utils: utilsMock}

	notif := struct{}{}
	app.On("SendBroadcast", mock.Anything).Return()
	utilsMock.On("GetLaunchIntentForPackage", app).Return("com.example.package.MainActivity")

	err := googleModel.SetIconBadgeNum(app, notif, 5)
	assert.Error(t, err)
	assert.Equal(t, "google not support before API O", err.Error())
	app.AssertNotCalled(t, "SendBroadcast", mock.Anything)
}

func TestGoogleModelImpl_SetIconBadgeNum_SdkAtOrAboveO(t *testing.T) {
	setSdkIntForTest(26)
	app := &DummyApplicationGoogle{PackageName: "com.example.package"}
	utilsMock := &DummyUtilsGoogle{}
	googleModel := &GoogleModelImpl{Utils: utilsMock}

	notif := struct{}{}
	intentCap := new(DummyIntent)
	app.On("SendBroadcast", mock.AnythingOfType("*original.DummyIntent")).Return().Run(func(args mock.Arguments) {
		arg := args.Get(0).(*DummyIntent)
		*intentCap = *arg
	})
	utilsMock.On("GetLaunchIntentForPackage", app).Return("com.example.package.MainActivity")

	err := googleModel.SetIconBadgeNum(app, notif, 7)
	assert.NoError(t, err)
	app.AssertNumberOfCalls(t, "SendBroadcast", 1)
	assert.Equal(t, "android.intent.action.BADGE_COUNT_UPDATE", intentCap.GetAction())
	assert.Equal(t, 7, intentCap.GetIntExtra("badge_count", 0))
	assert.Equal(t, "com.example.package", intentCap.GetStringExtra("badge_count_package_name", ""))
	assert.Equal(t, "com.example.package.MainActivity", intentCap.GetStringExtra("badge_count_class_name", ""))
}