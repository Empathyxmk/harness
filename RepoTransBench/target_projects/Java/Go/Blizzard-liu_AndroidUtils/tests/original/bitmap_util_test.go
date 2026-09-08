package original

import (
    "testing"
)

type BitmapOptions struct {
    OutWidth         int
    OutHeight        int
    InJustDecodeBounds bool
    InSampleSize       int
}

func CalculateInSampleSize(opts *BitmapOptions, reqWidth, reqHeight int) *BitmapOptions {
    opts.InJustDecodeBounds = false
    w := opts.OutWidth
    h := opts.OutHeight
    sampleSize := 1
    if h > reqHeight || w > reqWidth {
        hRatio := h / reqHeight
        wRatio := w / reqWidth
        if hRatio > wRatio {
            sampleSize = hRatio
        } else {
            sampleSize = wRatio
        }
    }
    if sampleSize < 1 {
        sampleSize = 1
    }
    opts.InSampleSize = sampleSize
    return opts
}

func TestCalculateInSampleSizeLargeImage(t *testing.T) {
    options := &BitmapOptions{OutWidth: 900, OutHeight: 900}
    out := CalculateInSampleSize(options, 450, 400)
    if out != options {
        t.Errorf("Expected returned pointer to be options")
    }
    if out.InJustDecodeBounds != false {
        t.Errorf("Expected InJustDecodeBounds to be false")
    }
    if out.InSampleSize <= 1 {
        t.Errorf("Expected InSampleSize > 1, got %d", out.InSampleSize)
    }
}

func TestCalculateInSampleSizeSmallImage(t *testing.T) {
    options := &BitmapOptions{OutWidth: 200, OutHeight: 100}
    out := CalculateInSampleSize(options, 450, 400)
    if out != options {
        t.Errorf("Expected returned pointer to be options")
    }
    if out.InJustDecodeBounds != false {
        t.Errorf("Expected InJustDecodeBounds to be false")
    }
    if out.InSampleSize != 1 {
        t.Errorf("Expected InSampleSize == 1, got %d", out.InSampleSize)
    }
}

func TestBitmapUtilConstructorThrowsError(t *testing.T) {
    defer func() {
        if r := recover(); r == nil {
            t.Errorf("Expected panic from constructor")
        }
    }()
    bitmapUtilPanic()
}

func bitmapUtilPanic() {
    panic("BitmapUtil cannot be instantiated")
}