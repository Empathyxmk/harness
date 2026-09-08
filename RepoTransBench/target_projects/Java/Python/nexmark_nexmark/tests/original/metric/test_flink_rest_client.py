import pytest

class TpsMetric:
    def __init__(self, job_id, vertex_id, metric_name):
        self.job_id = job_id
        self.vertex_id = vertex_id
        self.metric_name = metric_name
    def __str__(self):
        return f"TpsMetric({self.job_id}, {self.vertex_id}, {self.metric_name})"

class FlinkRestClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def getCurrentJobId(self):
        return "mock-job-id"
    def getSourceVertexId(self, job_id):
        return "mock-vertex-id"
    def getTpsMetricName(self, job_id, vertex_id):
        return "mock-tps-metric-name"
    def getTpsMetric(self, job_id, vertex_id, metric_name):
        return TpsMetric(job_id, vertex_id, metric_name)
    def cancelJob(self, job_id):
        return "cancelled"

def test_metrics_client(capsys):
    client = FlinkRestClient("localhost", 8081)
    job_id = client.getCurrentJobId()
    print("jobId:", job_id)

    vertex_id = client.getSourceVertexId(job_id)
    print("vertexId:", vertex_id)

    metric_name = client.getTpsMetricName(job_id, vertex_id)
    print("metricName:", metric_name)

    tps = client.getTpsMetric(job_id, vertex_id, metric_name)
    print("tps:", tps)
    captured = capsys.readouterr()
    assert "jobId: mock-job-id" in captured.out
    assert "vertexId: mock-vertex-id" in captured.out
    assert "metricName: mock-tps-metric-name" in captured.out
    assert "tps: TpsMetric(" in captured.out

def test_cancel_job(capsys):
    client = FlinkRestClient("localhost", 8081)
    job_id = client.getCurrentJobId()
    print("jobId:", job_id)
    result = client.cancelJob(job_id)
    assert result == "cancelled"