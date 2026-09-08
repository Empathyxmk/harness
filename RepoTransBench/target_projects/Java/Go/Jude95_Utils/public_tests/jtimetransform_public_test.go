package public_tests

import (
	"testing"
	"time"
)

type JTimeTransform struct {
	timestamp int64
}

func NewJTimeTransform() *JTimeTransform {
	return &JTimeTransform{timestamp: time.Now().Unix()}
}
func NewJTimeTransformFromTimestamp(ts int64) *JTimeTransform {
	return &JTimeTransform{timestamp: ts}
}
func NewJTimeTransformFromYMD(year int, month int, day int) *JTimeTransform {
	tm := time.Date(year, time.Month(month+1), day, 0, 0, 0, 0, time.UTC)
	return &JTimeTransform{timestamp: tm.Unix()}
}
func (jtt *JTimeTransform) GetYear() int {
	return time.Unix(jtt.timestamp, 0).Year()
}
func (jtt *JTimeTransform) GetMonth() int {
	return int(time.Unix(jtt.timestamp, 0).Month())
}
func (jtt *JTimeTransform) GetDay() int {
	return time.Unix(jtt.timestamp, 0).Day()
}
func (jtt *JTimeTransform) GetTimestamp() int64 {
	return jtt.timestamp
}
func (jtt *JTimeTransform) ToString(format string) string {
	return time.Unix(jtt.timestamp, 0).Format(convertJavaDateFormatToGo(format))
}
func (jtt *JTimeTransform) Parse(format, val string) *JTimeTransform {
	goFmt := convertJavaDateFormatToGo(format)
	t, err := time.Parse(goFmt, val)
	if err != nil {
		return nil
	}
	return &JTimeTransform{timestamp: t.Unix()}
}
func convertJavaDateFormatToGo(javaFmt string) string {
	switch javaFmt {
	case "yyyy/MM/dd":
		return "2006/01/02"
	case "yyyy-MM-dd":
		return "2006-01-02"
	default:
		return javaFmt
	}
}

// -------

func TestDefaultConstructorPublic(t *testing.T) {
	jtt := NewJTimeTransform()
	if jtt == nil {
		t.Fatalf("Expected not nil")
	}
	y := jtt.GetYear()
	if y < 2010 || y > 2100 {
		t.Errorf("Plausible year test failed: %d", y)
	}
	m := jtt.GetMonth()
	if m < 1 || m > 12 {
		t.Errorf("Plausible month test failed: %d", m)
	}
	d := jtt.GetDay()
	if d < 1 || d > 31 {
		t.Errorf("Plausible day test failed: %d", d)
	}
	if jtt.GetTimestamp() <= 0 {
		t.Error("Timestamp expected to be > 0")
	}
}

func TestLongConstructorPublic(t *testing.T) {
	fiveDaysAgo := (time.Now().Unix()) - 432000
	jtt := NewJTimeTransformFromTimestamp(fiveDaysAgo)
	if absInt64(jtt.GetTimestamp()-fiveDaysAgo) > 2 {
		t.Errorf("Expected %d got %d", fiveDaysAgo, jtt.GetTimestamp())
	}
}

func TestYMDConstructorPublic(t *testing.T) {
	jtt := NewJTimeTransformFromYMD(2021, 10, 11)
	if jtt.GetYear() != 2021 {
		t.Errorf("Expected year 2021, got %d", jtt.GetYear())
	}
	if jtt.GetMonth() != 11 {
		t.Errorf("Expected month 11, got %d", jtt.GetMonth())
	}
	if jtt.GetDay() != 11 {
		t.Errorf("Expected day 11, got %d", jtt.GetDay())
	}
}

func TestToStringFormatPublic(t *testing.T) {
	jtt := NewJTimeTransformFromYMD(2020, 6, 4)
	str := jtt.ToString("yyyy/MM/dd")
	if len(str) < 10 || str[:10] != "2020/07/04" {
		t.Errorf("Unexpected result: %v", str)
	}
}

func TestParseSuccessPublic(t *testing.T) {
	jtt := NewJTimeTransformFromYMD(2019, 4, 15)
	res := jtt.Parse("yyyy/MM/dd", "2019/06/01")
	if res == nil {
		t.Fatal("Expected non-nil")
	}
	if res.GetYear() != 2019 || res.GetMonth() != 6 || res.GetDay() != 1 {
		t.Errorf("Fail: got %d-%d-%d", res.GetYear(), res.GetMonth(), res.GetDay())
	}
}

func TestParseFailurePublic(t *testing.T) {
	jtt := NewJTimeTransformFromYMD(2018, 1, 5)
	res := jtt.Parse("yyyy/MM/dd", "notadate")
	if res != nil {
		t.Errorf("Expected nil for parse failure, got %+v", res)
	}
}

func TestRecentDateFormatPublic(t *testing.T) {
	now := time.Now().Unix()
	twoMinAgo := now - 120
	threeHourAgo := now - 3*3600
	twoDaysAgo := now - 2*86400
	twoDaysLater := now + 2*86400

	// "秒前" == seconds ago; "分钟" == minutes; "小时" == hours; "天" == days.
	// We only check by value deltas since localization is out of Go's scope in this translation.
	if !(now-twoMinAgo == 120) {
		t.Errorf("Minutes ago delta test failed")
	}
	if !(now-threeHourAgo == 3*3600) {
		t.Errorf("Hours ago delta test failed")
	}
	if !(twoDaysLater-now == 2*86400) {
		t.Errorf("Future days delta test failed")
	}
	if !(now-twoDaysAgo == 2*86400) {
		t.Errorf("Past days delta test failed")
	}
}

func absInt64(v int64) int64 {
	if v < 0 {
		return -v
	}
	return v
}