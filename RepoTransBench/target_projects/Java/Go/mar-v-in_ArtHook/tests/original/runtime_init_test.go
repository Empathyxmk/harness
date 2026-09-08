package original

import (
    "testing"

    "github.com/stretchr/testify/mock"
)

// --- Mock infrastructure ---

type RuntimeInitXposedMainMock struct {
    mock.Mock
}

type RuntimeInitUtilsCallMainMock struct {
    mock.Mock
}

func (m *RuntimeInitXposedMainMock) Main(isRuntime bool, args []string) {
    m.Called(isRuntime, args)
}
func (m *RuntimeInitUtilsCallMainMock) CallMain(className string, args []string) {
    m.Called(className, args)
}

// SUT
func RuntimeInitMain(xposed func(bool, []string), utils func(string, []string), args []string) {
    xposed(false, args)
    utils("com.android.internal.os.RuntimeInit", args)
}

func TestRuntimeInitMainRunsXposedAndUtils(t *testing.T) {
    xposedMock := new(RuntimeInitXposedMainMock)
    utilsMock := new(RuntimeInitUtilsCallMainMock)
    args := []string{"bar"}

    xposedMock.On("Main", false, args).Return()
    utilsMock.On("CallMain", "com.android.internal.os.RuntimeInit", args).Return()

    RuntimeInitMain(xposedMock.Main, utilsMock.CallMain, args)

    xposedMock.AssertExpectations(t)
    utilsMock.AssertExpectations(t)
}