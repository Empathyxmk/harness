package original

import (
	"io"
	"testing"

	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/assert"
)

// Mocks for TrackerGroup, TrackerClient, TrackerServer, Connection interfaces

type TrackerGroup interface {
	GetTrackerServer() TrackerServer
	GetTrackerServerWithIdx(int) TrackerServer
	GetTrackerServers() []TrackerServer
}

type TrackerServer interface {
	GetConnection() Connection
	GetIndex() int
}

type Connection interface {
	io.Closer
}

// TrackerClient - system under test, simplified
type TrackerClient struct {
	tracker_group TrackerGroup
	errno         int
}

func NewTrackerClient(g TrackerGroup) *TrackerClient {
	return &TrackerClient{tracker_group: g, errno: 0}
}
func (tc *TrackerClient) GetErrorCode() int {
	return tc.errno
}
func (tc *TrackerClient) GetTrackerServer() TrackerServer {
	return tc.tracker_group.GetTrackerServer()
}
func (tc *TrackerClient) GetConnection(ts TrackerServer) Connection {
	if ts != nil {
		return ts.GetConnection()
	}
	servers := tc.tracker_group.GetTrackerServers()
	for _, srv := range servers {
		conn := srv.GetConnection()
		if conn != nil {
			return conn
		}
	}
	return nil
}

type MockTrackerGroup struct {
	servers []TrackerServer
	server  TrackerServer
}

func (mtg *MockTrackerGroup) GetTrackerServer() TrackerServer {
	return mtg.server
}
func (mtg *MockTrackerGroup) GetTrackerServerWithIdx(idx int) TrackerServer {
	return mtg.servers[idx]
}
func (mtg *MockTrackerGroup) GetTrackerServers() []TrackerServer {
	return mtg.servers
}

type MockTrackerServer struct {
	conn  Connection
	index int
}

func (mts *MockTrackerServer) GetConnection() Connection {
	return mts.conn
}
func (mts *MockTrackerServer) GetIndex() int {
	return mts.index
}

type MockConnection struct{}

func (mc *MockConnection) Close() error { return nil }

func TestConstructorsAndGetErrorCode(t *testing.T) {
	g := &MockTrackerGroup{}
	tc := NewTrackerClient(g)
	assert.Equal(t, g, tc.tracker_group)
	tc2 := NewTrackerClient(g)
	tc2.errno = 10
	assert.Equal(t, 10, tc2.GetErrorCode())
}

func TestGetTrackerServer(t *testing.T) {
	server := &MockTrackerServer{}
	group := &MockTrackerGroup{server: server}
	tc := NewTrackerClient(group)
	assert.Equal(t, server, tc.GetTrackerServer())
}

func TestGetConnectionSuccess(t *testing.T) {
	server := &MockTrackerServer{conn: &MockConnection{}}
	group := &MockTrackerGroup{servers: []TrackerServer{server}}
	tc := NewTrackerClient(group)
	assert.Equal(t, server.conn, tc.GetConnection(nil))
}

func TestGetConnectionWithFailover(t *testing.T) {
	server1 := &MockTrackerServer{conn: nil, index: 0}
	server2 := &MockTrackerServer{conn: &MockConnection{}, index: 1}
	group := &MockTrackerGroup{servers: []TrackerServer{server1, server2}}
	tc := NewTrackerClient(group)
	assert.Equal(t, server2.conn, tc.GetConnection(nil))
}