using Xunit;

namespace Casidiablo.MultiDex.Tests.Public
{
    public class MultiDexApplicationPublicTest
    {
        class MockContext { }
        class MyApp : MultiDexApplication
        {
            public override void AttachBaseContext(object baseContext)
            {
                base.AttachBaseContext(baseContext);
            }
        }

        [Fact]
        public void TestAttachBaseContextOverridePublic()
        {
            var app = new MyApp();
            app.AttachBaseContext(new MockContext());
            Assert.NotNull(app);
            Assert.Equal(typeof(MyApp), app.GetType());
        }
    }
}