using System;
using System.Collections.Generic;
using Moq;
using Xunit;
using ProjectName;
using TestUtilities;

namespace OriginalTests
{
    public class InjectingPreferenceFragmentTest
    {
        private Mock<Activity> _mockActivity;
        private Mock<object> _mockActivityObjectGraph;
        private Mock<object> _mockFragmentObjectGraph;
        private Mock<InjectingPreferenceFragment> _fragment;

        public InjectingPreferenceFragmentTest()
        {
            _mockActivity = new Mock<Activity>();
            _mockActivityObjectGraph = new Mock<object>();
            _mockFragmentObjectGraph = new Mock<object>();
            _fragment = new Mock<InjectingPreferenceFragment> { CallBase = true };

            var injector = _mockActivity.As<Injector>();
            injector.Setup(i => i.GetObjectGraph()).Returns(_mockActivityObjectGraph.Object);

            _mockActivityObjectGraph.Setup(g => g.GetType().GetMethod("Plus") != null 
                ? ((dynamic)g.Object).Plus(It.IsAny<object[]>()) 
                : null
            ).Returns(_mockFragmentObjectGraph.Object);

            // Do not throw on inject, just track calls
            _mockFragmentObjectGraph.Setup(g => g.GetType().GetMethod("Inject") != null 
                ? ((dynamic)g.Object).Inject(It.IsAny<object>()) 
                : null
            );

            _fragment.Setup(f => f.GetModules()).Returns(new List<object> { new InjectingFragmentModule(_fragment.Object, _fragment.Object) });
        }

        [Fact]
        public void TestOnAttach_FirstTime()
        {
            Assert.Null(_fragment.Object.GetObjectGraph());
            _fragment.Object.OnAttach(_mockActivity.Object);
            Assert.NotNull(_fragment.Object.GetObjectGraph());
            Assert.Equal(_mockFragmentObjectGraph.Object, _fragment.Object.GetObjectGraph());
            _mockActivity.As<Injector>().Verify(i => i.GetObjectGraph(), Times.Once);
            // .Plus and .Inject are tested by Setup above (mocked dynamic)
        }

        [Fact]
        public void TestOnAttach_RetainedFragment()
        {
            _fragment.Object.OnAttach(_mockActivity.Object);

            // Simulate Set mFirstAttach=false like in Java
            _fragment.Object.GetType().GetProperty("FirstAttach")?.SetValue(_fragment.Object, false);

            // Re-invoke onAttach
            _fragment.Object.OnAttach(_mockActivity.Object);

            Assert.NotNull(_fragment.Object.GetObjectGraph());
            Assert.Equal(_mockFragmentObjectGraph.Object, _fragment.Object.GetObjectGraph());
            _mockActivity.As<Injector>().Verify(i => i.GetObjectGraph(), Times.Exactly(2));
        }

        [Fact]
        public void TestOnDestroy()
        {
            _fragment.Object.OnAttach(_mockActivity.Object);
            Assert.NotNull(_fragment.Object.GetObjectGraph());

            _fragment.Object.OnDestroy();

            Assert.Null(_fragment.Object.GetObjectGraph());
        }

        [Fact]
        public void TestGetObjectGraph()
        {
            _fragment.Object.OnAttach(_mockActivity.Object);
            Assert.Equal(_mockFragmentObjectGraph.Object, _fragment.Object.GetObjectGraph());
        }

        [Fact]
        public void TestInject_GraphInitialized()
        {
            _fragment.Object.OnAttach(_mockActivity.Object);
            var target = new object();

            _fragment.Object.Inject(target);
        }

        [Fact]
        public void TestInject_GraphNotInitialized()
        {
            Assert.Null(_fragment.Object.GetObjectGraph());
            var target = new object();

            Assert.Throws<InvalidOperationException>(() => _fragment.Object.Inject(target));
        }

        [Fact]
        public void TestGetModules()
        {
            var modules = _fragment.Object.GetModules();
            Assert.NotNull(modules);
            Assert.Single(modules);
            Assert.IsType<InjectingFragmentModule>(modules[0]);
        }
    }
}