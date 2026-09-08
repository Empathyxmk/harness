using Xunit;
using Hankkin.Library;

namespace Hankkin.TaoBaoDetailDemo.Public.Tests
{
    public class StatusBarViewPublicTests
    {
        private class DummyContext { }

        [Fact]
        public void Test_ConstructorWithContext()
        {
            var ctx = new DummyContext();
            var sbv = new StatusBarView(ctx);
            Assert.NotNull(sbv);
        }

        [Fact]
        public void Test_ConstructorWithContextAndAttrs()
        {
            var ctx = new DummyContext();
            var sbv = new StatusBarView(ctx, null);
            Assert.NotNull(sbv);
        }
    }
}