using Moq;
using Xunit;
using ProjectName;

namespace PublicTests
{
    public class InjectingActivityModulePublicTest
    {
        private Mock<Activity> _mockActivity1;
        private Mock<Injector> _mockInjector1;
        private Mock<Activity> _mockActivity2;
        private Mock<Injector> _mockInjector2;
        private InjectingActivityModule _module1;
        private InjectingActivityModule _module2;

        public InjectingActivityModulePublicTest()
        {
            _mockActivity1 = new Mock<Activity>();
            _mockInjector1 = new Mock<Injector>();
            _mockActivity2 = new Mock<Activity>();
            _mockInjector2 = new Mock<Injector>();

            _module1 = new InjectingActivityModule(_mockActivity1.Object, _mockInjector1.Object);
            _module2 = new InjectingActivityModule(_mockActivity2.Object, _mockInjector2.Object);
        }

        [Fact]
        public void TestProvideActivityContextPublic()
        {
            var context = _module1.ProvideActivityContext();
            Assert.NotNull(context);
            Assert.Equal(_mockActivity1.Object, context);

            var context2 = _module2.ProvideActivityContext();
            Assert.NotNull(context2);
            Assert.Equal(_mockActivity2.Object, context2);
        }

        [Fact]
        public void TestProvideActivityPublic()
        {
            var activityRes = _module1.ProvideActivity();
            Assert.NotNull(activityRes);
            Assert.Equal(_mockActivity1.Object, activityRes);

            var activityRes2 = _module2.ProvideActivity();
            Assert.NotNull(activityRes2);
            Assert.Equal(_mockActivity2.Object, activityRes2);
        }

        [Fact]
        public void TestProvideActivityInjectorPublic()
        {
            var result1 = _module1.ProvideActivityInjector();
            Assert.NotNull(result1);
            Assert.Equal(_mockInjector1.Object, result1);

            var result2 = _module2.ProvideActivityInjector();
            Assert.NotNull(result2);
            Assert.Equal(_mockInjector2.Object, result2);
        }
    }
}