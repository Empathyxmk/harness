using System;
using System.Threading;
using System.Threading.Tasks;
using Xunit;

namespace OriginalTests.Lock
{
    public class RedisReentrantLockTemplateTests
    {
        [Fact(Skip="Manual Redis & concurrency test; see source for full details.")]
        public void TestTry()
        {
            /*
            var jp = new JedisPool("127.0.0.1", 6379);
            var template = new RedisDistributedLockTemplate(jp);
            int size = 100;
            var startCountDownLatch = new CountdownEvent(1);
            var endDownLatch = new CountdownEvent(size);
            for (int i = 0; i < size; ++i)
            {
                new Thread(() =>
                {
                    try { startCountDownLatch.Wait(); }
                    catch { }
                    var sleepTime = new Random().Next(5) * 1000;
                    template.Execute("test", 5000, new Callback(
                        onGetLock: () => {
                            Console.WriteLine($"{Thread.CurrentThread.Name}:getLock");
                            Thread.Sleep(sleepTime);
                            Console.WriteLine($"{Thread.CurrentThread.Name}:sleeped:{sleepTime}");
                            endDownLatch.Signal();
                            return null;
                        },
                        onTimeout: () =>
                        {
                            Console.WriteLine($"{Thread.CurrentThread.Name}:timeout");
                            endDownLatch.Signal();
                            return null;
                        }
                    ));
                }).Start();
            }
            startCountDownLatch.Signal();
            endDownLatch.Wait();
            */
        }
    }
}