using System.Collections.Generic;
using System.Text.RegularExpressions;
using Xunit;

namespace Ikkisoft.SerialKiller.PublicTests
{
    public class PatternListPublicTest
    {
        [Fact]
        public void TestPatternMatchingWithNewPattern()
        {
            var patterns = new List<Regex>
            {
                new Regex(@"^PUBLIC_\d+$"),
                new Regex(@"TestCase.*")
            };

            string value1 = "PUBLIC_1234";
            string value2 = "TestCasePublic";
            string value3 = "NotMatching";

            Assert.True(patterns[0].IsMatch(value1));
            Assert.False(patterns[0].IsMatch(value2));

            Assert.True(patterns[1].IsMatch(value2));
            Assert.False(patterns[1].IsMatch(value3));
        }
    }
}