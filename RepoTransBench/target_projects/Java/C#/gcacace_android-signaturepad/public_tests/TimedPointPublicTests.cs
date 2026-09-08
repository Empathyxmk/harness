using System.Threading;
using Xunit;
using SignaturePad.Utils;

namespace SignaturePadTests.Public
{
    public class TimedPointPublicTests
    {
        [Fact]
        public void TestSetPublic()
        {
            TimedPoint tp = new TimedPoint();
            Assert.Same(tp, tp.Set(-7.2, 8.19));
            Assert.Equal(-7.2, tp.x, 2);
            Assert.Equal(8.19, tp.y, 2);
        }

        [Fact]
        public void TestDistanceToPublic()
        {
            TimedPoint t1 = new TimedPoint().Set(1, 1);
            TimedPoint t2 = new TimedPoint().Set(4, 5);
            float dist = t1.DistanceTo(t2);
            Assert.Equal(5.0, dist, 3);
        }

        [Fact]
        public void TestVelocityFromPositiveDiffPublic()
        {
            TimedPoint t1 = new TimedPoint().Set(2, 3);
            Thread.Sleep(2); // Small delay to ensure timestamp difference
            TimedPoint t2 = new TimedPoint().Set(7, 11);
            float velocity = t2.VelocityFrom(t1);
            Assert.True(velocity > 0);
        }

        [Fact]
        public void TestVelocityFromZeroDiffPublic()
        {
            TimedPoint t1 = new TimedPoint().Set(3, 4);
            TimedPoint t2 = new TimedPoint();
            t2.x = 6; t2.y = 8; t2.timestamp = t1.timestamp; // same timestamp as t1
            float velocity = t2.VelocityFrom(t1);
            Assert.Equal(5.0, velocity, 3);
        }

        [Fact]
        public void TestVelocityNaNInfinitePublic()
        {
            TimedPoint t1 = new TimedPoint();
            t1.x = t1.y = 10;
            t1.timestamp = 500;
            TimedPoint t2 = new TimedPoint();
            t2.x = t2.y = 10;
            t2.timestamp = 600;
            float velocity = t2.VelocityFrom(t1); // distance is 0 -> velocity 0
            Assert.Equal(0, velocity, 3);
        }
    }
}