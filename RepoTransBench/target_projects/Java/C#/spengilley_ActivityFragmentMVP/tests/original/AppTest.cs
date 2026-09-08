using Xunit;
using ActivityFragmentMVP;
using Moq;

namespace ActivityFragmentMVP.Tests.Original
{
    public class AppTest
    {
        private App app;
        private App.ObjectGraph graph;

        public AppTest()
        {
            app = new App();
            graph = new App.ObjectGraph();
        }

        [Fact]
        public void testOnTerminate()
        {
            app.onTerminate(); // just call to cover as it's empty
        }

        [Fact]
        public void testGetApplicationGraph()
        {
            app.buildObjectGraphAndInject();
            Assert.NotNull(app.getApplicationGraph());
        }

        [Fact]
        public void testInjectCallsGraph()
        {
            app.buildObjectGraphAndInject();
            object obj = new object();
            app.inject(obj);
            Assert.NotNull(app.getApplicationGraph());
        }

        [Fact]
        public void testCreateScopedGraph()
        {
            app.buildObjectGraphAndInject();
            var graph = app.createScopedGraph("mod");
            Assert.NotNull(graph);
        }
    }
}