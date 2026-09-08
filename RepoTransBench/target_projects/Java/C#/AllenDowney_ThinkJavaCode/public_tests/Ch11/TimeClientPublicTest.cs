using Xunit;
using AllenDowney.ThinkJavaCode;

namespace PublicTests.Ch11
{
    public class TimeClientPublicTest
    {
        [Fact]
        public void TestCustomToStringPublic()
        {
            var t = new Time(2, 45, 30.0);
            Assert.Equal("02:45:30.0\n", t.ToString());
        }

        [Fact]
        public void TestAddAndIncrementWithDiffDataPublic()
        {
            var t1 = new Time(3, 15, 25.0);
            var t2 = new Time(4, 25, 35.0);
            var sum = Time.Add(t1, t2);
            Assert.Equal(7, sum.Hour);
            Assert.Equal(40, sum.Minute);
            Assert.Equal(60.0, sum.Second, 8);

            t1.Increment(36.5);
            Assert.Equal("03:16:01.5\n", t1.ToString());
        }
    }
}