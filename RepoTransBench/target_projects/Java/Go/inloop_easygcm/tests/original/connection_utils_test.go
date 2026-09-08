package original

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// --- Interfaces and mocks for emulating Android behavior ---

type Context interface {
    GetPackageManager() PackageManager
    GetPackageName() string
    GetSystemService(service string) interface{}
}

type PackageManager interface {
    CheckPermission(perm, pkg string) int
}

type ConnectivityManager interface {
    GetActiveNetworkInfo() NetworkInfo
}

type NetworkInfo interface {
    IsConnected() bool
}

const (
    PERMISSION_GRANTED = 1
    PERMISSION_DENIED  = -1
)

// --- Mocks ---

type MockContext struct {
    mock.Mock
}

func (m *MockContext) GetPackageManager() PackageManager {
    args := m.Called()
    return args.Get(0).(PackageManager)
}
func (m *MockContext) GetPackageName() string {
    args := m.Called()
    return args.String(0)
}
func (m *MockContext) GetSystemService(service string) interface{} {
    args := m.Called(service)
    return args.Get(0)
}

type MockPackageManager struct {
    mock.Mock
}

func (m *MockPackageManager) CheckPermission(perm, pkg string) int {
    args := m.Called(perm, pkg)
    return args.Int(0)
}

type MockConnectivityManager struct {
    mock.Mock
}

func (m *MockConnectivityManager) GetActiveNetworkInfo() NetworkInfo {
    args := m.Called()
    if args.Get(0) == nil {
        return nil
    }
    return args.Get(0).(NetworkInfo)
}

type MockNetworkInfo struct {
    mock.Mock
}

func (m *MockNetworkInfo) IsConnected() bool {
    args := m.Called()
    return args.Bool(0)
}

// --- Code under test (to be replaced by actual implementation) ---

func HasAccessNetworkStatePermission(ctx Context) bool {
    pm := ctx.GetPackageManager()
    pkgName := ctx.GetPackageName()
    perm := pm.CheckPermission("android.permission.ACCESS_NETWORK_STATE", pkgName)
    return perm == PERMISSION_GRANTED
}

func IsOnline(ctx Context) bool {
    pm := ctx.GetPackageManager()
    pkgName := ctx.GetPackageName()
    if pm.CheckPermission("android.permission.ACCESS_NETWORK_STATE", pkgName) != PERMISSION_GRANTED {
        // "Hope for best" branch: return true
        return true
    }

    cm, ok := ctx.GetSystemService("connectivity").(ConnectivityManager)
    if !ok || cm == nil {
        return false
    }
    netInfo := cm.GetActiveNetworkInfo()
    if netInfo == nil {
        return false
    }
    return netInfo.IsConnected()
}

// --- Tests ---

func TestHasAccessNetworkStatePermissionGranted(t *testing.T) {
    ctx := new(MockContext)
    pm := new(MockPackageManager)
    ctx.On("GetPackageManager").Return(pm)
    ctx.On("GetPackageName").Return("eu.inloop.easygcm.test")

    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(PERMISSION_GRANTED)

    assert.True(t, HasAccessNetworkStatePermission(ctx))
}

func TestHasAccessNetworkStatePermissionDenied(t *testing.T) {
    ctx := new(MockContext)
    pm := new(MockPackageManager)
    ctx.On("GetPackageManager").Return(pm)
    ctx.On("GetPackageName").Return("eu.inloop.easygcm.test")

    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(PERMISSION_DENIED)

    assert.False(t, HasAccessNetworkStatePermission(ctx))
}

func TestIsOnlineWithPermissionAndConnected(t *testing.T) {
    ctx := new(MockContext)
    pm := new(MockPackageManager)
    cm := new(MockConnectivityManager)
    netInfo := new(MockNetworkInfo)

    ctx.On("GetPackageManager").Return(pm)
    ctx.On("GetPackageName").Return("eu.inloop.easygcm.test")
    ctx.On("GetSystemService", "connectivity").Return(cm)
    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(PERMISSION_GRANTED)
    cm.On("GetActiveNetworkInfo").Return(netInfo)
    netInfo.On("IsConnected").Return(true)

    assert.True(t, IsOnline(ctx))
}

func TestIsOnlineWithPermissionAndNotConnected(t *testing.T) {
    ctx := new(MockContext)
    pm := new(MockPackageManager)
    cm := new(MockConnectivityManager)
    netInfo := new(MockNetworkInfo)

    ctx.On("GetPackageManager").Return(pm)
    ctx.On("GetPackageName").Return("eu.inloop.easygcm.test")
    ctx.On("GetSystemService", "connectivity").Return(cm)
    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(PERMISSION_GRANTED)
    cm.On("GetActiveNetworkInfo").Return(netInfo)
    netInfo.On("IsConnected").Return(false)

    assert.False(t, IsOnline(ctx))
}

func TestIsOnlineWithPermissionAndNoNetworkInfo(t *testing.T) {
    ctx := new(MockContext)
    pm := new(MockPackageManager)
    cm := new(MockConnectivityManager)

    ctx.On("GetPackageManager").Return(pm)
    ctx.On("GetPackageName").Return("eu.inloop.easygcm.test")
    ctx.On("GetSystemService", "connectivity").Return(cm)
    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(PERMISSION_GRANTED)
    cm.On("GetActiveNetworkInfo").Return(nil)

    assert.False(t, IsOnline(ctx))
}

func TestIsOnlineWithoutPermission(t *testing.T) {
    ctx := new(MockContext)
    pm := new(MockPackageManager)

    ctx.On("GetPackageManager").Return(pm)
    ctx.On("GetPackageName").Return("eu.inloop.easygcm.test")
    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(PERMISSION_DENIED)

    assert.True(t, IsOnline(ctx))
}