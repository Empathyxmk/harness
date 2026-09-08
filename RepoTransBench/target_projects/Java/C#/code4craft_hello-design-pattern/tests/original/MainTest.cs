using Xunit;

namespace HelloDesignPattern.Tests
{
    public class MainTest
    {
        [Fact]
        public void TestMain()
        {
            // C# Program.Main() expects string[] args
            // The test is for coverage, so just call without assert
            Program.Main(new string[] { });
        }
    }
}