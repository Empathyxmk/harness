package public_tests

import (
	"testing"
)

type SpeechRecognizer struct{}

type SpeechRecognizerSetup struct {
	acousticModel, dictionary, rawLogDir string
}

func DefaultSpeechRecognizerSetup() *SpeechRecognizerSetup {
	return &SpeechRecognizerSetup{}
}

func (s *SpeechRecognizerSetup) SetAcousticModel(f string) *SpeechRecognizerSetup {
	s.acousticModel = f
	return s
}
func (s *SpeechRecognizerSetup) SetDictionary(f string) *SpeechRecognizerSetup {
	s.dictionary = f
	return s
}
func (s *SpeechRecognizerSetup) SetRawLogDir(f string) *SpeechRecognizerSetup {
	s.rawLogDir = f
	return s
}
func (s *SpeechRecognizerSetup) GetRecognizer() *SpeechRecognizer {
	return &SpeechRecognizer{}
}

func TestDefaultSetupReturnsSetupInstancePublic(t *testing.T) {
	setup := DefaultSpeechRecognizerSetup()
	if setup == nil {
		t.Fatal("Expected setup to be non-nil")
	}
}

func TestSetupWithNonExistingFilesPublic(t *testing.T) {
	setup := DefaultSpeechRecognizerSetup()
	model := "dummy_model_dir_public"
	dict := "dummy_dict_file_public.dic"
	logDir := "dummy_log_dir_public"
	if setup.SetAcousticModel(model) != setup {
		t.Errorf("SetAcousticModel should return self")
	}
	if setup.SetDictionary(dict) != setup {
		t.Errorf("SetDictionary should return self")
	}
	if setup.SetRawLogDir(logDir) != setup {
		t.Errorf("SetRawLogDir should return self")
	}
}

func TestGetRecognizerReturnsInstancePublic(t *testing.T) {
	setup := DefaultSpeechRecognizerSetup()
	if setup.GetRecognizer() == nil {
		t.Fatal("Expected non-nil SpeechRecognizer from GetRecognizer")
	}
}