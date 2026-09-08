using System.Collections.Generic;
using Moq;
using Xunit;
using ProjectName;
using TestUtilities;

namespace OriginalTests
{
    public class InjectingActionBarActivityTest
    {
        private Mock<object> _mockAppObjectGraph;
        private Mock<object> _mockActivityObjectGraph;
        private Mock<Bundle> _mockBundle;
        private TestUtilities.TestUtils.InjectingApplication _mockInjectingApplication;
        private Mock<InjectingActionBarActivity> _activity;

        public InjectingActionBarActivityTest()
        {
            _mockAppObjectGraph = new Mock<object>();
            _mockActivityObjectGraph = new Mock<object>();
            _mockBundle = new Mock<Bundle>();
            _mockInjectingApplication = new TestUtilities.TestUtils.InjectingApplication();
            _mockInjectingApplication.SetObjectGraph(_mockAppObjectGraph.Object);
            _activity = new Mock<InjectingActionBarActivity> { CallBase = true };

            // simulate GetApplication returns our injecting app
            _activity.Setup(a => a.GetApplication()).Returns(_mockInjectingApplication);

            // simulate Plus and Inject
            // Dynamic simulated Plus: return mockActivityObjectGraph
            // .Inject does not throw
            // assume GetObjectGraph/setObjectGraph methods exist

            _mockAppObjectGraph.Setup(g => g.GetType().GetMethod("Plus") != null 
                ? ((dynamic)g.Object).Plus(It.IsAny<object[]>()) : null
            ).Returns(_mockActivityObjectGraph.Object);

            var modules = new List<object> { new InjectingActivityModule(_activity.Object, _activity.Object) };
            _activity.Setup(a => a.GetModules()).Returns(modules);
        }

        [Fact]
        public void TestOnCreate()
        {
            Assert.Null(_activity.Object.GetObjectGraph());
            _activity.Object.OnCreate(_mockBundle.Object);

            Assert.NotNull(_activity.Object.GetObjectGraph());
            Assert.Equal(_mockActivityObjectGraph.Object, _activity.Object.GetObjectGraph());
        }

        [Fact]
        public void TestOnDestroy()
        {
            _activity.Object.OnCreate(_mockBundle.Object);
            Assert.NotNull(_activity.Object.GetObjectGraph());

            _activity.Object.OnDestroy();

            Assert.Null(_activity.Object.GetObjectGraph());
        }

        [Fact]
        public void TestGetObjectGraph()
        {
            _activity.Object.OnCreate(_mockBundle.Object);
            Assert.Equal(_mockActivityObjectGraph.Object, _activity.Object.GetObjectGraph());
        }

        [Fact]
        public void TestInject_GraphInitialized()
        {
            _activity.Object.OnCreate(_mockBundle.Object);
            var target = new object();

            _activity.Object.Inject(target);
        }

        [Fact]
        public void TestInject_GraphNotInitialized()
        {
            Assert.Null(_activity.Object.GetObjectGraph());
            var target = new object();
            Assert.Throws<InvalidOperationException>(() => _activity.Object.Inject(target));
        }

        [Fact]
        public void TestGetModules()
        {
            var modules = _activity.Object.GetModules();
            Assert.NotNull(modules);
            Assert.Single(modules);
            Assert.IsType<InjectingActivityModule>(modules[0]);
        }
    }
}