using System.Collections.Generic;
using Moq;
using Xunit;
using ProjectName;
using TestUtilities;

namespace PublicTests
{
    public class InjectingActionBarActivityPublicTest
    {
        private Mock<object> _mockAppObjectGraph;
        private Mock<object> _mockActivityObjectGraph;
        private Mock<Bundle> _mockBundle;
        private TestUtilities.TestUtils.InjectingApplication _mockInjectingApplication;
        private Mock<InjectingActionBarActivity> _activity;

        public InjectingActionBarActivityPublicTest()
        {
            _mockAppObjectGraph = new Mock<object>();
            _mockActivityObjectGraph = new Mock<object>();
            _mockBundle = new Mock<Bundle>();
            _mockInjectingApplication = new TestUtilities.TestUtils.InjectingApplication();
            _mockInjectingApplication.SetObjectGraph(_mockAppObjectGraph.Object);
            _activity = new Mock<InjectingActionBarActivity> { CallBase = true };

            _activity.Setup(a => a.GetApplication()).Returns(_mockInjectingApplication);

            _mockAppObjectGraph.Setup(g => g.GetType().GetMethod("Plus") != null
                ? ((dynamic)g.Object).Plus(It.IsAny<object[]>()) : null
            ).Returns(_mockActivityObjectGraph.Object);

            var modules = new List<object>
            {
                new InjectingActivityModule(_activity.Object, _activity.Object),
                new LoggingManager()
            };
            _activity.Setup(a => a.GetModules()).Returns(modules);
        }

        [Fact]
        public void TestOnCreatePublic()
        {
            Assert.Null(_activity.Object.GetObjectGraph());
            _activity.Object.OnCreate(_mockBundle.Object);

            Assert.NotNull(_activity.Object.GetObjectGraph());
            Assert.Equal(_mockActivityObjectGraph.Object, _activity.Object.GetObjectGraph());
        }

        [Fact]
        public void TestOnDestroyPublic()
        {
            _activity.Object.OnCreate(_mockBundle.Object);
            Assert.NotNull(_activity.Object.GetObjectGraph());

            _activity.Object.OnDestroy();

            Assert.Null(_activity.Object.GetObjectGraph());
        }

        [Fact]
        public void TestGetObjectGraphPublic()
        {
            _activity.Object.OnCreate(_mockBundle.Object);
            Assert.Equal(_mockActivityObjectGraph.Object, _activity.Object.GetObjectGraph());
        }

        [Fact]
        public void TestInject_GraphInitializedPublic()
        {
            _activity.Object.OnCreate(_mockBundle.Object);
            object target = "SomeTarget";
            _activity.Object.Inject(target);
        }

        [Fact]
        public void TestInject_GraphNotInitializedPublic()
        {
            Assert.Null(_activity.Object.GetObjectGraph());
            object target = 123456;
            Assert.Throws<System.InvalidOperationException>(() => _activity.Object.Inject(target));
        }

        [Fact]
        public void TestGetModulesPublic()
        {
            var modules = _activity.Object.GetModules();
            Assert.NotNull(modules);
            Assert.Equal(2, modules.Count);
            Assert.IsType<InjectingActivityModule>(modules[0]);
            Assert.IsType<LoggingManager>(modules[1]);
        }
    }
}