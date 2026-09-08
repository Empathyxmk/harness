using System;
using System.Collections.Generic;
using Moq;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class InjectingPreferenceFragmentPublicTest
    {
        private Mock<Activity> _mockActivityPublic;
        private Mock<object> _mockActivityObjectGraphPublic;
        private Mock<object> _mockFragmentObjectGraphPublic;
        private Mock<InjectingPreferenceFragment> _fragment;

        public InjectingPreferenceFragmentPublicTest()
        {
            _mockActivityPublic = new Mock<Activity>();
            _mockActivityObjectGraphPublic = new Mock<object>();
            _mockFragmentObjectGraphPublic = new Mock<object>();
            _fragment = new Mock<InjectingPreferenceFragment> { CallBase = true };

            _mockActivityPublic.As<Injector>()
                .Setup(i => i.GetObjectGraph())
                .Returns(_mockActivityObjectGraphPublic.Object);

            _mockActivityObjectGraphPublic.Setup(g => g.GetType().GetMethod("Plus") != null
                ? ((dynamic)g.Object).Plus(It.IsAny<object[]>()) : null
            ).Returns(_mockFragmentObjectGraphPublic.Object);

            _mockFragmentObjectGraphPublic.Setup(g => g.GetType().GetMethod("Inject") != null
                ? ((dynamic)g.Object).Inject(It.IsAny<object>()) : null
            );

            _fragment.Setup(f => f.GetModules()).Returns(new List<object> { new LoggingManager() });
        }

        [Fact]
        public void TestOnAttach_FirstTimePublic()
        {
            Assert.Null(_fragment.Object.GetObjectGraph());
            _fragment.Object.OnAttach(_mockActivityPublic.Object);
            Assert.NotNull(_fragment.Object.GetObjectGraph());
            Assert.Equal(_mockFragmentObjectGraphPublic.Object, _fragment.Object.GetObjectGraph());
            _mockActivityPublic.As<Injector>().Verify(i => i.GetObjectGraph(), Times.Once);
        }

        [Fact]
        public void TestOnAttach_RetainedFragmentPublic()
        {
            _fragment.Object.OnAttach(_mockActivityPublic.Object);

            // Simulate Set mFirstAttach=false like in Java
            _fragment.Object.GetType().GetProperty("FirstAttach")?.SetValue(_fragment.Object, false);

            _fragment.Object.OnAttach(_mockActivityPublic.Object);

            Assert.NotNull(_fragment.Object.GetObjectGraph());
            Assert.Equal(_mockFragmentObjectGraphPublic.Object, _fragment.Object.GetObjectGraph());
            _mockActivityPublic.As<Injector>().Verify(i => i.GetObjectGraph(), Times.Exactly(2));
        }

        [Fact]
        public void TestOnDestroyPublic()
        {
            _fragment.Object.OnAttach(_mockActivityPublic.Object);
            Assert.NotNull(_fragment.Object.GetObjectGraph());

            _fragment.Object.OnDestroy();

            Assert.Null(_fragment.Object.GetObjectGraph());
        }

        [Fact]
        public void TestGetObjectGraphPublic()
        {
            _fragment.Object.OnAttach(_mockActivityPublic.Object);
            Assert.Equal(_mockFragmentObjectGraphPublic.Object, _fragment.Object.GetObjectGraph());
        }

        [Fact]
        public void TestInject_GraphInitializedPublic()
        {
            _fragment.Object.OnAttach(_mockActivityPublic.Object);
            object target = "MyInjectedTarget";
            _fragment.Object.Inject(target);
        }

        [Fact]
        public void TestInject_GraphNotInitializedPublic()
        {
            Assert.Null(_fragment.Object.GetObjectGraph());
            object target = 999L;
            Assert.Throws<InvalidOperationException>(() => _fragment.Object.Inject(target));
        }

        [Fact]
        public void TestGetModulesPublic()
        {
            var modules = _fragment.Object.GetModules();
            Assert.NotNull(modules);
            Assert.Single(modules);
            Assert.IsType<LoggingManager>(modules[0]);
        }
    }
}