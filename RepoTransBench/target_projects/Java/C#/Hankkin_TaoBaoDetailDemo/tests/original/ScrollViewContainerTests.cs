using Xunit;
using Hankkin.Library;

namespace Hankkin.TaoBaoDetailDemo.Original.Tests
{
    public class ScrollViewContainerTests
    {
        private object context = new object();

        [Fact]
        public void Test_ConstructorsAndInit()
        {
            var sc1 = new ScrollViewContainer(context);
            Assert.NotNull(sc1);

            var sc2 = new ScrollViewContainer(context, null);
            Assert.NotNull(sc2);

            var sc3 = new ScrollViewContainer(context, null, 0);
            Assert.NotNull(sc3);
        }
    }
}