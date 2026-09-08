using System;
using Xunit;
using NexmarkFlink.metric.cpu;

namespace OriginalTests.metric
{
    public class CpuMetricSenderTests
    {
        [Fact(Skip = "Relies on runtime environment, ignored by default")]
        public void TestGetTaskManagerPid()
        {
            var result = CpuMetricSender.GetTaskManagerPidList();
            Console.WriteLine(result);
        }
    }
}