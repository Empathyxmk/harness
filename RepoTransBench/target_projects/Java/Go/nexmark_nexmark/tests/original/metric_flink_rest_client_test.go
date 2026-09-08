package original

import (
	"fmt"
	"testing"
)

type FlinkRestClient struct {
	address string
	port    int
}

func NewFlinkRestClient(host string, port int) *FlinkRestClient {
	return &FlinkRestClient{address: host, port: port}
}

func (c *FlinkRestClient) GetCurrentJobId() string    { return "jobid123" }
func (c *FlinkRestClient) GetSourceVertexId(jobId string) string {
	return "vertexid"
}
func (c *FlinkRestClient) GetTpsMetricName(jobId, vertexId string) string {
	return "tps-metric-name"
}
func (c *FlinkRestClient) GetTpsMetric(jobId, vertexId, metricName string) TpsMetric {
	return TpsMetric{id: "id", min: 1, max: 2, avg: 1.5, sum: 3}
}
func (c *FlinkRestClient) CancelJob(jobId string) {}

type TpsMetric struct {
	id      string
	min     float64
	max     float64
	avg     float64
	sum     float64
}

func TestMetricsClient(t *testing.T) {
	client := NewFlinkRestClient("localhost", 8081)
	jobId := client.GetCurrentJobId()
	fmt.Println("jobId:", jobId)

	vertexId := client.GetSourceVertexId(jobId)
	fmt.Println("vertexId:", vertexId)

	metricName := client.GetTpsMetricName(jobId, vertexId)
	fmt.Println("metricName:", metricName)

	tps := client.GetTpsMetric(jobId, vertexId, metricName)
	fmt.Println("tps:", tps)
}

func TestCancelJob(t *testing.T) {
	client := NewFlinkRestClient("localhost", 8081)
	jobId := client.GetCurrentJobId()
	fmt.Println("jobId:", jobId)
	client.CancelJob(jobId)
}