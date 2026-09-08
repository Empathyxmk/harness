package public_tests

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
    "github.com/inloop-easygcm/go-easygcm/tests/original"
)

func setupConnectionUtilsMocksPublic() (*original.MockContext, *original.MockPackageManager, *original.MockConnectivityManager, *original.MockNetworkInfo) {
    ctx := new(original.MockContext)
    pm := new(original.MockPackageManager)
    cm := new(original.MockConnectivityManager)
    netInfo := new(original.MockNetworkInfo)
    ctx.On("GetPackageManager").Return(pm)
    ctx.On("GetPackageName").Return("eu.inloop.easygcm.publictest")
    return ctx, pm, cm, netInfo
}

func TestHasAccessNetworkStatePermissionGrantedDifferent(t *testing.T) {
    ctx, pm, _, _ := setupConnectionUtilsMocksPublic()
    pm.On("CheckPermission", "android.permission.ACCESS_NETWORK_STATE", "eu.inloop.easygcm.publictest").Return(original.PERMISSION_GRANTED)
    assert.True(t, original.HasAccessNetworkStatePermission(ctx))
}

func TestHasAccessNetworkStatePermissionDeniedDifferent(t *testing.T) {
    ctx, pm, _, _ := setupConnectionUtilsMocksPublic()
    pm.On("CheckPermission", "android.permission.ACCESS_NETWORK_STATE", "eu.inloop.easygcm.publictest").Return(original.PERMISSION_DENIED)
    assert.False(t, original.HasAccessNetworkStatePermission(ctx))
}

func TestIsOnlineWithPermissionAndConnectedDifferent(t *testing.T) {
    ctx, pm, cm, netInfo := setupConnectionUtilsMocksPublic()
    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(original.PERMISSION_GRANTED)
    ctx.On("GetSystemService", "connectivity").Return(cm)
    cm.On("GetActiveNetworkInfo").Return(netInfo)
    netInfo.On("IsConnected").Return(true)
    assert.True(t, original.IsOnline(ctx))
}

func TestIsOnlineWithPermissionAndNotConnectedDifferent(t *testing.T) {
    ctx, pm, cm, netInfo := setupConnectionUtilsMocksPublic()
    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(original.PERMISSION_GRANTED)
    ctx.On("GetSystemService", "connectivity").Return(cm)
    cm.On("GetActiveNetworkInfo").Return(netInfo)
    netInfo.On("IsConnected").Return(false)
    assert.False(t, original.IsOnline(ctx))
}

func TestIsOnlineWithPermissionAndNoNetworkInfoDifferent(t *testing.T) {
    ctx, pm, cm, _ := setupConnectionUtilsMocksPublic()
    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(original.PERMISSION_GRANTED)
    ctx.On("GetSystemService", "connectivity").Return(cm)
    cm.On("GetActiveNetworkInfo").Return(nil)
    assert.False(t, original.IsOnline(ctx))
}

func TestIsOnlineWithoutPermissionDifferent(t *testing.T) {
    ctx, pm, _, _ := setupConnectionUtilsMocksPublic()
    pm.On("CheckPermission", mock.Anything, mock.Anything).Return(original.PERMISSION_DENIED)
    assert.True(t, original.IsOnline(ctx))
}