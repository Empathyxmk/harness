using Xunit;
using Johanjanssen.JavaUpgrades;

namespace OriginalTests.Java11.JavaeeRemovedBroken.WS
{
    public class WSExampleTest
    {
        [Fact]
        public void Call_ShouldReturnResult()
        {
            var ws = new WSExample();
            var result = ws.Call();
            Assert.Equal("Result!", result);
        }

        [Fact]
        public void Main_ShouldExecuteWithoutException()
        {
            // Covers static Main(string[]) and expects no throw
            var args = new string[] { };
            WSExample.Main(args);
        }
    }
}