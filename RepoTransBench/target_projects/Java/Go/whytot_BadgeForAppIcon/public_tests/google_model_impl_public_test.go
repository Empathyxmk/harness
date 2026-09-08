package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// Support dummy for GoogleModelImpl (public test)
type DummyIntentPub struct {
	action string
	extras map[string]interface{}
}

func NewDummyIntentPub(action string) *DummyIntentPub {
	return &DummyIntentPub{action: action, extras: make(map[string]interface{})}
}
func (d *DummyIntentPub) SetExtra(key string, val interface{}) {
	d.extras[key] = val
}
func (d *DummyIntentPub) GetAction() string { return d.action }
func (d *DummyIntentPub) GetIntExtra(key string, def int) int {
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
func (d *DummyIntentPub) GetStringExtra(key string, def string) string {
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

type DummyApplicationGooglePub struct {
	mock.Mock
	PackageName string
}

func (a *DummyApplicationGooglePub) SendBroadcast(intent *DummyIntentPub) {
	a.Called(intent)
}
func (a *DummyApplicationGooglePub) GetPackageName() string { return a.PackageName }

type DummyUtilsGooglePub struct {
	mock.Mock
}

func (u *DummyUtilsGooglePub) GetLaunchIntentForPackage(app *DummyApplicationGooglePub) string {
	args := u.Called(app)
	return args.String(0)
}
func (u *DummyUtilsGooglePub) CanResolveBroadcast(app *DummyApplicationGooglePub, intent *DummyIntentPub) bool {
	args := u.Called(app, intent)
	return args.Bool(0)
}

type GoogleModelImplPublic struct {
	Utils *DummyUtilsGooglePub
}

var sdkIntForTestPublic = 0

func setSdkIntForTestPublic(val int) {
	sdkIntForTestPublic = val
}

func (g *GoogleModelImplPublic) SetIconBadgeNum(app *DummyApplicationGooglePub, notif interface{}, count int) error {
	if sdkIntForTestPublic < 26 {
		return errors.New("google not support before API O")
	}
	intent := NewDummyIntentPub("android.intent.action.BADGE_COUNT_UPDATE")
	intent.SetExtra("badge_count", count)
	intent.SetExtra("badge_count_package_name", app.GetPackageName())
	intent.SetExtra("badge_count_class_name", g.Utils.GetLaunchIntentForPackage(app))
	app.SendBroadcast(intent)
	return nil
}

func TestGoogleModelImplPublic_SetIconBadgeNum_SdkBelowO(t *testing.T) {
	setSdkIntForTestPublic(24)
	app := &DummyApplicationGooglePub{PackageName: "sample.another"}
	utilsMock := &DummyUtilsGooglePub{}
	googleModel := &GoogleModelImplPublic{Utils: utilsMock}
	notif := struct{}{}
	app.On("SendBroadcast", mock.Anything).Return()
	utilsMock.On("GetLaunchIntentForPackage", app).Return("sample.another.MainAct")

	err := googleModel.SetIconBadgeNum(app, notif, 15)
	assert.Error(t, err)
	assert.Equal(t, "google not support before API O", err.Error())
	app.AssertNotCalled(t, "SendBroadcast", mock.Anything)
}

func TestGoogleModelImplPublic_SetIconBadgeNum_SdkAtOrAboveO(t *testing.T) {
	setSdkIntForTestPublic(27)
	app := &DummyApplicationGooglePub{PackageName: "sample.another"}
	utilsMock := &DummyUtilsGooglePub{}
	googleModel := &GoogleModelImplPublic{Utils: utilsMock}
	notif := struct{}{}
	intentCap := new(DummyIntentPub)
	app.On("SendBroadcast", mock.AnythingOfType("*public_tests.DummyIntentPub")).Return().Run(func(args mock.Arguments) {
		arg := args.Get(0).(*DummyIntentPub)
		*intentCap = *arg
	})
	utilsMock.On("GetLaunchIntentForPackage", app).Return("sample.another.MainAct")

	err := googleModel.SetIconBadgeNum(app, notif, 21)
	assert.NoError(t, err)
	app.AssertNumberOfCalls(t, "SendBroadcast", 1)
	assert.Equal(t, "android.intent.action.BADGE_COUNT_UPDATE", intentCap.GetAction())
	assert.Equal(t, 21, intentCap.GetIntExtra("badge_count", 0))
	assert.Equal(t, "sample.another", intentCap.GetStringExtra("badge_count_package_name", ""))
	assert.Equal(t, "sample.another.MainAct", intentCap.GetStringExtra("badge_count_class_name", ""))
}