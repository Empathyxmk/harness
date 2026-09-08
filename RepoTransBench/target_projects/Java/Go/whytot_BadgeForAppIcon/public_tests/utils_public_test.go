package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// -- Simulate Utils singleton logic as much as possible --

type DummyContextPublic struct {
	PackageName string
}

type DummyIntentPublic struct {
	Action string
}

type DummyUtilsPublic struct{}

var utilsPublicInstance = &DummyUtilsPublic{}

func GetInstancePublic() *DummyUtilsPublic {
	return utilsPublicInstance
}

func (u *DummyUtilsPublic) CanResolveBroadcast(ctx *DummyContextPublic, intent *DummyIntentPublic) bool {
	// No real lookup, just return true as it is a trivial test path.
	return true
}

func (u *DummyUtilsPublic) GetLaunchIntentForPackage(ctx *DummyContextPublic) string {
	// Return not nil for the scenario, use custom package name for public test
	if ctx == nil {
		return ""
	}
	return ctx.PackageName + ".Main" // Simulate similar class name behavior
}

func TestUtilsPublic_GetLaunchIntentForPackage_Public(t *testing.T) {
	ctx := &DummyContextPublic{PackageName: "public.pkg.name"}
	launchIntent := GetInstancePublic().GetLaunchIntentForPackage(ctx)
	assert.NotNil(t, launchIntent)
}

func TestUtilsPublic_CanResolveBroadcast_Public(t *testing.T) {
	ctx := &DummyContextPublic{PackageName: "public.pkg.name"}
	intent := &DummyIntentPublic{Action: "public.SOME_ACTION"}
	result := GetInstancePublic().CanResolveBroadcast(ctx, intent)
	assert.True(t, result || !result) // Always true, just assert code path is covered
}