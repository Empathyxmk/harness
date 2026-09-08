using Xunit;
using RoundWidget.round;

namespace RoundWidget.Tests.Original
{
    public class RoundStatusImplBuilderTest
    {
        [Fact]
        public void TestBuilderChain()
        {
            var builder = new RoundStatusImpl.RoundStatusBuilder();
            builder.setMRadius(9f)
                   .setMTopLeftRadius(8f)
                   .setMTopRightRadius(7f)
                   .setMBottomLeftRadius(6f)
                   .setMBottomRightRadius(5f);

            var impl = builder.build();
            Assert.Equal(9f, impl.getRadius(), 5);
            Assert.Equal(8f, impl.getTopLeftRadius(), 5);
            Assert.Equal(7f, impl.getTopRightRadius(), 5);
            Assert.Equal(6f, impl.getBottomLeftRadius(), 5);
            Assert.Equal(5f, impl.getBottomRightRadius(), 5);
        }
    }
}