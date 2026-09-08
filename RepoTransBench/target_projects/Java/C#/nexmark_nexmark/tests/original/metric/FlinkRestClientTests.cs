using System;
using Xunit;
using NexmarkFlink.metric;
using NexmarkFlink.metric.tps;

namespace OriginalTests.metric
{
    public class FlinkRestClientTests
    {
        [Fact(Skip = "Client-side integration test, ignored by default")]
        public void TestMetricsClient()
        {
            var client = new FlinkRestClient("localhost", 8081);
            var jobId = client.GetCurrentJobId();
            Console.WriteLine("jobId: " + jobId);

            var vertexId = client.GetSourceVertexId(jobId);
            Console.WriteLine("vertexId: " + vertexId);

            var metricName = client.GetTpsMetricName(jobId, vertexId);
            Console.WriteLine("metricName: " + metricName);

            TpsMetric tps = client.GetTpsMetric(jobId, vertexId, metricName);
            Console.WriteLine("tps: " + tps);
        }

        [Fact(Skip = "Job cancellation and Flink API call, ignored by default")]
        public void TestCancelJob()
        {
            var client = new FlinkRestClient("localhost", 8081);
            var jobId = client.GetCurrentJobId();
            Console.WriteLine("jobId: " + jobId);
            client.CancelJob(jobId);
        }
    }
}