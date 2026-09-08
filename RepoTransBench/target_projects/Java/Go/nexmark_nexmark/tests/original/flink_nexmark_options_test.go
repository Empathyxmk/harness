package original

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

func TestMetricMonitorDelayDefaults(t *testing.T) {
	option := MetricMonitorDelay
	assert.Equal(t, "nexmark.metric.monitor.delay", option.key)
	assert.Equal(t, 10*time.Second, option.defaultValue)
}

func TestMetricMonitorDurationDefaults(t *testing.T) {
	option := MetricMonitorDuration
	assert.Equal(t, "nexmark.metric.monitor.duration", option.key)
	assert.Equal(t, time.Duration(1<<63-1), option.defaultValue)
}

func TestMetricMonitorIntervalDefaults(t *testing.T) {
	option := MetricMonitorInterval
	assert.Equal(t, "nexmark.metric.monitor.interval", option.key)
	assert.Equal(t, 5*time.Second, option.defaultValue)
}

func TestMetricReporterHostDefaults(t *testing.T) {
	option := MetricReporterHost
	assert.Equal(t, "nexmark.metric.reporter.host", option.key)
	assert.Equal(t, "localhost", option.defaultValue)
}

func TestMetricReporterPortDefaults(t *testing.T) {
	option := MetricReporterPort
	assert.Equal(t, "nexmark.metric.reporter.port", option.key)
	assert.Equal(t, 9098, option.defaultValue)
}

func TestFlinkRestAddressDefaults(t *testing.T) {
	option := FlinkRestAddress
	assert.Equal(t, "flink.rest.address", option.key)
	assert.Equal(t, "localhost", option.defaultValue)
}

func TestFlinkRestPortDefaults(t *testing.T) {
	option := FlinkRestPort
	assert.Equal(t, "flink.rest.port", option.key)
	assert.Equal(t, 8081, option.defaultValue)
}