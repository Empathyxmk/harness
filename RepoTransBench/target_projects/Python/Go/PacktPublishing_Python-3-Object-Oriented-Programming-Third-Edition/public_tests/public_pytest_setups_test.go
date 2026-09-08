package public_tests

import (
	"testing"
)

type CustomResource struct {
	Name   string
	Status string
}

func (c *CustomResource) Use() {
	c.Status = c.Name + " used"
}
func (c *CustomResource) Destroy() {
	c.Status = "destroyed"
}

func resourcePublic() *CustomResource {
	return &CustomResource{Name: "RESOURCE_X_PUBLIC", Status: "new"}
}

func TestResourceName(t *testing.T) {
	r := resourcePublic()
	if r.Name != "RESOURCE_X_PUBLIC" {
		t.Errorf("Expected resource name RESOURCE_X_PUBLIC")
	}
	r.Use()
	if r.Status != "RESOURCE_X_PUBLIC used" {
		t.Errorf("Expected status RESOURCE_X_PUBLIC used, got %v", r.Status)
	}
}

func TestResourceDestroy(t *testing.T) {
	r := resourcePublic()
	r.Destroy()
	if r.Status != "destroyed" {
		t.Errorf("Expected status destroyed, got %v", r.Status)
	}
}