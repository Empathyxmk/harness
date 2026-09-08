package public_tests

import (
    "errors"
    "testing"

    "github.com/stretchr/testify/mock"
)

// --- Mocks ---

type LogPublicMock struct {
    mock.Mock
}

func (l *LogPublicMock) Warn(tag string, err error) {
    l.Called(tag, err)
}
func (l *LogPublicMock) Debug(tag string, msg string) {
    l.Called(tag, msg)
}

type XposedPublicMainLike struct {
    mock.Mock
}

func (x *XposedPublicMainLike) Init(mainZygote bool) error {
    args := x.Called(mainZygote)
    if args.Get(0) != nil {
        return args.Get(0).(error)
    }
    return nil
}
func (x *XposedPublicMainLike) Test(log *LogPublicMock) {
    log.Debug("ArtHook.Xposed", "TEST")
}

func XposedMainImplPublic(xposed *XposedPublicMainLike, log *LogPublicMock, mainZygote bool) {
    err := xposed.Init(mainZygote)
    if err != nil {
        log.Warn("ArtHook.Xposed", err)
    }
}

func TestMainCallsInitAndHandlesDifferentException(t *testing.T) {
    // Simulate throwing a different error and ensure correct logging
    logMock := new(LogPublicMock)
    xposed := new(XposedPublicMainLike)
    xposed.On("Init", true).Return(errors.New("Different fail"))
    logMock.On("Warn", "ArtHook.Xposed", mock.AnythingOfType("error")).Return()

    XposedMainImplPublic(xposed, logMock, true)

    xposed.AssertExpectations(t)
    logMock.AssertExpectations(t)
}

func TestTestPrintsLogWithDifferentVerification(t *testing.T) {
    logMock := new(LogPublicMock)
    xposed := new(XposedPublicMainLike)
    logMock.On("Debug", "ArtHook.Xposed", "TEST").Return().Times(1) // atLeastOnce equivalent is >=1

    xposed.Test(logMock)

    logMock.AssertExpectations(t)
}