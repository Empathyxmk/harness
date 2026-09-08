using Moq;

namespace TestUtilities
{
    // Placeholder for reused mocks/utilities to match Java TestUtils.
    public static class TestUtils
    {
        public class InjectingApplication : ProjectName.Injector // ProjectName.Injector is assumed interface from source code
        {
            private object _objectGraph;

            public object GetObjectGraph()
            {
                return _objectGraph!;
            }

            public void Inject(object target)
            {
                // Simulate Graph injection (mocked in tests)
            }

            public void SetObjectGraph(object graph)
            {
                _objectGraph = graph;
            }
        }

        public static InjectingApplication MockInjectingApplication(object appObjectGraph)
        {
            var mock = new Mock<InjectingApplication> { CallBase = true };
            mock.Object.SetObjectGraph(appObjectGraph);
            return mock.Object;
        }
    }
}