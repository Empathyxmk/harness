using System;
using System.Threading;
using System.Threading.Tasks;
using Xunit;

namespace OriginalTests.Lock
{
    public class ZkReentrantLockTemplateTests
    {
        [Fact(Skip="Manual concurrency test; long-running. See source for real multithreaded stress.")]
        public void TestTry()
        {
            /*
            // Concurrency logic, launches 100 threads that grab a distributed lock, sleep, and count down.
            var client = new CuratorFramework("127.0.0.1:2181", new RetryPolicy());
            client.Start();

            var template = new ZkDistributedLockTemplate(client);
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