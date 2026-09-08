using Xunit;
using AllenDowney.ThinkJavaCode;

namespace OriginalTests.Ch11
{
    public class TimeTest
    {
        [Fact]
        public void TestDefaultConstructor()
        {
            var t = new Time();
            Assert.Equal("00:00:00.0\n", t.ToString());
        }

        [Fact]
        public void TestParameterizedConstructorAndToString()
        {
            var t = new Time(9, 15, 7.7);
            Assert.Equal("09:15:07.7\n", t.ToString());
        }

        [Fact]
        public void TestEqualsTrueAndFalse()
        {
            var t1 = new Time(2, 5, 10.0);
            var t2 = new Time(2, 5, 10.0);
            var t3 = new Time(3, 5, 10.0);
            Assert.True(t1.Equals(t2));
            Assert.False(t1.Equals(t3));
        }

        [Fact]
        public void TestAddStatic()
        {
            var t1 = new Time(1, 20, 30.0);
            var t2 = new Time(2, 40, 15.5);
            var sum = Time.Add(t1, t2);
            Assert.Equal("03:60:45.5\n", sum.ToString());
        }

        [Fact]
        public void TestAddInstanceNoRollover()
        {
            var t1 = new Time(1, 20, 10.0);
            var t2 = new Time(2, 10, 30.0);
            var sum = t1.Add(t2);
            Assert.Equal("03:30:40.0\n", sum.ToString());
        }

        [Fact]
        public void TestAddInstanceWithSecondRollover()
        {
            var t1 = new Time(1, 50, 40.0);
            var t2 = new Time(0, 5, 25.0);
            var sum = t1.Add(t2);
            Assert.Equal("01:56:05.0\n", sum.ToString());
        }

        [Fact]
        public void TestAddInstanceWithMinuteRollover()
        {
            var t1 = new Time(1, 55, 50.0);
            var t2 = new Time(0, 6, 15.0);
            var sum = t1.Add(t2);
            Assert.Equal("02:02:05.0\n", sum.ToString());
        }

        [Fact]
        public void TestIncrementNoRollover()
        {
            var t = new Time(2, 15, 50.0);
            t.Increment(5.5);
            Assert.Equal("02:15:55.5\n", t.ToString());
        }

        [Fact]
        public void TestIncrementSecondsToMinuteRollover()
        {
            var t = new Time(0, 44, 50.0);
            t.Increment(14.0);
            Assert.Equal("00:45:04.0\n", t.ToString());
        }

        [Fact]
        public void TestIncrementSecondsAndMinuteRollover()
        {
            var t = new Time(1, 59, 55.0);
            t.Increment(10.0);
            Assert.Equal("02:00:05.0\n", t.ToString());
        }
    }
}