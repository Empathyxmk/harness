using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Original.Java11.JavaeeRemovedBroken.Activation
{
    public class ActivationExampleTest
    {
        [Fact]
        public void TestMainNoExceptions()
        {
            var ex = Record.Exception(() => ActivationExample.Main(new string[0]));
            Assert.Null(ex);
        }
    }
}