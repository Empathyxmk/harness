package original

import (
	"os"
	"path/filepath"
	"testing"
)

type DummyActivityForCapture struct {
	LastIntent     string
	LastRequestCode int
	PkgMgr         *DummyPackageManager
}

func (d *DummyActivityForCapture) StartActivityForResult(intent string, requestCode int) {
	d.LastIntent = intent
	d.LastRequestCode = requestCode
}

type DummyFragmentForCapture struct {
	LastIntent     string
	LastRequestCode int
	Activity       *DummyActivityForCapture
}

func (d *DummyFragmentForCapture) StartActivityForResult(intent string, requestCode int) {
	d.LastIntent = intent
	d.LastRequestCode = requestCode
}
func (d *DummyFragmentForCapture) GetActivity() *DummyActivityForCapture { return d.Activity }

type DummyPackageManager struct {
	HasCamera bool
}

type CapturePhotoHelper struct {
	host     interface{}
	photo    string
	pkgmgr   *DummyPackageManager
}

const CAPTURE_PHOTO_REQUEST_CODE = 1234

func NewCapturePhotoHelper(host interface{}, pkgmgr *DummyPackageManager) *CapturePhotoHelper {
	return &CapturePhotoHelper{host: host, pkgmgr: pkgmgr}
}

func (h *CapturePhotoHelper) HasCamera() bool {
	return h.pkgmgr != nil && h.pkgmgr.HasCamera
}

func (h *CapturePhotoHelper) SetPhoto(path string) {
	h.photo = path
}

func (h *CapturePhotoHelper) GetPhoto() string {
	return h.photo
}

func (h *CapturePhotoHelper) CreatePhotoFile() *os.File {
	// Simulate as needed
	return nil
}

func (h *CapturePhotoHelper) CapturePhoto(uri string) {
	if uri == "" {
		return
	}
	switch host := h.host.(type) {
	case *DummyFragmentForCapture:
		host.StartActivityForResult("intent:"+uri, CAPTURE_PHOTO_REQUEST_CODE)
	case *DummyActivityForCapture:
		host.StartActivityForResult("intent:"+uri, CAPTURE_PHOTO_REQUEST_CODE)
	}
}

func TestCapturePhotoHelper_HasCameraTrueAndFalse(t *testing.T) {
	withCamera := &DummyPackageManager{HasCamera: true}
	withoutCamera := &DummyPackageManager{HasCamera: false}
	dummyAct := &DummyActivityForCapture{PkgMgr: withCamera}
	hpAct := NewCapturePhotoHelper(dummyAct, withCamera)
	if !hpAct.HasCamera() {
		t.Error("Expected HasCamera true")
	}
	noCamAct := &DummyActivityForCapture{PkgMgr: withoutCamera}
	hpNoCam := NewCapturePhotoHelper(noCamAct, withoutCamera)
	if hpNoCam.HasCamera() {
		t.Error("Expected HasCamera false")
	}
}

func TestCapturePhotoHelper_SetPhotoAndGetPhoto(t *testing.T) {
	withCamera := &DummyPackageManager{HasCamera: true}
	dummyAct := &DummyActivityForCapture{PkgMgr: withCamera}
	hp := NewCapturePhotoHelper(dummyAct, withCamera)
	tempFile := filepath.Join(os.TempDir(), "abcde.jpg")
	hp.SetPhoto(tempFile)
	photo := hp.GetPhoto()
	if photo != tempFile {
		t.Errorf("Expected %q, got %q", tempFile, photo)
	}
}

func TestCapturePhotoHelper_CreatePhotoFileFallback(t *testing.T) {
	withCamera := &DummyPackageManager{HasCamera: true}
	dummyAct := &DummyActivityForCapture{PkgMgr: withCamera}
	hp := NewCapturePhotoHelper(dummyAct, withCamera)
	f := hp.CreatePhotoFile()
	if f != nil {
		t.Error("Expected CreatePhotoFile to return nil")
	}
}

func TestCapturePhotoHelper_CapturePhoto_withUri(t *testing.T) {
	withCamera := &DummyPackageManager{HasCamera: true}
	dummyAct := &DummyActivityForCapture{PkgMgr: withCamera}
	dummyFrag := &DummyFragmentForCapture{Activity: dummyAct}
	hpFrag := NewCapturePhotoHelper(dummyFrag, withCamera)
	uri := "content://foo/bar"
	hpFrag.CapturePhoto(uri)
	if dummyFrag.LastIntent == "" || dummyFrag.LastRequestCode != CAPTURE_PHOTO_REQUEST_CODE {
		t.Error("Fragment: Expected intent set with proper request code")
	}
	dummyAct.LastIntent = ""
	hpAct := NewCapturePhotoHelper(dummyAct, withCamera)
	hpAct.CapturePhoto(uri)
	if dummyAct.LastIntent == "" || dummyAct.LastRequestCode != CAPTURE_PHOTO_REQUEST_CODE {
		t.Error("Activity: Expected intent set with proper request code")
	}
}

func TestCapturePhotoHelper_CapturePhoto_nullUri(t *testing.T) {
	withCamera := &DummyPackageManager{HasCamera: true}
	dummyAct := &DummyActivityForCapture{PkgMgr: withCamera}
	hp := NewCapturePhotoHelper(dummyAct, withCamera)
	hp.CapturePhoto("")
	if dummyAct.LastIntent != "" {
		t.Error("Should not call with null uri")
	}
}