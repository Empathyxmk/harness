using System.Collections.Generic;
using Moq;
using Xunit;
using ProjectName;
using TestUtilities;

namespace OriginalTests
{
    public class InjectingPreferenceActivityTest
    {
        private Mock<object> _mockAppObjectGraph;
        private Mock<object> _mockActivityObjectGraph;
        private Mock<Bundle> _mockBundle;
        private TestUtils.InjectingApplication _mockInjectingApplication;
        private Mock<InjectingPreferenceActivity> _activity;

        public InjectingPreferenceActivityTest()
        {
            _mockAppObjectGraph = new Mock<object>();
            _mockActivityObjectGraph = new Mock<object>();
            _mockBundle = new Mock<Bundle>();
            _mockInjectingApplication = new TestUtils.InjectingApplication();
            _mockInjectingApplication.SetObjectGraph(_mockAppObjectGraph.Object);

            _activity = new Mock<InjectingPreferenceActivity> { CallBase = true };
            _activity.Setup(a => a.GetApplication()).Returns(_mockInjectingApplication);

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