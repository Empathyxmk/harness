package public_tests

import (
	"errors"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// -- Fakes --

type ActivityStub struct {
	mock.Mock
	tmpdir string
}

func (a *ActivityStub) GetFilesDir() string {
	return a.tmpdir
}

type Worker struct {
	activity    *ActivityStub
	file_path   string
	binary_path string
	uri         interface{}
}

func NewWorker(a *ActivityStub) *Worker {
	return &Worker{activity: a}
}

func (w *Worker) runWithNewProcessReturn(_ bool, _ string) (string, error) {
	args := w.activity.Called()
	val, ok := args.Get(0).(string)
	if !ok {
		return "", args.Error(0)
	}
	return val, args.Error(1)
}

func (w *Worker) runWithNewProcessNoReturn(_ bool, _ string) error {
	args := w.activity.Called()
	return args.Error(0)
}
func (w *Worker) rootAvailable() bool {
	out, err := w.runWithNewProcessReturn(true, "id")
	return err == nil && out != "" && len(out) > 0
}

func (w *Worker) copy() error {
	args := w.activity.Called()
	return args.Error(0)
}

func (w *Worker) getBinary() error {
	_, err := os.Stat(w.file_path)
	if err != nil {
		return err
	}
	return nil
}

func (w *Worker) patch() error {
	args := w.activity.Called()
	return args.Error(0)
}

func (w *Worker) flash(act *ActivityStub) error {
	args := w.activity.Called()
	return args.Error(0)
}

// ------- TESTS --------

func TestWorkerPublic_RootAvailable_True(t *testing.T) {
	a := &ActivityStub{tmpdir: filepath.Join(os.TempDir(), "workerpublictest")}
	w := NewWorker(a)
	a.On("Called").Return("root otheruser", nil)
	assert.True(t, w.rootAvailable())
}

func TestWorkerPublic_RootAvailable_False(t *testing.T) {
	a := &ActivityStub{tmpdir: filepath.Join(os.TempDir(), "workerpublictest")}
	w := NewWorker(a)
	a.On("Called").Return(nil, nil)
	assert.False(t, w.rootAvailable())
}

func TestWorkerPublic_Copy_Throws(t *testing.T) {
	a := &ActivityStub{tmpdir: filepath.Join(os.TempDir(), "workerpublictest")}
	w := NewWorker(a)
	a.On("Called").Return(errors.New("fail again"))
	err := w.copy()
	assert.Error(t, err)
}

func TestWorkerPublic_GetBinary_NotExist(t *testing.T) {
	a := &ActivityStub{tmpdir: filepath.Join(os.TempDir(), "workerpublictest")}
	w := NewWorker(a)
	w.file_path = filepath.Join(os.TempDir(), "definitely_missing.zip")
	w.binary_path = filepath.Join(os.TempDir(), "definitely_missing-binary")
	_, _ = os.Remove(w.file_path)
	err := w.getBinary()
	assert.Error(t, err)
}

func TestWorkerPublic_Patch_AssetsUtilThrows(t *testing.T) {
	a := &ActivityStub{tmpdir: filepath.Join(os.TempDir(), "workerpublictest")}
	w := NewWorker(a)
	a.On("Called").Return(errors.New("fail2"))
	err := w.patch()
	assert.Error(t, err)
}

func TestWorkerPublic_Flash_Throws(t *testing.T) {
	a := &ActivityStub{tmpdir: filepath.Join(os.TempDir(), "workerpublictest")}
	w := NewWorker(a)
	a.On("Called").Return(errors.New("fail3"))
	err := w.flash(a)
	assert.Error(t, err)
}