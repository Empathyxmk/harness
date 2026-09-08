using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Original.Java11.JavaeeRemovedBroken.Transaction
{
    public class TransactionExampleTest
    {
        [Fact]
        public void TestMainNoExceptions()
        {
            var ex = Record.Exception(() => TransactionExample.Main(new string[0]));
            Assert.Null(ex);
        }
    }
}