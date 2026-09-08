using Xunit;

namespace ProjectName.PublicTests.Processor
{
    public class CompilePublicTest
    {
        public enum ColorPublic { RED, GREEN, BLUE }

        [Fact]
        public void SimpleCompileTest_PublicVariant()
        {
            Assert.Equal(ColorPublic.GREEN, Enum.Parse<ColorPublic>("GREEN"));
        }
    }
}