package original

import (
	"testing"
	"github.com/tamir7/contacts"
)

func TestPhoneNumber_ConstructorsAndGetters_Type(t *testing.T) {
	p := contacts.NewPhoneNumberWithType("12345", contacts.PhoneNumberTypeHOME, "54321")
	if p.Number != "12345" {
		t.Errorf("expected number 12345, got %v", p.Number)
	}
	if p.NormalizedNumber != "54321" {
		t.Errorf("expected normalized 54321, got %v", p.NormalizedNumber)
	}
	if p.Type != contacts.PhoneNumberTypeHOME {
		t.Errorf("expected type HOME, got %v", p.Type)
	}
	if p.Label != "" {
		t.Errorf("expected label empty, got %v", p.Label)
	}
}

func TestPhoneNumber_ConstructorsAndGetters_Label(t *testing.T) {
	p := contacts.NewPhoneNumberWithLabel("333", "mobile label", "333")
	if p.Number != "333" {
		t.Errorf("expected number 333, got %v", p.Number)
	}
	if p.Label != "mobile label" {
		t.Errorf("expected label mobile label, got %v", p.Label)
	}
	if p.Type != contacts.PhoneNumberTypeCUSTOM {
		t.Errorf("expected type CUSTOM, got %v", p.Type)
	}
	if p.NormalizedNumber != "333" {
		t.Errorf("expected normalized number 333, got %v", p.NormalizedNumber)
	}
}

func TestPhoneNumber_EqualsAndHashCode(t *testing.T) {
	p1 := contacts.NewPhoneNumberWithType("123", contacts.PhoneNumberTypeHOME, "abc")
	p2 := contacts.NewPhoneNumberWithType("123", contacts.PhoneNumberTypeHOME, "abc")
	p3 := contacts.NewPhoneNumberWithType("999", contacts.PhoneNumberTypeHOME, "abc")
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

func TestPhoneNumber_TypeFromValue(t *testing.T) {
	cases := []struct {
		val int
		typ contacts.PhoneNumberType
	}{
		{0, contacts.PhoneNumberTypeCUSTOM},
		{1, contacts.PhoneNumberTypeHOME},
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
		{999, contacts.PhoneNumberTypeUNKNOWN},
	}
	for _, c := range cases {
		got := contacts.PhoneNumberTypeFromValue(c.val)
		if got != c.typ {
			t.Errorf("fromValue(%d): expected=%d got=%d", c.val, c.typ, got)
		}
	}
}

func TestPhoneNumber_NotEqualConditions(t *testing.T) {
	p1 := contacts.NewPhoneNumberWithType("x", contacts.PhoneNumberTypeHOME, "n")
	if p1.Equal(nil) {
		t.Errorf("should not equal nil")
	}
	if p1.Equal("notPhone") {
		t.Errorf("should not equal a string")
	}
	p2 := contacts.NewPhoneNumberWithType("different", contacts.PhoneNumberTypeHOME, "n")
	if p1.Equal(p2) {
		t.Errorf("should not equal as numbers differ")
	}
}