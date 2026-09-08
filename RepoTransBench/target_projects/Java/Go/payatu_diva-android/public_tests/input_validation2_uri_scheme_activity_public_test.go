package public_tests

import "testing"

type EditText struct {
	text string
}

type InputValidation2URISchemeActivity struct {
	input *EditText
}

func NewInputValidation2URIActivityPublic() *InputValidation2URISchemeActivity {
	return &InputValidation2URISchemeActivity{
		input: &EditText{},
	}
}

func (a *InputValidation2URISchemeActivity) FindViewById(id int) *EditText {
	return a.input
}

func TestInputValidation2URISchemeActivity_userInput_isAccepted_public(t *testing.T) {
	act := NewInputValidation2URIActivityPublic()
	input := act.FindViewById(10)
	publicInput := "publicTestInput"
	input.text = publicInput
	if input.text != publicInput {
		t.Errorf("Expected input %q, got %q", publicInput, input.text)
	}
}