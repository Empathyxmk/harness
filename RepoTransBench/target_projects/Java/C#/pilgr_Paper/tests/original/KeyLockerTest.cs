using System;
using System.Threading;
using System.Threading.Tasks;
using Xunit;

namespace PilgrPaper.OriginalTests
{
    public class KeyLockerTest
    {
        [Fact]
        public void TestAcquireAndRelease()
        {
            var locker = new KeyLocker();
            locker.Acquire("myKey");
            locker.Release("myKey");
        }

        [Fact]
        public void TestAcquireNullKey()
        {
            var locker = new KeyLocker();
            Assert.Throws<ArgumentException>(() => locker.Acquire(null));
        }

        [Fact]
        public void TestReleaseNullKey()
        {
            var locker = new KeyLocker();
            Assert.Throws<ArgumentException>(() => locker.Release(null));
        }

        [Fact]
        public void TestReleaseWithoutAcquire()
        {
            var locker = new KeyLocker();
            Assert.Throws<InvalidOperationException>(() => locker.Release("notAcquired"));
        }

        [Fact]
        public void TestAcquireGlobalAndReleaseGlobal()
        {
            var locker = new KeyLocker();
            locker.Acquire("a");
            locker.Acquire("b");

            var finished = false;
            var t = new Thread(() =>
            {
                locker.AcquireGlobal();
                try
                {
                    finished = true;
                }
                finally
                {
                    locker.ReleaseGlobal();
                }
            });

            t.Start();
            locker.Release("a");
            locker.Release("b");
            t.Join(2000);

            Assert.True(finished);
        }
    }
}