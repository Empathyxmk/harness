package original

import (
    "errors"
    "testing"
)

type fakePkgInfo struct {
    VersionCode int
    VersionName string
}

type fakePackageManager struct {
    pkgInfo *fakePkgInfo
    fail    bool
}

func (pm *fakePackageManager) GetPackageInfo(pkg string) (*fakePkgInfo, error) {
    if pm.fail {
        return nil, errors.New("NameNotFoundException")
    }
    return pm.pkgInfo, nil
}

type fakeContext struct {
    packageName string
    pm         *fakePackageManager
}

func (c *fakeContext) GetPackageName() string {
    return c.packageName
}
func (c *fakeContext) GetPackageManager() *fakePackageManager {
    return c.pm
}

func TestGetVerCodeNormal(t *testing.T) {
    info := &fakePkgInfo{VersionCode: 123}
    pm := &fakePackageManager{pkgInfo: info}
    ctx := &fakeContext{packageName: "pkg", pm: pm}
    code, err := AppUtilsGetVerCode(ctx)
    if err != nil || code != 123 {
        t.Errorf("Expected version code 123, got %d, err: %v", code, err)
    }
}

func TestGetVerCodeNotFound(t *testing.T) {
    pm := &fakePackageManager{fail: true}
    ctx := &fakeContext{packageName: "pkg", pm: pm}
    code, err := AppUtilsGetVerCode(ctx)
    if err == nil || code != -1 {
        t.Errorf("Expected -1 and error, got %d, %v", code, err)
    }
}

func TestGetVerNameNormal(t *testing.T) {
    info := &fakePkgInfo{VersionName: "verX"}
    pm := &fakePackageManager{pkgInfo: info}
    ctx := &fakeContext{packageName: "pkg", pm: pm}
    name, err := AppUtilsGetVerName(ctx)
    if err != nil || name != "verX" {
        t.Errorf("Expected verX, got %q, err: %v", name, err)
    }
}

func TestGetVerNameNotFound(t *testing.T) {
    pm := &fakePackageManager{fail: true}
    ctx := &fakeContext{packageName: "pkg", pm: pm}
    name, err := AppUtilsGetVerName(ctx)
    if name != "" || err == nil {
        t.Errorf("Expected empty string and error, got %q, %v", name, err)
    }
}

// Simulated implementation for tests
func AppUtilsGetVerCode(ctx *fakeContext) (int, error) {
    pm := ctx.GetPackageManager()
    info, err := pm.GetPackageInfo(ctx.GetPackageName())
    if err != nil {
        return -1, err
    }
    return info.VersionCode, nil
}

func AppUtilsGetVerName(ctx *fakeContext) (string, error) {
    pm := ctx.GetPackageManager()
    info, err := pm.GetPackageInfo(ctx.GetPackageName())
    if err != nil {
        return "", err
    }
    return info.VersionName, nil
}