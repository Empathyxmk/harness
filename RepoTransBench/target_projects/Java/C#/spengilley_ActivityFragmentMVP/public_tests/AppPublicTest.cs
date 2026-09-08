using Xunit;
using ActivityFragmentMVP;

namespace ActivityFragmentMVP.Tests.Public
{
    public class AppPublicTest
    {
        private App app;

        public AppPublicTest()
        {
            app = new App();
        }

        [Fact]
        public void testOnTerminate_MultipleCalls()
        {
            app.onTerminate();
            app.onTerminate(); // call multiple times for coverage
        }

        [Fact]
        public void testBuildObjectGraphAndInjectMultipleTimes()
        {
            app.buildObjectGraphAndInject();
            app.buildObjectGraphAndInject();
            Assert.NotNull(app.getApplicationGraph());
        }

        [Fact]
        public void testInjectWithStringObject()
        {
            app.buildObjectGraphAndInject();
            string someObj = "HelloPublic";
            app.inject(someObj);
            Assert.NotNull(app.getApplicationGraph());
        }

        [Fact]
        public void testCreateScopedGraphWithLongerName()
        {
            app.buildObjectGraphAndInject();
            var scoped = app.createScopedGraph("publicModExtra");
            Assert.NotNull(scoped);
        }
    }
}