package public_tests

import (
	"reflect"
	"testing"

	"scrapinghub_adblockparser/adblockparser"
)

func TestPublicSplitDataTitles(t *testing.T) {
	xs := []string{"Joe", "amy", "Mike", "susan"}
	yes, no := adblockparser.SplitData(xs, func(t string) bool {
		return len(t) > 0 && t[0] >= 'A' && t[0] <= 'Z'
	})
	expectedYes := []string{"Joe", "Mike"}
	expectedNo := []string{"amy", "susan"}
	if !reflect.DeepEqual(yes, expectedYes) {
		t.Errorf("yes = %#v, want %#v", yes, expectedYes)
	}
	if !reflect.DeepEqual(no, expectedNo) {
		t.Errorf("no = %#v, want %#v", no, expectedNo)
	}
}

func TestPublicSplitDataAllYes(t *testing.T) {
	xs := []string{"Alpha", "Beta"}
	yes, no := adblockparser.SplitData(xs, func(s string) bool { return len(s) > 0 && s[0] >= 'A' && s[0] <= 'Z' })
	if !reflect.DeepEqual(yes, xs) {
		t.Errorf("yes = %#v, want %#v", yes, xs)
	}
	if len(no) != 0 {
		t.Errorf("no = %#v, want []", no)
	}
}

func TestPublicSplitDataAllNo(t *testing.T) {
	xs := []string{"gamma", "delta"}
	yes, no := adblockparser.SplitData(xs, func(s string) bool { return len(s) > 0 && s[0] >= 'A' && s[0] <= 'Z' })
	if len(yes) != 0 {
		t.Errorf("yes = %#v, want []", yes)
	}
	if !reflect.DeepEqual(no, xs) {
		t.Errorf("no = %#v, want %#v", no, xs)
	}
}

func TestPublicSplitDataEmpty(t *testing.T) {
	yes, no := adblockparser.SplitData([]string{}, func(string) bool { return true })
	if len(yes) != 0 || len(no) != 0 {
		t.Errorf("yes=%v no=%v, want [] []", yes, no)
	}
}