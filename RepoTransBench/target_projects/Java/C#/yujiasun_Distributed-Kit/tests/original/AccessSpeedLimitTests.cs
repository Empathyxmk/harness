using System;
using System.Threading;
using Xunit;

namespace OriginalTests.Limit
{
    public class AccessSpeedLimitTests
    {
        [Fact(Skip="Manual test with real Redis instance. Infinite loop.")]
        public void Test1()
        {
            // This test is intentionally skipped: it runs in a loop and depends on real Redis.
            // See original Java for logic. Uncomment and remove Skip attribute to debug manually.
            /*
            var jp = new JedisPool("127.0.0.1", 6379);
            var accessSpeedLimit = new AccessSpeedLimit(jp);
            var sdf = new System.Globalization.CultureInfo("en-US").DateTimeFormat.ShortTimePattern;
            while (true)
            {
                if (accessSpeedLimit.TryAccess("10.0.0.1", 1, 5))
                {
                    Console.WriteLine("yes " + DateTime.Now.ToString(" mm:ss"));
                }
                else
                {
                    Console.WriteLine("no " + DateTime.Now.ToString(" mm:ss"));
                }
                Thread.Sleep(100);
            }
            */
        }

        [Fact(Skip="Manual test with real Redis instance. Infinite loop.")]
        public void Test2()
        {
            /*
            var jp = new JedisPool("127.0.0.1", 6379);
            var template = new RedisDistributedLockTemplate(jp);
            var limitRule = new LimitRule() { Seconds = 1, LimitCount = 5, LockCount = 7, LockTime = 2 };
            var accessSpeedLimit = new AccessSpeedLimit(jp);
            var sdf = new System.Globalization.CultureInfo("en-US").DateTimeFormat.ShortTimePattern;
            while (true)
            {
                if (accessSpeedLimit.TryAccess("10.0.0.1", limitRule))
                {
                    Console.WriteLine("yes " + DateTime.Now.ToString(" mm:ss"));
                }
                else
                {
                    Console.WriteLine("no " + DateTime.Now.ToString(" mm:ss"));
                }
                Thread.Sleep(100);
            }
            */
        }
    }
}