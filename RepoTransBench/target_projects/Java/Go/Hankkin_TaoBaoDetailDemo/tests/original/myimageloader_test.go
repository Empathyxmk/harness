package original

import (
	"testing"
)

// Singleton pattern for MyImageLoader
type MyImageLoader struct{}

var instance *MyImageLoader

func GetMyImageLoaderInstance() *MyImageLoader {
	if instance == nil {
		instance = &MyImageLoader{}
	}
	return instance
}

func (l *MyImageLoader) DisplayImage(context, url string)     {}
func (l *MyImageLoader) DisplayImageWithProgress(context, url string, withProgress bool) {
}
func (l *MyImageLoader) DisplayFile(context, filename string)                           {}
func (l *MyImageLoader) DisplayFileWithDim(context, filename string, w, h int)          {}
func (l *MyImageLoader) DisplayImageWH(context, url string, w, h int, progress bool)    {}
func (l *MyImageLoader) DisplayImageFitted(context, url string, w, h int)               {}
func (l *MyImageLoader) DisplayImageCenter(context, url string, w, h int)               {}

func TestMyImageLoader_GetInstanceSingleton(t *testing.T) {
	loader1 := GetMyImageLoaderInstance()
	loader2 := GetMyImageLoaderInstance()
	if loader1 != loader2 {
		t.Error("MyImageLoader.getInstance() should return same singleton instance")
	}
}

func TestMyImageLoader_DisplayImageSignatures(t *testing.T) {
	loader := GetMyImageLoaderInstance()
	loader.DisplayImage("context", "http://example.com/img.png")
	loader.DisplayImageWithProgress("context", "http://example.com/img2.png", true)
	loader.DisplayFile("context", "")
	loader.DisplayFileWithDim("context", "", 100, 100)
	loader.DisplayImageWH("context", "http://example.com/img3.png", 100, 100, true)
	loader.DisplayImageWH("context", "http://example.com/img4.png", 120, 80, false)
	loader.DisplayImageFitted("context", "http://example.com/img5.png", 80, 90)
	loader.DisplayImageCenter("context", "http://example.com/img6.png", 40, 20)
	// Test just ensures all "API surfaces" called, no panics/exceptions.
}