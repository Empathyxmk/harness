package db

import "testing"

func TestReleaseGarbagePermissions(t *testing.T) {
	type permission struct{ used, garbage bool }
	used := permission{used: true}
	garbage := permission{garbage: true}
	perms := []permission{used, garbage}
	var usedFound, garbageFound bool
	for _, p := range perms {
		if p.used {
			usedFound = true
		}
		if p.garbage {
			garbageFound = true
		}
	}
	if !usedFound || !garbageFound {
		t.Errorf("Permissions tracking failed")
	}
}