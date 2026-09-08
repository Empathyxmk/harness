using Xunit;
using SignaturePad.Utils;

namespace SignaturePadTests.Original
{
    public class BezierTests
    {
        [Fact]
        public void TestSetAndPoint()
        {
            TimedPoint sp = new TimedPoint().Set(0, 0);
            TimedPoint c1 = new TimedPoint().Set(5, 5);
            TimedPoint c2 = new TimedPoint().Set(10, 5);
            TimedPoint ep = new TimedPoint().Set(10, 0);
            Bezier bezier = new Bezier();
            bezier.Set(sp, c1, c2, ep);
            Assert.Equal(sp, bezier.startPoint);
            Assert.Equal(c1, bezier.control1);
            Assert.Equal(c2, bezier.control2);
            Assert.Equal(ep, bezier.endPoint);

            double pointX = bezier.Point(0.5f, 0, 5, 10, 10);
            Assert.True(pointX > 0);
            Assert.True(pointX < 10);

            double pointY = bezier.Point(0.5f, 0, 5, 5, 0);
            Assert.True(pointY >= 0 && pointY <= 5);
        }

        [Fact]
        public void TestLengthStraightLine()
        {
            TimedPoint sp = new TimedPoint().Set(0, 0);
            TimedPoint c1 = new TimedPoint().Set(0, 0);
            TimedPoint c2 = new TimedPoint().Set(10, 0);
            TimedPoint ep = new TimedPoint().Set(10, 0);
            Bezier bezier = new Bezier();
            bezier.Set(sp, c1, c2, ep);
            float length = bezier.Length();
            Assert.True(length > 9 && length < 11, $"Length should be about 10, got: {length}");
        }

        [Fact]
        public void TestLengthCurved()
        {
            TimedPoint sp = new TimedPoint().Set(0, 0);
            TimedPoint c1 = new TimedPoint().Set(0, 10);
            TimedPoint c2 = new TimedPoint().Set(10, 10);
            TimedPoint ep = new TimedPoint().Set(10, 0);
            Bezier bezier = new Bezier();
            bezier.Set(sp, c1, c2, ep);
            float length = bezier.Length();
            Assert.True(length > 10);
        }
    }
}