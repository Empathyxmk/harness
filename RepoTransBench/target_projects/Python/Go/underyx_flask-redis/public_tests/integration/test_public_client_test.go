package integration

import (
	"strings"
	"testing"
)

type DummyRedisPublic struct {
	calledWithURL    string
	calledWithKWArgs map[string]interface{}
}

func (d *DummyRedisPublic) FromURL(url string, kwargs map[string]interface{}) interface{} {
	d.calledWithURL = url
	d.calledWithKWArgs = kwargs
	return struct{}{}
}

func TestInitAppCustomUrlPublic(t *testing.T) {
	instance := &struct {
		strict       bool
		configPrefix string
		providerClass *DummyRedisPublic
	}{strict: false, configPrefix: "FOO", providerClass: &DummyRedisPublic{}}

	dummyApp := struct {
		config     map[string]string
		extensions map[string]interface{}
	}{
		config:     map[string]string{"FOO_URL": "redis://localhost:6380/2"},
		extensions: map[string]interface{}{},
	}

	result := instance.providerClass.FromURL("redis://localhost:6380/2", map[string]interface{}{"password": "letmein"})
	if instance.providerClass.calledWithURL != "redis://localhost:6380/2" {
		t.Errorf("Expected URL = redis://localhost:6380/2, got %s", instance.providerClass.calledWithURL)
	}
	if instance.providerClass.calledWithKWArgs["password"] != "letmein" {
		t.Errorf("Expected password == letmein in kwargs")
	}
	key := strings.ToLower(instance.configPrefix)
	dummyApp.extensions[key] = instance
	if _, ok := dummyApp.extensions["foo"]; !ok {
		t.Fatalf("Expected 'foo' in dummyApp.extensions")
	}
	if dummyApp.extensions["foo"] != instance {
		t.Fatalf("Expected dummyApp.extensions['foo'] is instance")
	}
}

func TestFromCustomProviderPublic(t *testing.T) {
	type CustomProvider struct{
		lastURL string
		lastKW  map[string]interface{}
	}
	var provider CustomProvider
	dummyApp := struct{
		config map[string]string
		extensions map[string]interface{}
	}{config: map[string]string{"REDIS_URL": "redis://localhost:6381/4"}, extensions: map[string]interface{}{}}
	FromURL := func(url string, kwargs map[string]interface{}) string {
		provider.lastURL = url
		provider.lastKW = kwargs
		return "custom-conn"
	}
	res := FromURL(dummyApp.config["REDIS_URL"], map[string]interface{}{"fooopt": 99})
	if provider.lastURL != "redis://localhost:6381/4" || provider.lastKW["fooopt"] != 99 || res != "custom-conn" {
		t.Errorf("Custom provider wrong args or result")
	}
	dummyApp.extensions["redis"] = &provider
	if _, ok := dummyApp.extensions["redis"]; !ok {
		t.Fatalf("Expected 'redis' key in dummyApp.extensions")
	}
}