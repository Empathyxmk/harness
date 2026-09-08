package original

import (
	"reflect"
	"testing"
	pdfredactor "pdfredactor"
)

func TestRedactorOptions_Defaults(t *testing.T) {
	opts := pdfredactor.NewRedactorOptions()
	if opts.InputStream != nil {
		t.Errorf("expected InputStream to be nil")
	}
	if opts.OutputStream != nil {
		t.Errorf("expected OutputStream to be nil")
	}
	if !reflect.DeepEqual(opts.MetadataFilters, map[string][]func(string)string{}) {
		t.Errorf("expected MetadataFilters to be empty map, got %+v", opts.MetadataFilters)
	}
	if len(opts.XMPFilters) != 0 {
		t.Errorf("expected XMPFilters to be empty")
	}
	if opts.XMPSerializer != nil {
		t.Errorf("expected XMPSerializer to be nil")
	}
	if len(opts.ContentFilters) != 0 {
		t.Errorf("expected ContentFilters to be empty")
	}
	expGlyphs := []rune{'?', '#', '*', ' '}
	if !reflect.DeepEqual(opts.ContentReplacementGlyphs, expGlyphs) {
		t.Errorf("expected ContentReplacementGlyphs %v, got %v", expGlyphs, opts.ContentReplacementGlyphs)
	}
	if len(opts.LinkFilters) != 0 {
		t.Errorf("expected LinkFilters to be empty")
	}
}

func TestRedactorOptions_SettingOptions(t *testing.T) {
	opts := pdfredactor.NewRedactorOptions()
	opts.InputStream = "input"
	opts.OutputStream = "output"
	opts.MetadataFilters = map[string][]func(string)string{
		"Title": {
			func(v string) string { return "NewTitle" },
		},
	}
	opts.ContentFilters = []pdfredactor.ContentFilter{}
	opts.LinkFilters = []func(string, interface{}) interface{}{
		func(href string, annotation interface{}) interface{} { return nil },
	}
	opts.XMPFilters = []func(interface{}) interface{}{
		func(xml interface{}) interface{} { return nil },
	}
	opts.XMPSerializer = func(xml interface{}) string { return "<xml />" }

	if opts.InputStream != "input" {
		t.Errorf("InputStream not set correctly")
	}
	if opts.OutputStream != "output" {
		t.Errorf("OutputStream not set correctly")
	}
	if reflect.TypeOf(opts.MetadataFilters["Title"][0]).Kind() != reflect.Func {
		t.Errorf("MetadataFilters[\"Title\"] is not a function")
	}
	if opts.LinkFilters[0]("href", nil) != nil {
		t.Errorf("LinkFilters function did not return nil")
	}
	if opts.XMPFilters[0](nil) != nil {
		t.Errorf("XMPFilters function did not return nil")
	}
	if opts.XMPSerializer(nil) != "<xml />" {
		t.Errorf("XMPSerializer did not return expected string")
	}
}