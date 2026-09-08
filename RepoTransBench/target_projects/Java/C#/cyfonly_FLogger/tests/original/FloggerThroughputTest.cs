using System;
using System.Threading;
using System.Threading.Tasks;

namespace cyfonly_FLogger.Tests.Original
{
    public class FloggerThroughputTest
    {
        private static cyfonly_FLogger.FLogger flogger = cyfonly_FLogger.FLogger.GetInstance();

        private static string record_100_byte = "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.";   //100字节
        private static string record_200_byte = "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.";   //200字节
        private static string record_400_byte = "Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.Performance Testing.";   //400字节
        private static int messageCount = 0;
        private static int count = 1000000;
        private static int threadNum = 1;

        public static void Main(string[] args)
        {
            var latch = new CountdownEvent(threadNum);

            long st = DateTimeOffset.Now.ToUnixTimeMilliseconds();

            for (int i = 0; i < threadNum; i++)
            {
                Task.Run(() =>
                {
                    while (Interlocked.CompareExchange(ref messageCount, 0, 0) < count)
                    {
                        flogger.Info(record_400_byte);
                        Interlocked.Increment(ref messageCount);
                    }
                    latch.Signal();
                });
            }

            latch.Wait();
            long et = DateTimeOffset.Now.ToUnixTimeMilliseconds();

            Console.WriteLine($"messageCount={messageCount}, threadNum={threadNum}, costTime={et - st}ms, throughput={(1000 * messageCount / (et - st))}");
            Environment.Exit(0);
        }
    }
}