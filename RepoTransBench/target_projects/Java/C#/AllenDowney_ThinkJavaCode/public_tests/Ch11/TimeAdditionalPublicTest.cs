using Xunit;
using AllenDowney.ThinkJavaCode;

namespace PublicTests.Ch11
{
    public class TimeAdditionalPublicTest
    {
        [Fact]
        public void TestTimeToSecondsAndConversion()
        {
            var t = new Time(6, 4, 15.0);
            double seconds = Time.TimeToSeconds(t);
            Assert.Equal(6 * 3600 + 4 * 60 + 15.0, seconds, 8);

            var t2 = Time.SecondsToTime(3678.5);
            Assert.Equal(1, t2.Hour);
            Assert.Equal(1, t2.Minute);
            Assert.Equal(18.5, t2.Second, 8);
        }

        [Fact]
        public void TestSubtractTime()
        {
            var t1 = new Time(7, 10, 15.0);
            var t2 = new Time(4, 20, 15.0);
            var diff = Time.Subtract(t1, t2);
            Assert.Equal(2, diff.Hour);
            Assert.Equal(50, diff.Minute);
            Assert.Equal(0.0, diff.Second, 8);
        }
    }
}