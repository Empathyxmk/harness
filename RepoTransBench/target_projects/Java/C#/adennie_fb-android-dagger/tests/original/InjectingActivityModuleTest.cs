using Moq;
using Xunit;
using ProjectName;

namespace OriginalTests
{
    public class InjectingActivityModuleTest
    {
        private Mock<Activity> _mockActivity;
        private Mock<Injector> _mockInjector;
        private InjectingActivityModule _module;

        public InjectingActivityModuleTest()
        {
            _mockActivity = new Mock<Activity>();
            _mockInjector = new Mock<Injector>();
            _module = new InjectingActivityModule(_mockActivity.Object, _mockInjector.Object);
        }

        [Fact]
        public void TestProvideActivityContext()
        {
            var context = _module.ProvideActivityContext();
            Assert.NotNull(context);
            Assert.Equal(_mockActivity.Object, context);
        }

        [Fact]
        public void TestProvideActivity()
        {
            var activity = _module.ProvideActivity();
            Assert.NotNull(activity);
            Assert.Equal(_mockActivity.Object, activity);
        }

        [Fact]
        public void TestProvideActivityInjector()
        {
            var injector = _module.ProvideActivityInjector();
            Assert.NotNull(injector);
            Assert.Equal(_mockInjector.Object, injector);
        }
    }
}