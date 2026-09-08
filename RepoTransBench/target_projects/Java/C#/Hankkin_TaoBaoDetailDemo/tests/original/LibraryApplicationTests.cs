using Xunit;

namespace Hankkin.TaoBaoDetailDemo.Original.Tests
{
    public class LibraryApplicationTests
    {
        [Fact]
        public void LibraryApplicationTest_ConstructorWorks()
        {
            // Just ensure construction does not throw
            var app = new object();
            Assert.NotNull(app);
        }
    }
}