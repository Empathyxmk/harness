package original

import (
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// --- Mock infrastructure ---

// XposedMainMock will record arguments and allow verification.
type XposedMainMock struct {
    mock.Mock
}

func (m *XposedMainMock) Main(isZygote bool, args []string) {
    m.Called(isZygote, args)
}

// UtilsCallMainMock tracks call to CallMain.
type UtilsCallMainMock struct {
    mock.Mock
}

func (m *UtilsCallMainMock) CallMain(className string, args []string) {
    m.Called(className, args)
}

// --- SUT stub ---

// ZygoteInitMain simulates the ZygoteInit.main logic.
func ZygoteInitMain(xposed XposedMainFn, utils UtilsCallMainFn, args []string) {
    xposed(true, args)
    utils("com.android.internal.os.ZygoteInit", args)
}

// Functional types for easier test injection
type XposedMainFn func(bool, []string)
type UtilsCallMainFn func(string, []string)

// --- Test ---

func TestZygoteInitMainRunsXposedAndUtils(t *testing.T) {
    xposedMock := new(XposedMainMock)
    utilsMock := new(UtilsCallMainMock)
    args := []string{"foo"}

    xposedMock.On("Main", true, args).Return()
    utilsMock.On("CallMain", "com.android.internal.os.ZygoteInit", args).Return()

    ZygoteInitMain(xposedMock.Main, utilsMock.CallMain, args)

    xposedMock.AssertExpectations(t)
    utilsMock.AssertExpectations(t)
}