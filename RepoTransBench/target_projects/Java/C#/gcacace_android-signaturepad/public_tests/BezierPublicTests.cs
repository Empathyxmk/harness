using Xunit;
using SignaturePad.Utils;

namespace SignaturePadTests.Public
{
    public class BezierPublicTests
    {
        [Fact]
        public void TestSetAndPointPublic()
        {
            TimedPoint sp = new TimedPoint().Set(2, -2);
            TimedPoint c1 = new TimedPoint().Set(4, 15);
            TimedPoint c2 = new TimedPoint().Set(20, 10);
            TimedPoint ep = new TimedPoint().Set(25, -4);
            Bezier bezier = new Bezier();
            bezier.Set(sp, c1, c2, ep);
            Assert.Equal(sp, bezier.startPoint);
            Assert.Equal(c1, bezier.control1);
            Assert.Equal(c2, bezier.control2);
            Assert.Equal(ep, bezier.endPoint);

            double pointX = bezier.Point(0.25f, 2, 4, 20, 25);
            Assert.True(pointX > 2 && pointX < 25);

            double pointY = bezier.Point(0.75f, -2, 15, 10, -4);
            Assert.True(pointY > -4 && pointY < 15);
        }

        [Fact]
        public void TestLengthDifferentStraightLine()
        {
            TimedPoint sp = new TimedPoint().Set(10, 10);
            TimedPoint c1 = new TimedPoint().Set(10, 10);
            TimedPoint c2 = new TimedPoint().Set(30, 10);
            TimedPoint ep = new TimedPoint().Set(30, 10);
            Bezier bezier = new Bezier();
            bezier.Set(sp, c1, c2, ep);
            float length = bezier.Length();
            Assert.True(length > 19 && length < 21, $"Length should be about 20, got: {length}");
        }

        [Fact]
        public void TestLengthPublicCurved()
        {
            TimedPoint sp = new TimedPoint().Set(5, 5);
            TimedPoint c1 = new TimedPoint().Set(5, 25);
            TimedPoint c2 = new TimedPoint().Set(25, 25);
            TimedPoint ep = new TimedPoint().Set(25, 5);
            Bezier bezier = new Bezier();
            bezier.Set(sp, c1, c2, ep);
            float length = bezier.Length();
            Assert.True(length > 20);
        }
    }
}