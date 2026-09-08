package public_tests

import (
	"io"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Mocks for TrackerGroup, TrackerClient, TrackerServer, Connection interfaces (public versions)

type TrackerGroupPublic interface {
	GetTrackerServer() TrackerServerPublic
	GetTrackerServerWithIdx(int) TrackerServerPublic
	GetTrackerServers() []TrackerServerPublic
}

type TrackerServerPublic interface {
	GetConnection() ConnectionPublic
	GetIndex() int
}

type ConnectionPublic interface {
	io.Closer
}

type TrackerClientPublic struct {
	tracker_group TrackerGroupPublic
	errno         int
}

func NewTrackerClientPublic(g TrackerGroupPublic) *TrackerClientPublic {
	return &TrackerClientPublic{tracker_group: g, errno: 0}
}
func (tc *TrackerClientPublic) GetErrorCode() int {
	return tc.errno
}
func (tc *TrackerClientPublic) GetTrackerServer() TrackerServerPublic {
	return tc.tracker_group.GetTrackerServer()
}
func (tc *TrackerClientPublic) GetConnection(ts TrackerServerPublic) ConnectionPublic {
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

type MockTrackerGroupPublic struct {
	servers []TrackerServerPublic
	server  TrackerServerPublic
}

func (mtg *MockTrackerGroupPublic) GetTrackerServer() TrackerServerPublic {
	return mtg.server
}
func (mtg *MockTrackerGroupPublic) GetTrackerServerWithIdx(idx int) TrackerServerPublic {
	return mtg.servers[idx]
}
func (mtg *MockTrackerGroupPublic) GetTrackerServers() []TrackerServerPublic {
	return mtg.servers
}

type MockTrackerServerPublic struct {
	conn  ConnectionPublic
	index int
}

func (mts *MockTrackerServerPublic) GetConnection() ConnectionPublic {
	return mts.conn
}
func (mts *MockTrackerServerPublic) GetIndex() int {
	return mts.index
}

type MockConnectionPublic struct{}

func (mc *MockConnectionPublic) Close() error { return nil }

func TestConstructorsAndGetErrorCodePublic(t *testing.T) {
	g := &MockTrackerGroupPublic{}
	tc := NewTrackerClientPublic(g)
	assert.Equal(t, g, tc.tracker_group)
	tc2 := NewTrackerClientPublic(g)
	tc2.errno = 10
	assert.Equal(t, 10, tc2.GetErrorCode())
}

func TestGetTrackerServerPublic(t *testing.T) {
	server := &MockTrackerServerPublic{}
	group := &MockTrackerGroupPublic{server: server}
	tc := NewTrackerClientPublic(group)
	assert.Equal(t, server, tc.GetTrackerServer())
}

func TestGetConnectionFailoverPublic(t *testing.T) {
	server1 := &MockTrackerServerPublic{conn: nil, index: 0}
	server2 := &MockTrackerServerPublic{conn: &MockConnectionPublic{}, index: 1}
	group := &MockTrackerGroupPublic{servers: []TrackerServerPublic{server1, server2}}
	tc := NewTrackerClientPublic(group)
	assert.Equal(t, server2.conn, tc.GetConnection(nil))
}