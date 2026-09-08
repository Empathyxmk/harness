using System;
using Xunit;

namespace PilgrPaper.OriginalTests
{
    public class PaperTableTest
    {
        [Fact]
        public void TestDefaultConstructor()
        {
            var pt = new PaperTable<string>();
            Assert.Null(pt.Content);
        }

        [Fact]
        public void TestConstructorWithContent()
        {
            var pt = new PaperTable<int>(100);
            Assert.Equal(100, pt.Content);
        }
    }
}