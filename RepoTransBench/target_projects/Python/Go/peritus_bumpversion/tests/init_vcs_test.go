package tests

import (
	"testing"
	"errors"
	"bumpversion"
)

func TestDiscardDefaultIfSpecifiedAppendAction(t *testing.T) {
	parser := struct{}{}
	namespace := struct{ Foo []int }{Foo: []int{1}}
	action := bumpversion.NewDiscardDefaultIfSpecifiedAppendAction("foo")
	action.Call(parser, &namespace, 2)
	if len(namespace.Foo) != 1 || namespace.Foo[0] != 2 {
		t.Errorf("Expected namespace.Foo == [2], got %v", namespace.Foo)
	}
}

func TestBaseVCSIsUsableOSError(t *testing.T) {
	bumpversion.SetSubprocessCallFunc(func(args ...interface{}) error {
		return errors.New("No such file or directory")
	})

	res := bumpversion.NewDummyBaseVCS([]string{"nonexistent"}).IsUsable()
	if res {
		t.Errorf("Expected is_usable to be false on OSError")
	}
}

func TestBaseVCSIsUsableOtherRaises(t *testing.T) {
	bumpversion.SetSubprocessCallFunc(func(args ...interface{}) error {
		return errors.New("other error")
	})
	dummy := bumpversion.NewDummyBaseVCS([]string{"other"})
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic (OSError) for other error")
		}
	}()
	_ = dummy.IsUsable()
}

func TestGitLatestTagInfoDirty(t *testing.T) {
	dummyGit := bumpversion.NewDummyGit()
	info := dummyGit.LatestTagInfo()
	if dirty, ok := info["dirty"].(bool); !ok || !dirty {
		t.Errorf("Expected latest_tag_info dirty True, got %v", info["dirty"])
	}
}