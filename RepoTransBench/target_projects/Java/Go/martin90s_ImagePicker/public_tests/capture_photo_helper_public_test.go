package public_tests

import (
	"os"
	"path/filepath"
	"testing"
)

type DummyActivityForCapturePublic struct {
	LastIntent     string
	LastRequestCode int
	PkgMgr         *DummyPackageManagerPublic
}

func (d *DummyActivityForCapturePublic) StartActivityForResult(intent string, requestCode int) {
	d.LastIntent = intent
	d.LastRequestCode = requestCode
}

type DummyFragmentForCapturePublic struct {
	LastIntent     string
	LastRequestCode int
	Activity       *DummyActivityForCapturePublic
}

func (d *DummyFragmentForCapturePublic) StartActivityForResult(intent string, requestCode int) {
	d.LastIntent = intent
	d.LastRequestCode = requestCode
}
func (d *DummyFragmentForCapturePublic) GetActivity() *DummyActivityForCapturePublic { return d.Activity }

type DummyPackageManagerPublic struct {
	NumResolveInfos int
}

type CapturePhotoHelperPublic struct {
	host     interface{}
	photo    string
	pkgmgr   *DummyPackageManagerPublic
}

const CAPTURE_PHOTO_REQUEST_CODE_PUBLIC = 1234

func NewCapturePhotoHelperPublic(host interface{}, pkgmgr *DummyPackageManagerPublic) *CapturePhotoHelperPublic {
	return &CapturePhotoHelperPublic{host: host, pkgmgr: pkgmgr}
}

func (h *CapturePhotoHelperPublic) HasCamera() bool {
	return h.pkgmgr != nil && h.pkgmgr.NumResolveInfos > 0
}

func (h *CapturePhotoHelperPublic) SetPhoto(path string) {
	h.photo = path
}

func (h *CapturePhotoHelperPublic) GetPhoto() string {
	return h.photo
}

func (h *CapturePhotoHelperPublic) CreatePhotoFile() *os.File {
	return nil
}

func (h *CapturePhotoHelperPublic) CapturePhoto(uri string) {
	if uri == "" {
		return
	}
	switch host := h.host.(type) {
	case *DummyFragmentForCapturePublic:
		host.StartActivityForResult("intent:"+uri, CAPTURE_PHOTO_REQUEST_CODE_PUBLIC)
	case *DummyActivityForCapturePublic:
		host.StartActivityForResult("intent:"+uri, CAPTURE_PHOTO_REQUEST_CODE_PUBLIC)
	}
}

func TestCapturePhotoHelper_HasCameraTrueAndFalse_Public(t *testing.T) {
	withCamera := &DummyPackageManagerPublic{NumResolveInfos: 2}
	withoutCamera := &DummyPackageManagerPublic{NumResolveInfos: 0}
	dummyAct := &DummyActivityForCapturePublic{PkgMgr: withCamera}
	hpAct := NewCapturePhotoHelperPublic(dummyAct, withCamera)
	if !hpAct.HasCamera() {
		t.Error("Expected HasCamera true (public)")
	}
	noCamAct := &DummyActivityForCapturePublic{PkgMgr: withoutCamera}
	hpNoCam := NewCapturePhotoHelperPublic(noCamAct, withoutCamera)
	if hpNoCam.HasCamera() {
		t.Error("Expected HasCamera false (public)")
	}
}

func TestCapturePhotoHelper_SetPhotoAndGetPhoto_Public(t *testing.T) {
	withCamera := &DummyPackageManagerPublic{NumResolveInfos: 2}
	dummyAct := &DummyActivityForCapturePublic{PkgMgr: withCamera}
	hp := NewCapturePhotoHelperPublic(dummyAct, withCamera)
	tempFile := filepath.Join(os.TempDir(), "unique_img.png")
	hp.SetPhoto(tempFile)
	photo := hp.GetPhoto()
	if photo != tempFile {
		t.Errorf("Expected %q, got %q", tempFile, photo)
	}
}

func TestCapturePhotoHelper_CreatePhotoFileFallback_Public(t *testing.T) {
	withCamera := &DummyPackageManagerPublic{NumResolveInfos: 2}
	dummyAct := &DummyActivityForCapturePublic{PkgMgr: withCamera}
	hp := NewCapturePhotoHelperPublic(dummyAct, withCamera)
	f := hp.CreatePhotoFile()
	if f != nil {
		t.Error("Expected CreatePhotoFile to return nil (public)")
	}
}

func TestCapturePhotoHelper_CapturePhoto_withUri_Public(t *testing.T) {
	withCamera := &DummyPackageManagerPublic{NumResolveInfos: 2}
	dummyAct := &DummyActivityForCapturePublic{PkgMgr: withCamera}
	dummyFrag := &DummyFragmentForCapturePublic{Activity: dummyAct}
	hpFrag := NewCapturePhotoHelperPublic(dummyFrag, withCamera)
	uri := "content://different/path"
	hpFrag.CapturePhoto(uri)
	if dummyFrag.LastIntent == "" || dummyFrag.LastRequestCode != CAPTURE_PHOTO_REQUEST_CODE_PUBLIC {
		t.Error("Fragment: Expected intent set with proper request code")
	}
	dummyAct.LastIntent = ""
	hpAct := NewCapturePhotoHelperPublic(dummyAct, withCamera)
	hpAct.CapturePhoto(uri)
	if dummyAct.LastIntent == "" || dummyAct.LastRequestCode != CAPTURE_PHOTO_REQUEST_CODE_PUBLIC {
		t.Error("Activity: Expected intent set with proper request code")
	}
}

func TestCapturePhotoHelper_CapturePhoto_nullUri_Public(t *testing.T) {
	withCamera := &DummyPackageManagerPublic{NumResolveInfos: 2}
	dummyAct := &DummyActivityForCapturePublic{PkgMgr: withCamera}
	hp := NewCapturePhotoHelperPublic(dummyAct, withCamera)
	hp.CapturePhoto("")
	if dummyAct.LastIntent != "" {
		t.Error("Should not call with null uri (public)")
	}
}