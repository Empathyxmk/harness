package original

import (
	"testing"

	"jameszbl_java_design_patterns/builder"
)

func TestNoNamePanics(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic on no name, got nil")
		}
	}()
	_ = builder.NewPersonBuilder().Name("").Age(17).Nationality(builder.NationalityJapan).SkinColor(builder.SkinColorYellow).Build()
}

func TestPersonBuild(t *testing.T) {
	name := "老张"
	age := 57
	person := builder.NewPersonBuilder().Name(name).Age(age).Nationality(builder.NationalityJapan).SkinColor(builder.SkinColorYellow).Build()
	if person == nil {
		t.Fatalf("person is nil")
	}
	if got := person.String(); got == "" {
		t.Errorf("person.String() empty")
	}
	if person.Name() != name {
		t.Errorf("Name: got %q, want %q", person.Name(), name)
	}
	if person.Age() != age {
		t.Errorf("Age: got %d, want %d", person.Age(), age)
	}
	if person.Nationality() != builder.NationalityJapan {
		t.Errorf("Nationality: got %v, want %v", person.Nationality(), builder.NationalityJapan)
	}
	if person.SkinColor() != builder.SkinColorYellow {
		t.Errorf("SkinColor: got %v, want %v", person.SkinColor(), builder.SkinColorYellow)
	}
}