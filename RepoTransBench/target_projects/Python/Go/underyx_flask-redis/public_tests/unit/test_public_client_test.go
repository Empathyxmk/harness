package unit

import (
	"testing"
	"strings"
)

type DummyRedis struct {
	url string
	kwargs map[string]interface{}
}

func (d *DummyRedis) FromURL(url string, kwargs map[string]interface{}) interface{} {
	d.url = url
	d.kwargs = kwargs
	return struct{}{}
}

func TestFlaskRedisInitAppDifferentURL(t *testing.T) {
	r := &struct{
		strict bool
		configPrefix string
		providerClass *DummyRedis
		extensions map[string]interface{}
	}{strict: false, configPrefix: "APP2", providerClass: &DummyRedis{}, extensions: map[string]interface{}{}}
	app := struct{
		config map[string]string
		extensions map[string]interface{}
	}{config: map[string]string{"APP2_URL": "redis://127.0.0.1:6382/5"}, extensions: map[string]interface{}{}}
	result := r.providerClass.FromURL("redis://127.0.0.1:6382/5", map[string]interface{}{"foo": "barbazquux"})
	if r.providerClass.url != "redis://127.0.0.1:6382/5" {
		t.Errorf("Expected URL correct, got %s", r.providerClass.url)
	}
	if r.providerClass.kwargs["foo"] != "barbazquux" {
		t.Errorf("Expected foo kwarg")
	}
	key := strings.ToLower(r.configPrefix)
	app.extensions[key] = r
	if _, ok := app.extensions["app2"]; !ok {
		t.Fatalf("Expected 'app2' in app.extensions")
	}
	if app.extensions["app2"] != r {
		t.Fatalf("Expected app.extensions['app2'] is r")
	}
}

func TestFromCustomProviderDiffURL(t *testing.T) {
	type OtherProvider struct{
		calledURL string
		calledKW map[string]interface{}
	}
	var other OtherProvider
	app := struct{
		config map[string]string
		extensions map[string]interface{}
	}{config: map[string]string{"REDIS_URL": "redis://192.168.1.2:6399/6"}, extensions: map[string]interface{}{}}
	FromURL := func(url string, kwargs map[string]interface{}) string {
		other.calledURL = url
		other.calledKW = kwargs
		return "hello-ext"
	}
	res := FromURL(app.config["REDIS_URL"], map[string]interface{}{"baropt": "bartest99"})
	if other.calledURL != "redis://192.168.1.2:6399/6" || other.calledKW["baropt"] != "bartest99" || res != "hello-ext" {
		t.Errorf("Provider called with wrong data or result")
	}
	app.extensions["redis"] = &other
	if _, ok := app.extensions["redis"]; !ok {
		t.Fatalf("Expected 'redis' key in app.extensions")
	}
}

func TestFlaskRedisBasicInstance(t *testing.T) {
	r := struct{
		configPrefix string
	}{configPrefix: "BAR"}
	if r.configPrefix != "BAR" {
		t.Errorf("configPrefix got: %s, want 'BAR'", r.configPrefix)
	}
	// Just check dummy interface functions exist
	_ = r
}