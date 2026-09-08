package public_tests

import (
    "testing"

    "github.com/stretchr/testify/mock"
)

// Mimic the public test with different args

type ZygoteInitXposedPublicMock struct {
    mock.Mock
}
type ZygoteInitUtilsPublicMock struct {
    mock.Mock
}

func (m *ZygoteInitXposedPublicMock) Main(isZygote bool, args []string) {
    m.Called(isZygote, args)
}

func (m *ZygoteInitUtilsPublicMock) CallMain(className string, args []string) {
    m.Called(className, args)
}

func ZygoteInitMainPublic(xposed func(bool, []string), utils func(string, []string), args []string) {
    xposed(true, args)
    utils("com.android.internal.os.ZygoteInit", args)
}

func TestMainRunsXposedAndUtilsWithDifferentArgs(t *testing.T) {
    xposedMock := new(ZygoteInitXposedPublicMock)
    utilsMock := new(ZygoteInitUtilsPublicMock)
    args := []string{"bar", "baz"}

    xposedMock.On("Main", true, args).Return()
    utilsMock.On("CallMain", "com.android.internal.os.ZygoteInit", args).Return()

    ZygoteInitMainPublic(xposedMock.Main, utilsMock.CallMain, args)

    xposedMock.AssertExpectations(t)
    utilsMock.AssertExpectations(t)
}