package original

import (
    "errors"
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// --- Mocks and SUT stubs ---

type LogMock struct {
    mock.Mock
}

func (l *LogMock) Warn(tag string, err error) {
    l.Called(tag, err)
}
func (l *LogMock) Debug(tag string, msg string) {
    l.Called(tag, msg)
}

type XposedMainLike struct {
    mock.Mock
}

func (x *XposedMainLike) Init(mainZygote bool) error {
    args := x.Called(mainZygote)
    if args.Get(0) != nil {
        return args.Get(0).(error)
    }
    return nil
}
func (x *XposedMainLike) Test(log *LogMock) {
    log.Debug("ArtHook.Xposed", "TEST")
}

func XposedMainImpl(xposed *XposedMainLike, log *LogMock, mainZygote bool) {
    err := xposed.Init(mainZygote)
    if err != nil {
        log.Warn("ArtHook.Xposed", err)
    }
}

func TestXposedMainCallsInitAndHandlesException(t *testing.T) {
    logMock := new(LogMock)
    xposed := new(XposedMainLike)
    xposed.On("Init", false).Return(errors.New("Fail"))
    logMock.On("Warn", "ArtHook.Xposed", mock.AnythingOfType("error")).Return()

    XposedMainImpl(xposed, logMock, false)

    xposed.AssertExpectations(t)
    logMock.AssertExpectations(t)
}

func TestXposedTestPrintsLog(t *testing.T) {
    logMock := new(LogMock)
    xposed := new(XposedMainLike)
    logMock.On("Debug", "ArtHook.Xposed", "TEST").Return()

    xposed.Test(logMock)

    logMock.AssertExpectations(t)
}