using Xunit;

namespace ElemeAmigo.PublicTests
{
    public class ExamplePublicSanityTests
    {
        [Fact]
        public void String_Concatenation_Works()
        {
            Assert.Equal("hello world", "hello " + "world");
        }
    }
}