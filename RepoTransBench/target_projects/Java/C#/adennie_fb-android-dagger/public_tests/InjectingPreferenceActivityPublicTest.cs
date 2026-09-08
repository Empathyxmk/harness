using System.Collections.Generic;
using Moq;
using Xunit;
using ProjectName;
using TestUtilities;

namespace PublicTests
{
    public class InjectingPreferenceActivityPublicTest
    {
        private Mock<object> _mockAppGraphPublic;
        private Mock<object> _mockActivityObjectGraphPublic;
        private Mock<Bundle> _mockBundle;
        private TestUtilities.TestUtils.InjectingApplication _mockInjectingApplicationPublic;
        private Mock<InjectingPreferenceActivity> _activity;

        public InjectingPreferenceActivityPublicTest()
        {
            _mockAppGraphPublic = new Mock<object>();
            _mockActivityObjectGraphPublic = new Mock<object>();
            _mockBundle = new Mock<Bundle>();
            _mockInjectingApplicationPublic = new TestUtilities.TestUtils.InjectingApplication();
            _mockInjectingApplicationPublic.SetObjectGraph(_mockAppGraphPublic.Object);

            _activity = new Mock<InjectingPreferenceActivity> { CallBase = true };
            _activity.Setup(a => a.GetApplication()).Returns(_mockInjectingApplicationPublic);

            _mockAppGraphPublic.Setup(g => g.GetType().GetMethod("Plus") != null
                ? ((dynamic)g.Object).Plus(It.IsAny<object[]>()) : null
            ).Returns(_mockActivityObjectGraphPublic.Object);

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
            Assert.Equal(_mockActivityObjectGraphPublic.Object, _activity.Object.GetObjectGraph());
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
            Assert.Equal(_mockActivityObjectGraphPublic.Object, _activity.Object.GetObjectGraph());
        }

        [Fact]
        public void TestInject_GraphInitializedPublic()
        {
            _activity.Object.OnCreate(_mockBundle.Object);
            object target = "AnotherTarget";
            _activity.Object.Inject(target);
        }

        [Fact]
        public void TestInject_GraphNotInitializedPublic()
        {
            Assert.Null(_activity.Object.GetObjectGraph());
            object target = 0.01;
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