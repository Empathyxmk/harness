package public_tests

import (
	"testing"
	"github.com/tamir7/contacts"
)

func TestPhoneNumberPublic_ConstructorsAndGetters_Type(t *testing.T) {
	p := contacts.NewPhoneNumberWithType("7770011", contacts.PhoneNumberTypeMOBILE, "007770011")
	if p.Number != "7770011" {
		t.Errorf("expected 7770011, got %v", p.Number)
	}
	if p.NormalizedNumber != "007770011" {
		t.Errorf("expected 007770011, got %v", p.NormalizedNumber)
	}
	if p.Type != contacts.PhoneNumberTypeMOBILE {
		t.Errorf("expected MOBILE, got %v", p.Type)
	}
	if p.Label != "" {
		t.Errorf("expected empty label, got %v", p.Label)
	}
}

func TestPhoneNumberPublic_ConstructorsAndGetters_Label(t *testing.T) {
	p := contacts.NewPhoneNumberWithLabel("20202", "office label", "20202")
	if p.Number != "20202" {
		t.Errorf("expected 20202, got %v", p.Number)
	}
	if p.Label != "office label" {
		t.Errorf("expected office label, got %v", p.Label)
	}
	if p.Type != contacts.PhoneNumberTypeCUSTOM {
		t.Errorf("expected type CUSTOM, got %v", p.Type)
	}
	if p.NormalizedNumber != "20202" {
		t.Errorf("expected normalized number 20202, got %v", p.NormalizedNumber)
	}
}

func TestPhoneNumberPublic_EqualsAndHashCode(t *testing.T) {
	p1 := contacts.NewPhoneNumberWithType("3333", contacts.PhoneNumberTypeWORK, "xyz")
	p2 := contacts.NewPhoneNumberWithType("3333", contacts.PhoneNumberTypeWORK, "xyz")
	p3 := contacts.NewPhoneNumberWithType("1234", contacts.PhoneNumberTypeWORK, "xyz")
	if !p1.Equal(p2) {
		t.Errorf("expected p1==p2")
	}
	if p1.Equal(p3) {
		t.Errorf("expected p1!=p3")
	}
	if p1.HashCode() != p2.HashCode() {
		t.Errorf("hashcodes should match")
	}
}

func TestPhoneNumberPublic_TypeFromValue(t *testing.T) {
	cases := []struct {
		val int
		typ contacts.PhoneNumberType
	}{
		{-1, contacts.PhoneNumberTypeCUSTOM},
		{2, contacts.PhoneNumberTypeMOBILE},
		{3, contacts.PhoneNumberTypeWORK},
		{4, contacts.PhoneNumberTypeFAX_WORK},
		{5, contacts.PhoneNumberTypeFAX_HOME},
		{6, contacts.PhoneNumberTypePAGER},
		{7, contacts.PhoneNumberTypeOTHER},
		{8, contacts.PhoneNumberTypeCALLBACK},
		{9, contacts.PhoneNumberTypeCAR},
		{10, contacts.PhoneNumberTypeCOMPANY_MAIN},
		{11, contacts.PhoneNumberTypeISDN},
		{12, contacts.PhoneNumberTypeMAIN},
		{13, contacts.PhoneNumberTypeOTHER_FAX},
		{14, contacts.PhoneNumberTypeRADIO},
		{15, contacts.PhoneNumberTypeTELEX},
		{16, contacts.PhoneNumberTypeTTY_TDD},
		{17, contacts.PhoneNumberTypeWORK_MOBILE},
		{18, contacts.PhoneNumberTypeWORK_PAGER},
		{19, contacts.PhoneNumberTypeASSISTANT},
		{20, contacts.PhoneNumberTypeMMS},
		{-999, contacts.PhoneNumberTypeUNKNOWN},
	}
	for _, c := range cases {
		got := contacts.PhoneNumberTypeFromValue(c.val)
		if got != c.typ {
			t.Errorf("fromValue(%d): expected=%d got=%d", c.val, c.typ, got)
		}
	}
}

func TestPhoneNumberPublic_NotEqualConditions(t *testing.T) {
	p1 := contacts.NewPhoneNumberWithType("abc", contacts.PhoneNumberTypeMOBILE, "num")
	if p1.Equal(nil) {
		t.Errorf("should not equal nil")
	}
	if p1.Equal(42) {
		t.Errorf("should not equal unrelated type")
	}
	p2 := contacts.NewPhoneNumberWithType("xyz", contacts.PhoneNumberTypeMOBILE, "num")
	if p1.Equal(p2) {
		t.Errorf("should not equal p2, different number")
	}
}