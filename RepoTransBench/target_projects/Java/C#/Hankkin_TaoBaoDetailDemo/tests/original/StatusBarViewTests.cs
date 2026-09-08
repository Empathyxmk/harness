using Xunit;
using Hankkin.Library;

namespace Hankkin.TaoBaoDetailDemo.Original.Tests
{
    public class StatusBarViewTests
    {
        [Fact]
        public void Test_Constructors()
        {
            var context = new object();
            var sbv1 = new StatusBarView(context);
            Assert.NotNull(sbv1);

            var sbv2 = new StatusBarView(context, null);
            Assert.NotNull(sbv2);
        }
    }
}