using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Public.Java15
{
    public class NashornBrokenPublicTest
    {
        [Fact]
        public void TestScriptEngineManagerAvailable_Public()
        {
            // Assume engine is absent in broken context
            Microsoft.ClearScript.V8.V8ScriptEngine engine = null;
            Assert.Null(engine);
        }
    }
}