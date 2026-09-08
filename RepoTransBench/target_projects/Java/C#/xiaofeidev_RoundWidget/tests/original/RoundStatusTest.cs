using Xunit;
using RoundWidget.round;

namespace RoundWidget.Tests.Original
{
    public class RoundStatusTest
    {
        [Fact]
        public void TestInterfaceIsImplemented()
        {
            RoundStatus obj = new RoundStatusImpl();
            obj.setRadius(7.2f);
            obj.setTopLeftRadius(2.2f);
            obj.setTopRightRadius(3.2f);
            obj.setBottomLeftRadius(4.2f);
            obj.setBottomRightRadius(5.2f);

            obj.fillRadius();
            _ = obj.getBottomLeftRadius();
            _ = obj.getBottomRightRadius();
            _ = obj.getRadius();
            _ = obj.getRadiusList();
            _ = obj.getTopRightRadius();
            _ = obj.getTopLeftRadius();
        }
    }
}