package tests

import (
	"reflect"
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

func TestSplitDataTitles(t *testing.T) {
	xs := []string{"foo", "Bar", "Spam", "egg"}
	yes, no := adblockparser.SplitData(xs, func(t string) bool {
		return len(t) > 0 && t[0] >= 'A' && t[0] <= 'Z'
	})
	expectedYes := []string{"Bar", "Spam"}
	expectedNo := []string{"foo", "egg"}
	if !reflect.DeepEqual(yes, expectedYes) {
		t.Errorf("yes = %#v, want %#v", yes, expectedYes)
	}
	if !reflect.DeepEqual(no, expectedNo) {
		t.Errorf("no = %#v, want %#v", no, expectedNo)
	}
}

func TestSplitDataAllYes(t *testing.T) {
	xs := []string{"Hello", "World"}
	yes, no := adblockparser.SplitData(xs, func(s string) bool { return len(s) > 0 && s[0] >= 'A' && s[0] <= 'Z' })
	if !reflect.DeepEqual(yes, xs) {
		t.Errorf("yes = %#v, want %#v", yes, xs)
	}
	if len(no) != 0 {
		t.Errorf("no = %#v, want []", no)
	}
}

func TestSplitDataAllNo(t *testing.T) {
	xs := []string{"foo", "bar"}
	yes, no := adblockparser.SplitData(xs, func(s string) bool { return len(s) > 0 && s[0] >= 'A' && s[0] <= 'Z' })
	if len(yes) != 0 {
		t.Errorf("yes = %#v, want []", yes)
	}
	if !reflect.DeepEqual(no, xs) {
		t.Errorf("no = %#v, want %#v", no, xs)
	}
}

func TestSplitDataEmpty(t *testing.T) {
	yes, no := adblockparser.SplitData([]string{}, func(string) bool { return false })
	if len(yes) != 0 || len(no) != 0 {
		t.Errorf("yes=%v no=%v, want [] []", yes, no)
	}
}