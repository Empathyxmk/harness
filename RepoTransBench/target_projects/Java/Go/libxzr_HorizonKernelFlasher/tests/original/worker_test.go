package original

import (
	"errors"
	"io"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// --- Mocks ---

type ActivityStub struct {
	mock.Mock
	tmpdir string
}

func (a *ActivityStub) GetFilesDir() string {
	return a.tmpdir
}

// ---- Worker structure and functions ---

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
	// simulate copy uses ContentResolver, which can throw IO error by test.
	args := w.activity.Called()
	return args.Error(0)
}

func (w *Worker) getBinary() error {
	// Simulates open non-existing file (should fail).
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

func TestWorker_RootAvailable_True(t *testing.T) {
	a := &ActivityStub{tmpdir: os.TempDir()}
	w := NewWorker(a)
	a.On("Called").Return("root xzr", nil)
	assert.True(t, w.rootAvailable())
}

func TestWorker_RootAvailable_False(t *testing.T) {
	a := &ActivityStub{tmpdir: os.TempDir()}
	w := NewWorker(a)
	a.On("Called").Return("", errors.New("io"))
	assert.False(t, w.rootAvailable())
}

func TestWorker_Copy_Throws(t *testing.T) {
	a := &ActivityStub{tmpdir: os.TempDir()}
	w := NewWorker(a)
	a.On("Called").Return(errors.New("fail"))
	err := w.copy()
	assert.Error(t, err)
}

func TestWorker_GetBinary_NotExist(t *testing.T) {
	a := &ActivityStub{tmpdir: os.TempDir()}
	w := NewWorker(a)
	w.file_path = filepath.Join(os.TempDir(), "notfound.zip")
	_, _ = os.Remove(w.file_path) // ensure doesn't exist
	err := w.getBinary()
	assert.Error(t, err)
}

func TestWorker_Patch_AssetsUtilThrows(t *testing.T) {
	a := &ActivityStub{tmpdir: os.TempDir()}
	w := NewWorker(a)
	a.On("Called").Return(errors.New("fail"))
	err := w.patch()
	assert.Error(t, err)
}

func TestWorker_Flash_Throws(t *testing.T) {
	a := &ActivityStub{tmpdir: os.TempDir()}
	w := NewWorker(a)
	a.On("Called").Return(errors.New("fail"))
	err := w.flash(a)
	assert.Error(t, err)
}