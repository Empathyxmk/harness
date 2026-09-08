using Xunit;
using SignaturePad.Utils;

namespace SignaturePadTests.Original
{
    public class ControlTimedPointsTests
    {
        [Fact]
        public void TestSet()
        {
            TimedPoint c1 = new TimedPoint().Set(1, 2);
            TimedPoint c2 = new TimedPoint().Set(3, 4);
            ControlTimedPoints control = new ControlTimedPoints();
            Assert.Same(control, control.Set(c1, c2));
            Assert.Equal(c1, control.c1);
            Assert.Equal(c2, control.c2);
        }
    }
}