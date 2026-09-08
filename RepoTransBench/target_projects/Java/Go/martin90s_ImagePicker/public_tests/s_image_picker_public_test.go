package public_tests

import (
	"testing"
)

type DummyConfigPublic struct {
	Ctx interface{}
}

type DummyActivityPublic struct {
	LastIntent     string
	LastRequestCode int
}

func (d *DummyActivityPublic) StartActivityForResult(intent string, requestCode int) {
	d.LastIntent = intent
	d.LastRequestCode = requestCode
}

type DummyFragmentPublic struct {
	Act            *DummyActivityPublic
	LastIntent     string
	LastRequestCode int
}

func (d *DummyFragmentPublic) GetActivity() *DummyActivityPublic {
	return d.Act
}
func (d *DummyFragmentPublic) StartActivityForResult(intent string, requestCode int) {
	d.LastIntent = intent
	d.LastRequestCode = requestCode
}

// Singleton-like cfg
var sImagePickerConfigPublic interface{}

type SImagePickerPublic struct {
	target interface{}
}

// Initialization and helpers
func SImagePickerInitPublic(cfg interface{}) {
	sImagePickerConfigPublic = cfg
}

func SImagePickerFromPublic(target interface{}) *SImagePickerPublic {
	return &SImagePickerPublic{target: target}
}

func SImagePickerGetConfigPublic() interface{} {
	if sImagePickerConfigPublic == nil {
		panic("Picker not initialized")
	}
	return sImagePickerConfigPublic
}

func (s *SImagePickerPublic) MaxCount(n int) *SImagePickerPublic      { return s }
func (s *SImagePickerPublic) RowCount(n int) *SImagePickerPublic      { return s }
func (s *SImagePickerPublic) PickMode(n int) *SImagePickerPublic      { return s }
func (s *SImagePickerPublic) CropFilePath(s2 string) *SImagePickerPublic { return s }
func (s *SImagePickerPublic) ShowCamera(b bool) *SImagePickerPublic   { return s }
func (s *SImagePickerPublic) PickText(n int) *SImagePickerPublic      { return s }
func (s *SImagePickerPublic) SetSelected(sel []string) *SImagePickerPublic { return s }
func (s *SImagePickerPublic) FileInterceptor(_ interface{}) *SImagePickerPublic { return s }
func (s *SImagePickerPublic) ForResult(requestCode int) {
	if s.target == nil {
		panic("Neither activity nor fragment")
	}
	switch t := s.target.(type) {
	case *DummyActivityPublic:
		t.StartActivityForResult("intent", requestCode)
	case *DummyFragmentPublic:
		t.StartActivityForResult("intent", requestCode)
	default:
		panic("Neither activity nor fragment")
	}
}

const (
	MODE_IMAGE = 2
)

var dummyActivityPublic *DummyActivityPublic
var dummyFragmentPublic *DummyFragmentPublic

func setupSImagePickerPublic() {
	dummyActivityPublic = &DummyActivityPublic{}
	dummyFragmentPublic = &DummyFragmentPublic{Act: dummyActivityPublic}
	SImagePickerInitPublic(&DummyConfigPublic{Ctx: dummyActivityPublic})
}

func TestSImagePicker_GetPickerConfig_ExceptionIfNotInitialized_Public(t *testing.T) {
	setupSImagePickerPublic()
	SImagePickerFromPublic(dummyActivityPublic)
	sImagePickerConfigPublic = nil
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for not initialized (public)")
		}
	}()
	SImagePickerGetConfigPublic()
}

func TestSImagePicker_ForResult_NoInitThrows_Public(t *testing.T) {
	setupSImagePickerPublic()
	sImagePickerConfigPublic = nil
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for not initialized (public)")
		}
	}()
	SImagePickerFromPublic(dummyActivityPublic).ForResult(11)
}

func TestSImagePicker_FromActivityAndFromFragment_Public(t *testing.T) {
	setupSImagePickerPublic()
	picker1 := SImagePickerFromPublic(dummyActivityPublic)
	if picker1 == nil {
		t.Error("Picker1 should not be nil")
	}
	picker2 := SImagePickerFromPublic(dummyFragmentPublic)
	if picker2 == nil {
		t.Error("Picker2 should not be nil")
	}
}

func TestSImagePicker_MethodChaining_Public(t *testing.T) {
	setupSImagePickerPublic()
	picker := SImagePickerFromPublic(dummyActivityPublic)
	selected := []string{"abc"}
	picker.MaxCount(3).RowCount(5).PickMode(MODE_IMAGE).CropFilePath("other_file.png").
		ShowCamera(false).PickText(456).SetSelected(selected)
}

func TestSImagePicker_ForResult_CallsActivityAndFragment_Public(t *testing.T) {
	setupSImagePickerPublic()
	pickerA := SImagePickerFromPublic(dummyActivityPublic)
	pickerA.ForResult(42)
	if dummyActivityPublic.LastIntent == "" || dummyActivityPublic.LastRequestCode != 42 {
		t.Errorf("Expected activity intent and request code 42")
	}
	pickerF := SImagePickerFromPublic(dummyFragmentPublic)
	pickerF.ForResult(24)
	if dummyFragmentPublic.LastIntent == "" || dummyFragmentPublic.LastRequestCode != 24 {
		t.Errorf("Expected fragment intent and request code 24")
	}
}

func TestSImagePicker_ForResult_NeitherActivityNorFragment_Public(t *testing.T) {
	setupSImagePickerPublic()
	picker := &SImagePickerPublic{target: nil}
	SImagePickerInitPublic(&DummyConfigPublic{Ctx: dummyActivityPublic})
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic for neither activity nor fragment")
		}
	}()
	picker.ForResult(999)
}

func TestSImagePicker_FileInterceptor_Public(t *testing.T) {
	setupSImagePickerPublic()
	picker := SImagePickerFromPublic(dummyActivityPublic)
	anonInterceptor := struct{}{}
	picker.FileInterceptor(anonInterceptor)
}