using Xunit;
using RoundWidget.round;

namespace RoundWidget.Tests.Public
{
    public class RoundStatusImplBuilderPublicTest
    {
        [Fact]
        public void TestBuilderSetsValues_Public()
        {
            var builder = new RoundStatusImpl.RoundStatusBuilder();
            builder.setMRadius(20.21f)
                .setMTopLeftRadius(22.22f)
                .setMTopRightRadius(23.23f)
                .setMBottomRightRadius(24.24f)
                .setMBottomLeftRadius(25.25f);

            var impl = builder.build();
            Assert.Equal(20.21f, impl.getRadius(), 4);
            Assert.Equal(22.22f, impl.getTopLeftRadius(), 4);
            Assert.Equal(23.23f, impl.getTopRightRadius(), 4);
            Assert.Equal(24.24f, impl.getBottomRightRadius(), 4);
            Assert.Equal(25.25f, impl.getBottomLeftRadius(), 4);
        }
    }
}