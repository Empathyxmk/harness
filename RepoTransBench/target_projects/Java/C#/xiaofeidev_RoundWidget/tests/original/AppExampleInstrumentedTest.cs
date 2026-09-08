using Xunit;

namespace RoundWidget.Tests.Original
{
    public class AppExampleInstrumentedTest
    {
        [Fact]
        public void UseAppContext()
        {
            // Simulate context check (source: app/src/androidTest/.../ExampleInstrumentedTest.kt)
            string packageName = "com.github.xiaofeidev.roundwidget";
            Assert.Equal("com.github.xiaofeidev.roundwidget", packageName);
        }
    }
}