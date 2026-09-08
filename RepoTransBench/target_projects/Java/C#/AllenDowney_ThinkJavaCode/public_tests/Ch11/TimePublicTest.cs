using Xunit;
using AllenDowney.ThinkJavaCode;

namespace PublicTests.Ch11
{
    public class TimePublicTest
    {
        [Fact]
        public void TestToStringAndConstructorPublic()
        {
            var t = new Time(3, 7, 15.5);
            Assert.Equal("03:07:15.5\n", t.ToString());
        }

        [Fact]
        public void TestAddStaticPublic()
        {
            var t1 = new Time(5, 10, 10.5);
            var t2 = new Time(6, 20, 50.5);
            var sum = Time.Add(t1, t2);
            Assert.Equal(11, sum.Hour);
            Assert.Equal(30, sum.Minute);
            Assert.Equal(61.0, sum.Second, 8);
        }

        [Fact]
        public void TestAddInstanceWithNoRolloverPublic()
        {
            var t1 = new Time(2, 10, 20.0);
            var t2 = new Time(2, 40, 25.0);
            var sum = t1.Add(t2);
            Assert.Equal("04:50:45.0\n", sum.ToString());
        }

        [Fact]
        public void TestIncrementSimplePublic()
        {
            var t = new Time(1, 2, 3.0);
            t.Increment(10.0);
            Assert.Equal("01:02:13.0\n", t.ToString());
        }

        [Fact]
        public void TestIncrementWithMinuteRolloverPublic()
        {
            var t = new Time(1, 59, 59.0);
            t.Increment(2.5);
            Assert.Equal("02:00:01.5\n", t.ToString());
        }
    }
}