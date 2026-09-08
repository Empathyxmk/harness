using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Original.Java11.JavaeeRemovedBroken.Annotation
{
    public class AnnotationExampleTest
    {
        [Fact]
        public void TestMainNoExceptions()
        {
            var ex = Record.Exception(() => AnnotationExample.Main(new string[0]));
            Assert.Null(ex);
        }
    }
}