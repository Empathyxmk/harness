using System.Threading;
using Xunit;
using SignaturePad.Utils;

namespace SignaturePadTests.Original
{
    public class TimedPointTests
    {
        [Fact]
        public void TestSet()
        {
            TimedPoint tp = new TimedPoint();
            Assert.Same(tp, tp.Set(5, 10));
            Assert.Equal(5, tp.x, 2);
            Assert.Equal(10, tp.y, 2);
        }

        [Fact]
        public void TestDistanceTo()
        {
            TimedPoint t1 = new TimedPoint().Set(0, 0);
            TimedPoint t2 = new TimedPoint().Set(3, 4);
            float dist = t1.DistanceTo(t2);
            Assert.Equal(5.0, dist, 3);
        }

        [Fact]
        public void TestVelocityFromPositiveDiff()
        {
            TimedPoint t1 = new TimedPoint().Set(0, 0);
            Thread.Sleep(2); // Small delay to ensure timestamp difference
            TimedPoint t2 = new TimedPoint().Set(3, 4);
            float velocity = t2.VelocityFrom(t1);
            Assert.True(velocity > 0);
        }

        [Fact]
        public void TestVelocityFromZeroDiff()
        {
            TimedPoint t1 = new TimedPoint().Set(0, 0);
            TimedPoint t2 = new TimedPoint();
            t2.x = 3; t2.y = 4; t2.timestamp = t1.timestamp; // same timestamp as t1
            float velocity = t2.VelocityFrom(t1);
            Assert.Equal(5.0, velocity, 3);
        }

        [Fact]
        public void TestVelocityNaNInfinite()
        {
            TimedPoint t1 = new TimedPoint();
            t1.x = t1.y = 0;
            t1.timestamp = 100;
            TimedPoint t2 = new TimedPoint();
            t2.x = t2.y = 0;
            t2.timestamp = 200;
            float velocity = t2.VelocityFrom(t1); // distance is 0 -> velocity 0
            Assert.Equal(0, velocity, 3);
        }
    }
}