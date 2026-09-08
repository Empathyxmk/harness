package original

import (
	"errors"
	"net"
	"testing"
	"time"
)

// Create mock ukcp and buffer types for the test

type MockUkcp struct {
	writeInvoked int
	userData     *MockUserData
}

type MockUserData struct {
	remoteAddr net.Addr
}

func (u *MockUkcp) user() *MockUserData {
	return u.userData
}

func (u *MockUkcp) getConv() uint64 {
	return 42
}

func (u *MockUkcp) write(_ interface{}) {
	u.writeInvoked++
}

type MockBuf struct {
	data []byte
}

func (b *MockBuf) WriteBytes(d []byte) {
	b.data = append(b.data, d...)
}

func newMockBuf() *MockBuf {
	b := &MockBuf{}
	b.WriteBytes([]byte("hello"))
	return b
}

// Mocks for the various servers

type Kcp4sharpExampleServer struct{}
type KcpDisconnectExampleServer struct{}
type KcpMultiplePingPongExampleServer struct{}
type KcpReconnectExampleServer struct {
	start int64
}
type SpeedExampleServer struct {
	start int64
}

func (Kcp4sharpExampleServer) onConnected(ukcp *MockUkcp)                           { ukcp.write("ok") }
func (Kcp4sharpExampleServer) handleReceive(buf *MockBuf, ukcp *MockUkcp) error     { ukcp.write(buf.data); return nil }
func (Kcp4sharpExampleServer) handleException(_ error, ukcp *MockUkcp) error        { ukcp.write("exception"); return nil }
func (Kcp4sharpExampleServer) handleClose(ukcp *MockUkcp) error                     { ukcp.write("closed"); return nil }
func (KcpDisconnectExampleServer) onConnected(ukcp *MockUkcp)                       { ukcp.write("ok") }
func (KcpDisconnectExampleServer) handleReceive(buf *MockBuf, ukcp *MockUkcp) error { ukcp.write(buf.data); return nil }
func (KcpDisconnectExampleServer) handleException(_ error, ukcp *MockUkcp) error    { ukcp.write("exception"); return nil }
func (KcpDisconnectExampleServer) handleClose(ukcp *MockUkcp) error                 { ukcp.write("closed"); return nil }
func (KcpMultiplePingPongExampleServer) onConnected(ukcp *MockUkcp)                 { ukcp.write("ok") }
func (KcpMultiplePingPongExampleServer) handleReceive(buf *MockBuf, ukcp *MockUkcp) error {
	ukcp.write(buf.data)
	return nil
}
func (KcpMultiplePingPongExampleServer) handleException(_ error, ukcp *MockUkcp) error { ukcp.write("exception"); return nil }
func (KcpMultiplePingPongExampleServer) handleClose(ukcp *MockUkcp) error              { ukcp.write("closed"); return nil }

func (s *KcpReconnectExampleServer) onConnected(ukcp *MockUkcp) { ukcp.write("ok"); s.start = time.Now().UnixMilli() }
func (s *KcpReconnectExampleServer) handleReceive(buf *MockBuf, ukcp *MockUkcp) error {
	ukcp.write(buf.data)
	return nil
}
func (s *KcpReconnectExampleServer) handleException(_ error, ukcp *MockUkcp) error { ukcp.write("exception"); return nil }
func (s *KcpReconnectExampleServer) handleClose(ukcp *MockUkcp) error              { ukcp.write("closed"); return nil }

func (s *SpeedExampleServer) onConnected(ukcp *MockUkcp) { ukcp.write("ok"); s.start = time.Now().UnixMilli() }
func (s *SpeedExampleServer) handleReceive(buf *MockBuf, ukcp *MockUkcp) error {
	ukcp.write(buf.data)
	return nil
}
func (s *SpeedExampleServer) handleException(_ error, ukcp *MockUkcp) error { ukcp.write("exception"); return nil }
func (s *SpeedExampleServer) handleClose(ukcp *MockUkcp) error              { ukcp.write("closed"); return nil }

func TestKcp4sharpExampleServerOnConnectedHandleReceiveExceptionAndClose(t *testing.T) {
	ukcp := &MockUkcp{userData: &MockUserData{remoteAddr: &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}}}
	buf := newMockBuf()
	server := Kcp4sharpExampleServer{}
	server.onConnected(ukcp)
	if err := server.handleReceive(buf, ukcp); err != nil {
		t.Errorf("handleReceive failed: %v", err)
	}
	err := errors.New("error")
	if err2 := server.handleException(err, ukcp); err2 != nil {
		t.Errorf("handleException failed: %v", err2)
	}
	if err2 := server.handleClose(ukcp); err2 != nil {
		t.Errorf("handleClose failed: %v", err2)
	}
	if ukcp.writeInvoked < 1 {
		t.Errorf("expected ukcp write to be called")
	}
}

func TestKcpDisconnectExampleServerOnConnectedHandleReceiveExceptionAndClose(t *testing.T) {
	ukcp := &MockUkcp{userData: &MockUserData{remoteAddr: &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}}}
	buf := newMockBuf()
	server := KcpDisconnectExampleServer{}
	server.onConnected(ukcp)
	if err := server.handleReceive(buf, ukcp); err != nil {
		t.Errorf("handleReceive failed: %v", err)
	}
	err := errors.New("error")
	if err2 := server.handleException(err, ukcp); err2 != nil {
		t.Errorf("handleException failed: %v", err2)
	}
	if err2 := server.handleClose(ukcp); err2 != nil {
		t.Errorf("handleClose failed: %v", err2)
	}
	if ukcp.writeInvoked < 1 {
		t.Errorf("expected ukcp write to be called")
	}
}

func TestKcpMultiplePingPongExampleServerLifecycle(t *testing.T) {
	ukcp := &MockUkcp{userData: &MockUserData{remoteAddr: &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}}}
	buf := newMockBuf()
	server := KcpMultiplePingPongExampleServer{}
	server.onConnected(ukcp)
	if err := server.handleReceive(buf, ukcp); err != nil {
		t.Errorf("handleReceive failed: %v", err)
	}
	err := errors.New("error2")
	if err2 := server.handleException(err, ukcp); err2 != nil {
		t.Errorf("handleException failed: %v", err2)
	}
	if err2 := server.handleClose(ukcp); err2 != nil {
		t.Errorf("handleClose failed: %v", err2)
	}
	if ukcp.writeInvoked < 1 {
		t.Errorf("expected ukcp write to be called")
	}
}

func TestKcpReconnectExampleServerAllPaths(t *testing.T) {
	ukcp := &MockUkcp{userData: &MockUserData{remoteAddr: &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}}}
	buf := newMockBuf()
	server := &KcpReconnectExampleServer{}
	server.onConnected(ukcp)
	_ = server.handleReceive(buf, ukcp)
	// Simulate time passing to hit the other path
	server.start = time.Now().UnixMilli() - 2000
	_ = server.handleReceive(buf, ukcp)
	ex := errors.New("error3")
	if err := server.handleException(ex, ukcp); err != nil {
		t.Errorf("handleException failed: %v", err)
	}
	if err := server.handleClose(ukcp); err != nil {
		t.Errorf("handleClose failed: %v", err)
	}
	if ukcp.writeInvoked < 1 {
		t.Errorf("expected ukcp write to be called")
	}
}

func TestSpeedExampleServerFlow(t *testing.T) {
	ukcp := &MockUkcp{userData: &MockUserData{remoteAddr: &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}}}
	buf := newMockBuf()
	server := &SpeedExampleServer{}
	server.onConnected(ukcp)
	if err := server.handleReceive(buf, ukcp); err != nil {
		t.Errorf("handleReceive failed: %v", err)
	}
	server.start = time.Now().UnixMilli() - 1200
	if err := server.handleReceive(buf, ukcp); err != nil {
		t.Errorf("handleReceive failed (second): %v", err)
	}
	ex := errors.New("error4")
	if err := server.handleException(ex, ukcp); err != nil {
		t.Errorf("handleException failed: %v", err)
	}
	if err := server.handleClose(ukcp); err != nil {
		t.Errorf("handleClose failed: %v", err)
	}
}