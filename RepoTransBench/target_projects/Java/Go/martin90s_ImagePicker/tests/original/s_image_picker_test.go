package original

import (
	"errors"
	"reflect"
	"testing"
)

type DummyConfig struct {
	Ctx interface{}
}

type DummyActivity struct {
	LastIntent     string
	LastRequestCode int
}

func (d *DummyActivity) StartActivityForResult(intent string, requestCode int) {
	d.LastIntent = intent
	d.LastRequestCode = requestCode
}

type DummyFragment struct {
	Act            *DummyActivity
	LastIntent     string
	LastRequestCode int
}

func (d *DummyFragment) GetActivity() *DummyActivity {
	return d.Act
}
func (d *DummyFragment) StartActivityForResult(intent string, requestCode int) {
	d.LastIntent = intent
	d.LastRequestCode = requestCode
}

// For singleton logic emulation
var sImagePickerConfig interface{}

type SImagePicker struct {
	target interface{}
}

func SImagePickerInit(cfg interface{}) {
	sImagePickerConfig = cfg
}

func SImagePickerFrom(target interface{}) *SImagePicker {
	return &SImagePicker{target: target}
}

func SImagePickerGetConfig() interface{} {
	if sImagePickerConfig == nil {
		panic("Picker not initialized")
	}
	return sImagePickerConfig
}

func (s *SImagePicker) MaxCount(n int) *SImagePicker      { return s }
func (s *SImagePicker) RowCount(n int) *SImagePicker      { return s }
func (s *SImagePicker) PickMode(n int) *SImagePicker      { return s }
func (s *SImagePicker) CropFilePath(s2 string) *SImagePicker { return s }
func (s *SImagePicker) ShowCamera(b bool) *SImagePicker   { return s }
func (s *SImagePicker) PickText(n int) *SImagePicker      { return s }
func (s *SImagePicker) SetSelected(sel []string) *SImagePicker { return s }
func (s *SImagePicker) FileInterceptor(_ interface{}) *SImagePicker { return s }
func (s *SImagePicker) ForResult(requestCode int) {
	if s.target == nil {
		panic("Neither activity nor fragment")
	}

	switch t := s.target.(type) {
	case *DummyActivity:
		t.StartActivityForResult("intent", requestCode)
	case *DummyFragment:
		t.StartActivityForResult("intent", requestCode)
	default:
		panic("Neither activity nor fragment")
	}
}

const (
	MODE_AVATAR = 1
	MODE_IMAGE  = 2
)

var dummyActivity *DummyActivity
var dummyFragment *DummyFragment

func setupSImagePicker() {
	dummyActivity = &DummyActivity{}
	dummyFragment = &DummyFragment{Act: dummyActivity}
	SImagePickerInit(&DummyConfig{Ctx: dummyActivity})
}

func TestSImagePicker_GetPickerConfig_ExceptionIfNotInitialized(t *testing.T) {
	setupSImagePicker()
	SImagePickerFrom(dummyActivity)
	// Simulate "unset"
	sImagePickerConfig = nil
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for not initialized")
		}
	}()
	SImagePickerGetConfig()
}

func TestSImagePicker_ForResult_NoInitThrows(t *testing.T) {
	setupSImagePicker()
	sImagePickerConfig = nil
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for not initialized")
		}
	}()
	SImagePickerFrom(dummyActivity).ForResult(1)
}

func TestSImagePicker_FromActivityAndFromFragment(t *testing.T) {
	setupSImagePicker()
	picker1 := SImagePickerFrom(dummyActivity)
	if picker1 == nil {
		t.Error("Picker1 should not be nil")
	}
	picker2 := SImagePickerFrom(dummyFragment)
	if picker2 == nil {
		t.Error("Picker2 should not be nil")
	}
}

func TestSImagePicker_MethodChaining(t *testing.T) {
	setupSImagePicker()
	picker := SImagePickerFrom(dummyActivity)
	selected := []string{}
	picker.MaxCount(5).RowCount(2).PickMode(MODE_AVATAR).CropFilePath("test.jpg").ShowCamera(true).PickText(123).SetSelected(selected)
}

func TestSImagePicker_ForResult_CallsActivityAndFragment(t *testing.T) {
	setupSImagePicker()
	pickerA := SImagePickerFrom(dummyActivity)
	pickerA.ForResult(99)
	if dummyActivity.LastIntent == "" || dummyActivity.LastRequestCode != 99 {
		t.Errorf("Expected activity intent and request code 99")
	}
	pickerF := SImagePickerFrom(dummyFragment)
	pickerF.ForResult(66)
	if dummyFragment.LastIntent == "" || dummyFragment.LastRequestCode != 66 {
		t.Errorf("Expected fragment intent and request code 66")
	}
}

func TestSImagePicker_ForResult_NeitherActivityNorFragment(t *testing.T) {
	setupSImagePicker()
	picker := &SImagePicker{target: nil}
	SImagePickerInit(&DummyConfig{Ctx: dummyActivity})
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for neither activity nor fragment")
		}
	}()
	picker.ForResult(7)
}

func TestSImagePicker_FileInterceptor(t *testing.T) {
	setupSImagePicker()
	picker := SImagePickerFrom(dummyActivity)
	picker.FileInterceptor(nil)
}