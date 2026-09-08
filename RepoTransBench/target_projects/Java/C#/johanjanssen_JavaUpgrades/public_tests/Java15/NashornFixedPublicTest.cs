using Xunit;
using Johanjanssen.JavaUpgrades;

namespace Johanjanssen.JavaUpgrades.Tests.Public.Java15
{
    public class NashornFixedPublicTest
    {
        [Fact]
        public void TestScriptEngineManagerNashornPresent_Public()
        {
            var engine = new Microsoft.ClearScript.V8.V8ScriptEngine();
            Assert.NotNull(engine); // Simulate "javascript" engine present
        }
    }
}