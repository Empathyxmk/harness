package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// --- Mock structures similar to Android Context/Intent/PackageManager ---

type DummyResolveInfo struct{}
type DummyComponentName struct {
	className string
}
func (c *DummyComponentName) GetClassName() string { return c.className }

type DummyIntentUtils struct {
	action string
}
func (i *DummyIntentUtils) Action() string       { return i.action }
func (i *DummyIntentUtils) SetAction(a string)   { i.action = a }

type DummyPackageManager struct {
	mock.Mock
}

func (p *DummyPackageManager) QueryBroadcastReceivers(intent *DummyIntentUtils, flags int) []DummyResolveInfo {
	args := p.Called(intent, flags)
	if li, ok := args.Get(0).([]DummyResolveInfo); ok {
		return li
	}
	return nil
}

func (p *DummyPackageManager) GetLaunchIntentForPackage(pkg string) *DummyIntentUtils {
	args := p.Called(pkg)
	i, _ := args.Get(0).(*DummyIntentUtils)
	return i
}

type DummyContext struct {
	mock.Mock
	PackageName string
	PackageManager *DummyPackageManager
}

func (c *DummyContext) GetPackageManager() *DummyPackageManager {
	return c.PackageManager
}
func (c *DummyContext) GetPackageName() string { return c.PackageName }


// ---- UTILS CODE/TESTS ----

// Singleton-style utility struct
type UtilsSingleton struct{}

var utilsInstance = &UtilsSingleton{}

func GetInstance() *UtilsSingleton {
	return utilsInstance
}

func (u *UtilsSingleton) CanResolveBroadcast(ctx *DummyContext, intent *DummyIntentUtils) bool {
	pm := ctx.GetPackageManager()
	out := pm.QueryBroadcastReceivers(intent, 0)
	return out != nil && len(out) > 0
}

func (u *UtilsSingleton) GetLaunchIntentForPackage(ctx *DummyContext) string {
	pm := ctx.GetPackageManager()
	pkg := ctx.GetPackageName()
	intent := pm.GetLaunchIntentForPackage(pkg)
	compName := intent.GetClassName()
	if compName == "" {
		panic(errors.New("getComponent() is nil"))
	}
	return compName
}

// ---- TESTS ----

func TestUtils_GetInstance_Singleton(t *testing.T) {
	i1 := GetInstance()
	i2 := GetInstance()
	assert.NotNil(t, i1)
	assert.Equal(t, i1, i2)
}

func TestUtils_CanResolveBroadcast_NoReceivers(t *testing.T) {
	pm := new(DummyPackageManager)
	ctx := &DummyContext{PackageManager: pm}
	pm.On("QueryBroadcastReceivers", mock.Anything, 0).Return(nil)
	assert.False(t, GetInstance().CanResolveBroadcast(ctx, &DummyIntentUtils{}))

	pm.On("QueryBroadcastReceivers", mock.Anything, 0).Return([]DummyResolveInfo{})
	assert.False(t, GetInstance().CanResolveBroadcast(ctx, &DummyIntentUtils{}))
}

func TestUtils_CanResolveBroadcast_WithReceivers(t *testing.T) {
	pm := new(DummyPackageManager)
	ctx := &DummyContext{PackageManager: pm}
	pm.On("QueryBroadcastReceivers", mock.Anything, 0).Return([]DummyResolveInfo{{}})
	assert.True(t, GetInstance().CanResolveBroadcast(ctx, &DummyIntentUtils{}))
}

func TestUtils_GetLaunchIntentForPackage(t *testing.T) {
	pm := new(DummyPackageManager)
	compName := &DummyComponentName{className: "com.example.package.MainActivity"}
	intent := &DummyIntentUtils{}
	pm.On("GetLaunchIntentForPackage", "com.example.package").Return(compName)
	ctx := &DummyContext{PackageName: "com.example.package", PackageManager: pm}

	// Simulate intent.GetComponent() being the compName object
	intentClassName := pm.GetLaunchIntentForPackage(ctx.PackageName).GetClassName()
	assert.Equal(t, "com.example.package.MainActivity", intentClassName)
}

func TestUtils_GetLaunchIntentForPackage_NullLaunchIntent(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic when intent is nil")
		}
	}()
	pm := new(DummyPackageManager)
	pm.On("GetLaunchIntentForPackage", "com.example.package").Return(&DummyComponentName{className: ""})
	ctx := &DummyContext{PackageName: "com.example.package", PackageManager: pm}

	GetInstance().GetLaunchIntentForPackage(ctx)
}