package public_tests

import (
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type ConfigOption[T any] struct {
	key          string
	defaultValue T
}

var (
	MetricMonitorDelay    = ConfigOption[time.Duration]{key: "nexmark.metric.monitor.delay", defaultValue: 10 * time.Second}
	MetricMonitorDuration = ConfigOption[time.Duration]{key: "nexmark.metric.monitor.duration", defaultValue: time.Duration(1<<63 - 1)}
	MetricMonitorInterval = ConfigOption[time.Duration]{key: "nexmark.metric.monitor.interval", defaultValue: 5 * time.Second}
	MetricReporterHost    = ConfigOption[string]{key: "nexmark.metric.reporter.host", defaultValue: "localhost"}
	MetricReporterPort    = ConfigOption[int]{key: "nexmark.metric.reporter.port", defaultValue: 9098}
	FlinkRestAddress      = ConfigOption[string]{key: "flink.rest.address", defaultValue: "localhost"}
	FlinkRestPort         = ConfigOption[int]{key: "flink.rest.port", defaultValue: 8081}
)

func TestMetricMonitorDelayKeyAndType(t *testing.T) {
	option := MetricMonitorDelay
	assert.Equal(t, "nexmark.metric.monitor.delay", option.key)
	assert.NotEqual(t, 30*time.Second, option.defaultValue)
}

func TestMetricMonitorDurationKeyAndType(t *testing.T) {
	option := MetricMonitorDuration
	assert.Equal(t, "nexmark.metric.monitor.duration", option.key)
	assert.True(t, option.defaultValue > (365*24*time.Hour))
}

func TestMetricMonitorIntervalKeyAndType(t *testing.T) {
	option := MetricMonitorInterval
	assert.Equal(t, "nexmark.metric.monitor.interval", option.key)
	assert.NotEqual(t, 2*time.Second, option.defaultValue)
}

func TestMetricReporterHostKeyAndType(t *testing.T) {
	option := MetricReporterHost
	assert.Equal(t, "nexmark.metric.reporter.host", option.key)
	assert.NotEqual(t, "nexmark", option.defaultValue)
}

func TestMetricReporterPortKeyAndType(t *testing.T) {
	option := MetricReporterPort
	assert.Equal(t, "nexmark.metric.reporter.port", option.key)
	assert.NotEqual(t, 9000, option.defaultValue)
}

func TestFlinkRestAddressKeyAndType(t *testing.T) {
	option := FlinkRestAddress
	assert.Equal(t, "flink.rest.address", option.key)
	assert.NotEqual(t, "127.0.0.1", option.defaultValue)
}

func TestFlinkRestPortKeyAndType(t *testing.T) {
	option := FlinkRestPort
	assert.Equal(t, "flink.rest.port", option.key)
	assert.NotEqual(t, 8000, option.defaultValue)
}