package public_tests

import (
	"testing"
)

type ImageLoaderPublic interface {
	Display(path string, width, height int)
	Pause()
	Resume()
	ClearMemoryCache()
	ClearDiskCache()
}

type DummyImageLoaderPublic struct {
	DisplayCalled    bool
	PauseCalled      bool
	ResumeCalled     bool
	ClearMemCalled   bool
	ClearDiskCalled  bool
}

func (d *DummyImageLoaderPublic) Display(path string, width, height int) {
	d.DisplayCalled = true
}
func (d *DummyImageLoaderPublic) Pause() {
	d.PauseCalled = true
}
func (d *DummyImageLoaderPublic) Resume() {
	d.ResumeCalled = true
}
func (d *DummyImageLoaderPublic) ClearMemoryCache() {
	d.ClearMemCalled = true
}
func (d *DummyImageLoaderPublic) ClearDiskCache() {
	d.ClearDiskCalled = true
}

func TestImageLoader_DisplayMethod_Public(t *testing.T) {
	loader := &DummyImageLoaderPublic{}
	loader.Display("some/path/public", 301, 401)
	if !loader.DisplayCalled {
		t.Error("Expected DisplayCalled true (public)")
	}
}

func TestImageLoader_PauseResumeAndClearCaches_Public(t *testing.T) {
	loader := &DummyImageLoaderPublic{}
	loader.Pause()
	if !loader.PauseCalled {
		t.Error("Pause should be called (public)")
	}
	loader.Resume()
	if !loader.ResumeCalled {
		t.Error("Resume should be called (public)")
	}
	loader.ClearMemoryCache()
	if !loader.ClearMemCalled {
		t.Error("ClearMemoryCache should be called (public)")
	}
	loader.ClearDiskCache()
	if !loader.ClearDiskCalled {
		t.Error("ClearDiskCache should be called (public)")
	}
}